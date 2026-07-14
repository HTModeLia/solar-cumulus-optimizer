"""Platform switch pour Solar Cumulus Optimizer."""

import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configuration de la plateforme switch."""
    try:
        coordinator = hass.data[DOMAIN][config_entry.entry_id]
        
        entities = [
            SolarCumulusControlSwitch(coordinator, config_entry),
        ]
        
        async_add_entities(entities)
        _LOGGER.debug("Switch entity added")
        
    except Exception as err:
        _LOGGER.error(f"Erreur setup switch: {err}")
        raise


class SolarCumulusControlSwitch(SwitchEntity):
    """Switch de contrôle du cumulus."""

    def __init__(self, coordinator, entry: ConfigEntry):
        """Initialisation."""
        self.coordinator = coordinator
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_control_{entry.entry_id}"
        self._attr_name = "Cumulus Solaire - Contrôle"
        self._attr_icon = "mdi:water-boiler"
        self._attr_has_entity_name = True

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Retourne la disponibilité."""
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool:
        """Retourne l'état du relais."""
        try:
            return self.coordinator.data.relay_active
        except Exception:
            return False

    async def async_turn_on(self, **kwargs) -> None:
        """Active le relais."""
        try:
            await self.coordinator._activate_relay("manual")
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error(f"Erreur activation: {err}")

    async def async_turn_off(self, **kwargs) -> None:
        """Désactive le relais."""
        try:
            await self.coordinator._deactivate_relay()
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error(f"Erreur désactivation: {err}")

    async def async_added_to_hass(self) -> None:
        """Appelé quand l'entité est ajoutée à HA."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    def _handle_coordinator_update(self) -> None:
        """Mise à jour depuis le coordinateur."""
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self):
        """Attributs supplémentaires."""
        try:
            state = self.coordinator.data
            return {
                "relay_reason": state.relay_reason,
                "solar_power_w": state.solar_power,
                "cloud_detected": state.cloud_detected,
                "last_activation": state.last_activation.isoformat() if state.last_activation else None,
                "activation_duration": state.activation_duration,
            }
        except Exception:
            return {}