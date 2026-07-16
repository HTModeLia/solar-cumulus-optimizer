"""Platform sensor pour Solar Cumulus Optimizer."""

import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de la plateforme sensor."""
    try:
        coordinator = hass.data[DOMAIN][config_entry.entry_id]
        
        entities = [
            CumulusStatusSensor(coordinator, config_entry),
            SolarPowerSensor(coordinator, config_entry),
            CloudDetectionSensor(coordinator, config_entry),
            DailySolarActivationsSensor(coordinator, config_entry),
            DailySolarRuntimeSensor(coordinator, config_entry),
            DailyHCActivationsSensor(coordinator, config_entry),
            DailyHCRuntimeSensor(coordinator, config_entry),
            LastActivationDurationSensor(coordinator, config_entry),
        ]
        
        async_add_entities(entities)
        _LOGGER.debug(f"Added {len(entities)} sensor entities")
        
    except Exception as err:
        _LOGGER.error(f"Erreur setup sensor: {err}")
        raise


class SolarCumulusBaseSensor(SensorEntity):
    """Classe de base pour les capteurs Solar Cumulus Optimizer."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Retourne les informations du périphérique."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry.entry_id)},
            name=self.entry.title or "Solar Cumulus Optimizer",
            manufacturer="HTModeLia",
            model="Solar Cumulus Optimizer",
            sw_version="0.0.11",
        )

    @property
    def available(self) -> bool:
        """Disponibilité."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """Ajout à HA."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    def _handle_coordinator_update(self) -> None:
        """Mise à jour du coordinateur."""
        self.async_write_ha_state()


class CumulusStatusSensor(SolarCumulusBaseSensor):
    """Sensor pour le statut du cumulus."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_status_{entry.entry_id}"
        self._attr_name = "Cumulus - Statut"
        self._attr_icon = "mdi:information"

    @property
    def native_value(self) -> str:
        """Retourne le statut."""
        try:
            state = self.coordinator.data
            if state.relay_active:
                return state.relay_reason.upper()
            return "IDLE"
        except Exception:
            return "UNKNOWN"


class SolarPowerSensor(SolarCumulusBaseSensor):
    """Sensor pour la puissance solaire."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_solar_power_{entry.entry_id}"
        self._attr_name = "Cumulus - Puissance Solaire"
        self._attr_icon = "mdi:solar-power"
        self._attr_unit_of_measurement = "W"

    @property
    def native_value(self) -> float:
        """Retourne la puissance."""
        try:
            return self.coordinator.data.solar_power
        except Exception:
            return 0


class CloudDetectionSensor(SolarCumulusBaseSensor):
    """Sensor pour la détection de nuages."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_cloud_detection_{entry.entry_id}"
        self._attr_name = "Cumulus - Détection Nuages"
        self._attr_icon = "mdi:cloud"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str:
        """Retourne état."""
        try:
            return "NUAGEUX" if self.coordinator.data.cloud_detected else "CLAIR"
        except Exception:
            return "UNKNOWN"


class DailySolarActivationsSensor(SolarCumulusBaseSensor):
    """Sensor pour compteur activations solaires."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_daily_solar_activations_{entry.entry_id}"
        self._attr_name = "Cumulus - Activations Solaire (Jour)"
        self._attr_icon = "mdi:counter"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> int:
        """Retourne le nombre."""
        try:
            return self.coordinator.data.daily_stats.get("solar_activations", 0)
        except Exception:
            return 0


class DailySolarRuntimeSensor(SolarCumulusBaseSensor):
    """Sensor pour temps solaire."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_daily_solar_runtime_{entry.entry_id}"
        self._attr_name = "Cumulus - Temps Solaire (Jour)"
        self._attr_icon = "mdi:clock"
        self._attr_unit_of_measurement = "h"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float:
        """Retourne le temps en heures."""
        try:
            seconds = self.coordinator.data.daily_stats.get("solar_runtime", 0)
            return round(seconds / 3600, 2)
        except Exception:
            return 0


class DailyHCActivationsSensor(SolarCumulusBaseSensor):
    """Sensor pour compteur HC."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_daily_hc_activations_{entry.entry_id}"
        self._attr_name = "Cumulus - Activations HC (Jour)"
        self._attr_icon = "mdi:counter"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> int:
        """Retourne le nombre."""
        try:
            return self.coordinator.data.daily_stats.get("hc_activations", 0)
        except Exception:
            return 0


class DailyHCRuntimeSensor(SolarCumulusBaseSensor):
    """Sensor pour temps HC."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_daily_hc_runtime_{entry.entry_id}"
        self._attr_name = "Cumulus - Temps HC (Jour)"
        self._attr_icon = "mdi:clock"
        self._attr_unit_of_measurement = "h"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float:
        """Retourne le temps en heures."""
        try:
            seconds = self.coordinator.data.daily_stats.get("hc_runtime", 0)
            return round(seconds / 3600, 2)
        except Exception:
            return 0


class LastActivationDurationSensor(SolarCumulusBaseSensor):
    """Sensor pour dernière durée."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{DOMAIN}_last_activation_duration_{entry.entry_id}"
        self._attr_name = "Cumulus - Dernière Durée"
        self._attr_icon = "mdi:clock"
        self._attr_unit_of_measurement = "s"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> int:
        """Retourne la durée en secondes."""
        try:
            return self.coordinator.data.activation_duration
        except Exception:
            return 0