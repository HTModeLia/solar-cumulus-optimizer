"""Platform switch pour Solar Cumulus Optimizer."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup du platform switch."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            SolarCumulusControlSwitch(coordinator, entry),
        ]
    )


class SolarCumulusControlSwitch(SwitchEntity):
    """Switch de contrôle du cumulus."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_control_{entry.entry_id}"
        self._attr_name = "Cumulus Solaire - Contrôle"

    @property
    def is_on(self) -> bool:
        """Retourne l'état du relais."""
        return self.coordinator.state.relay_active

    @property
    def extra_state_attributes(self) -> dict:
        """Attributs supplémentaires."""
        state = self.coordinator.state
        return {
            "reason": state.relay_reason,
            "solar_power": state.solar_power,
            "cloud_detected": state.cloud_detected,
            "activation_duration": state.activation_duration,
            "last_activation": state.last_activation,
        }

    async def async_turn_on(self, **kwargs) -> None:
        """Active le switch."""
        await self.coordinator._activate_relay("manual")
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Désactive le switch."""
        await self.coordinator._deactivate_relay()
        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        """Désactive le polling (coordinateur s'en charge)."""
        return False

    async def async_added_to_hass(self) -> None:
        """Ajoute les listeners de mise à jour."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
