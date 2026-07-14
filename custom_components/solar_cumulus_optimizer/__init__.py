"""Solar Cumulus Optimizer - Optimisation recharge cumulus avec énergie solaire."""

import logging
from datetime import timedelta
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import SolarCumulusCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "solar_cumulus_optimizer"
PLATFORMS: Final = [Platform.SWITCH, Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configuration du composant via YAML."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration du composant via config flow."""
    try:
        # Initialiser les données
        hass.data.setdefault(DOMAIN, {})

        # Créer le coordinateur
        coordinator = SolarCumulusCoordinator(hass, entry)
        
        # Première récupération des données
        await coordinator.async_config_entry_first_refresh()

        # Stocker le coordinateur
        hass.data[DOMAIN][entry.entry_id] = coordinator

        # Forward entry setup to platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True
        
    except Exception as err:
        _LOGGER.error(f"Erreur lors de la configuration: {err}")
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger une entrée de configuration."""
    try:
        # Unload platforms
        if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
            # Supprimer les données
            hass.data[DOMAIN].pop(entry.entry_id)
            return True
        return False
        
    except Exception as err:
        _LOGGER.error(f"Erreur lors du déchargement: {err}")
        return False