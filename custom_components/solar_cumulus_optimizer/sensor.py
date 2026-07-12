"""Platform sensor pour Solar Cumulus Optimizer."""

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup du platform sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            CumulusStatusSensor(coordinator, entry),
            SolarPowerSensor(coordinator, entry),
            CloudDetectionSensor(coordinator, entry),
            DailySolarActivationsSensor(coordinator, entry),
            DailySolarRuntimeSensor(coordinator, entry),
            DailyHCActivationsSensor(coordinator, entry),
            DailyHCRuntimeSensor(coordinator, entry),
            LastActivationDurationSensor(coordinator, entry),
        ]
    )


class CumulusStatusSensor(SensorEntity):
    """Capteur de statut du cumulus."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_status_{entry.entry_id}"
        self._attr_name = "Cumulus - Statut"
        self._attr_icon = "mdi:water-boiler"

    @property
    def native_value(self) -> str:
        """Retourne le statut."""
        state = self.coordinator.state
        if not state.relay_active:
            return "idle"
        return state.relay_reason

    @property
    def extra_state_attributes(self) -> dict:
        """Attributs supplémentaires."""
        state = self.coordinator.state
        return {
            "active": state.relay_active,
            "reason": state.relay_reason,
            "solar_power_w": round(state.solar_power, 1),
            "cloud_detected": state.cloud_detected,
            "min_runtime_end": state.min_runtime_end,
            "last_activation": state.last_activation,
        }

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class SolarPowerSensor(SensorEntity):
    """Capteur de puissance solaire."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_solar_power_{entry.entry_id}"
        self._attr_name = "Cumulus - Puissance Solaire"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:solar-power"

    @property
    def native_value(self) -> float:
        """Retourne la puissance solaire."""
        return round(self.coordinator.state.solar_power, 1)

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class CloudDetectionSensor(SensorEntity):
    """Capteur de détection de nuages."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_cloud_detection_{entry.entry_id}"
        self._attr_name = "Cumulus - Détection Nuages"
        self._attr_icon = "mdi:cloud"

    @property
    def native_value(self) -> str:
        """Retourne l'état de détection."""
        return "nuage" if self.coordinator.state.cloud_detected else "clair"

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class DailySolarActivationsSensor(SensorEntity):
    """Nombre d'activations solaires aujourd'hui."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_daily_solar_acts_{entry.entry_id}"
        self._attr_name = "Cumulus - Activations Solaire (Jour)"
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> int:
        """Retourne le nombre d'activations."""
        return self.coordinator.state.daily_stats["solar_activations"]

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class DailySolarRuntimeSensor(SensorEntity):
    """Durée d'activation solaire aujourd'hui."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_daily_solar_runtime_{entry.entry_id}"
        self._attr_name = "Cumulus - Temps Solaire (Jour)"
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:timer"

    @property
    def native_value(self) -> int:
        """Retourne le temps total."""
        return int(self.coordinator.state.daily_stats["solar_runtime"])

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class DailyHCActivationsSensor(SensorEntity):
    """Nombre d'activations HC aujourd'hui."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_daily_hc_acts_{entry.entry_id}"
        self._attr_name = "Cumulus - Activations HC (Jour)"
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> int:
        """Retourne le nombre d'activations."""
        return self.coordinator.state.daily_stats["hc_activations"]

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class DailyHCRuntimeSensor(SensorEntity):
    """Durée d'activation HC aujourd'hui."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_daily_hc_runtime_{entry.entry_id}"
        self._attr_name = "Cumulus - Temps HC (Jour)"
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_icon = "mdi:timer"

    @property
    def native_value(self) -> int:
        """Retourne le temps total."""
        return int(self.coordinator.state.daily_stats["hc_runtime"])

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class LastActivationDurationSensor(SensorEntity):
    """Durée de la dernière activation."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_last_duration_{entry.entry_id}"
        self._attr_name = "Cumulus - Dernière Durée"
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS
        self._attr_icon = "mdi:timer-outline"

    @property
    def native_value(self) -> int:
        """Retourne la durée."""
        return self.coordinator.state.activation_duration

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
