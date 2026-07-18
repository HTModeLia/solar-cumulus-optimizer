"""Coordinator pour l'optimisation du cumulus solaire."""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


@dataclass
class OptimizationState:
    """État d'optimisation du cumulus."""

    relay_active: bool = False
    relay_reason: str = "idle"  # solar, hc_night, hc_planned, manual
    solar_power: float = 0.0
    solar_power_history: list[float] = field(default_factory=list)
    last_activation: Optional[datetime] = None
    activation_duration: int = 0  # en secondes
    next_hc_activation: Optional[datetime] = None
    cloud_detected: bool = False
    min_runtime_end: Optional[datetime] = None
    daily_stats: dict = field(default_factory=lambda: {
        "solar_activations": 0,
        "solar_runtime": 0,
        "hc_activations": 0,
        "hc_runtime": 0,
    })


class SolarCumulusCoordinator(DataUpdateCoordinator):
    """Coordinateur pour gérer l'optimisation du cumulus."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(
            hass,
            _LOGGER,
            name="Solar Cumulus Optimizer",
            update_interval=timedelta(minutes=1),
        )
        self.entry = entry
        self.state = OptimizationState()
        self._load_config()

    def _load_config(self):
        """Charge la configuration."""
        self.config = self.entry.data
        self.options = self.entry.options

        # Seuils configurables
        self.min_solar_power = self.options.get("min_solar_power", 500)  # Watts
        self.min_runtime = self.options.get("min_runtime", 120)  # minutes
        self.max_runtime = self.options.get("max_runtime", 180)  # minutes
        self.cloud_threshold = self.options.get("cloud_threshold", 30)  # % chute
        self.hysteresis = self.options.get("hysteresis", 50)  # Watts
        self.night_temp_threshold = self.options.get("night_temp_threshold", 5)  # °C

        # Entités
        self.solar_power_entity = self.config.get("solar_power_entity")
        self.cumulus_relay_entity = self.config.get("cumulus_relay_entity")
        self.weather_entity = self.config.get("weather_entity")
        self.linky_ntraf_entity = self.config.get("linky_ntraf_entity")
        self.linky_sinti_entity = self.config.get("linky_sinti_entity")
        self.temp_outside_entity = self.options.get("temp_outside_entity")

    async def _async_update_data(self) -> OptimizationState:
        """Récupère les données et décide de l'activation."""
        try:
            # Récupère les données actuelles avec valeurs par défaut
            solar_power = self._get_entity_value(self.solar_power_entity, 0)
            is_night = self._is_night()
            ntraf = self._get_entity_value(self.linky_ntraf_entity, 1)  # 1=HP par défaut
            sinti = self._get_entity_value(self.linky_sinti_entity, 0)  # injection en W
            outside_temp = self._get_entity_value(self.temp_outside_entity, 10)  # 10°C par défaut
            
            # Log en debug pour diagnostique
            _LOGGER.debug(
                f"Update: Power={solar_power}W, Night={is_night}, NTRAF={ntraf}, "
                f"SINTI={sinti}W, Temp={outside_temp}°C"
            )

            # Détecte les nuages
            self._detect_cloud_drop(solar_power)

            # Maj historique
            self.state.solar_power = solar_power
            self._update_power_history()

            # Vérifie si runtime min n'a pas expiré
            if self.state.min_runtime_end and datetime.now() < self.state.min_runtime_end:
                # Continuer le fonctionnement
                if not self.state.relay_active:
                    await self._activate_relay("min_runtime")
            else:
                self.state.min_runtime_end = None
                # Logique d'optimisation
                should_activate = self._should_activate_relay(
                    solar_power, is_night, ntraf, outside_temp, sinti
                )

                if should_activate and not self.state.relay_active:
                    await self._activate_relay(should_activate)
                elif not should_activate and self.state.relay_active:
                    await self._deactivate_relay()

            return self.state

        except Exception as err:
            raise UpdateFailed(f"Erreur mise à jour: {err}") from err

    def _should_activate_relay(
        self, solar_power: float, is_night: bool, ntraf: int, outside_temp: float, sinti: float
    ) -> Optional[str]:
        """Détermine si le relais doit être activé."""

        # Mode solaire
        if not is_night and solar_power >= self.min_solar_power:
            # Activation solaire si production suffisante, même sans injection forte
            if solar_power > self.min_solar_power or sinti > 50:
                return "solar"

        # Mode HC de nuit
        if is_night and ntraf >= 2:  # Tarif HC
            # HC de nuit : chauffer si T° extérieure basse ou météo prévoit mauvais temps
            if outside_temp < self.night_temp_threshold:
                return "hc_night"

            # Vérifier prévisions météo
            if self._is_bad_weather_expected():
                return "hc_night"

            # Fallback simple pour les horaires HC si la production solaire n'est pas disponible
            if solar_power < self.min_solar_power:
                return "hc_night"

        return None

    def _detect_cloud_drop(self, current_power: float):
        """Détecte une chute due à un nuage."""
        if len(self.state.solar_power_history) >= 5:
            avg_recent = sum(self.state.solar_power_history[-5:]) / 5
            if avg_recent > 0 and current_power < avg_recent * (1 - self.cloud_threshold / 100):
                self.state.cloud_detected = True
            else:
                self.state.cloud_detected = False

    def _update_power_history(self):
        """Maintient un historique de 10 min."""
        self.state.solar_power_history.append(self.state.solar_power)
        if len(self.state.solar_power_history) > 10:
            self.state.solar_power_history.pop(0)

    def _is_bad_weather_expected(self) -> bool:
        """Vérifie si mauvais temps attendu dans les 6h."""
        try:
            # Vérifier si l'entité météo est configurée
            if not self.weather_entity:
                return False
            
            weather = self.hass.states.get(self.weather_entity)
            if weather is None:
                return False

            condition = weather.state
            # Temps instable/nuageux/pluie
            bad_conditions = ["partlycloudy", "cloudy", "rainy", "snowy", "pouring"]
            return condition in bad_conditions
        except Exception as err:
            _LOGGER.debug(f"Erreur vérification météo: {err}")
            return False

    def _is_night(self) -> bool:
        """Retourne True s'il fait nuit (soleil sous l'horizon)."""
        return self.hass.states.is_state("sun.sun", "below_horizon")

    def _get_entity_value(self, entity_id: str, default: float = 0) -> float:
        """Récupère la valeur d'une entité."""
        try:
            # Vérifier si l'entité est vide/optionnelle
            if not entity_id:
                return default
            
            state = self.hass.states.get(entity_id)
            if state is None or state.state in ("unknown", "unavailable"):
                return default
            return float(state.state)
        except (ValueError, TypeError, AttributeError) as err:
            _LOGGER.debug(f"Erreur lecture entité {entity_id}: {err}")
            return default

    async def _activate_relay(self, reason: str):
        """Active le relais."""
        try:
            self.state.relay_active = True
            self.state.relay_reason = reason
            self.state.last_activation = datetime.now()

            # Défini la durée minimale
            self.state.min_runtime_end = datetime.now() + timedelta(
                minutes=self.min_runtime
            )

            await self.hass.services.async_call(
                "switch",
                "turn_on",
                {"entity_id": self.cumulus_relay_entity},
                blocking=False,
            )

            # Stats
            if reason == "solar":
                self.state.daily_stats["solar_activations"] += 1
            else:
                self.state.daily_stats["hc_activations"] += 1

            _LOGGER.info(f"Relais activé: {reason}")
        except Exception as err:
            _LOGGER.error(f"Erreur activation relais: {err}")
            raise

    async def _deactivate_relay(self):
        """Désactive le relais."""
        try:
            if self.state.last_activation:
                duration = (datetime.now() - self.state.last_activation).total_seconds()
                self.state.activation_duration = int(duration)

                # Stats
                if self.state.relay_reason == "solar":
                    self.state.daily_stats["solar_runtime"] += duration
                else:
                    self.state.daily_stats["hc_runtime"] += duration

            self.state.relay_active = False
            self.state.relay_reason = "idle"

            await self.hass.services.async_call(
                "switch",
                "turn_off",
                {"entity_id": self.cumulus_relay_entity},
                blocking=False,
            )

            _LOGGER.info(f"Relais désactivé après {self.state.activation_duration}s")
        except Exception as err:
            _LOGGER.error(f"Erreur désactivation relais: {err}")
            raise

    @callback
    def get_state(self) -> OptimizationState:
        """Retourne l'état actuel."""
        return self.state
