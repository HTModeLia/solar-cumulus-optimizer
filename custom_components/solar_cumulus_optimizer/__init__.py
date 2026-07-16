"""Solar Cumulus Optimizer - Service de Forçage Manuel avec Timer
Optimisé pour Home Assistant 2026.7+
Username: HTModeLia
"""

import logging
from datetime import timedelta, datetime
from typing import Final
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, CALLBACK_TYPE
import voluptuous as vol

from .coordinator import SolarCumulusCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "solar_cumulus_optimizer"
PLATFORMS: Final = [Platform.SWITCH, Platform.SENSOR]

# Services
SERVICE_ACTIVATE_HEATING = "activate_heating"
SERVICE_DEACTIVATE_HEATING = "deactivate_heating"
SERVICE_RESET_STATS = "reset_stats"
SERVICE_FORCE_MODE = "force_mode"
SERVICE_SMART_ACTIVATE = "smart_activate"
SERVICE_FORCE_MANUAL_HEATING = "force_manual_heating"  # ⭐ NOUVEAU

# Schémas de validation
ACTIVATE_SCHEMA = vol.Schema({
    vol.Optional("reason", default="manual"): str,
    vol.Optional("notify", default=True): bool,
})

DEACTIVATE_SCHEMA = vol.Schema({
    vol.Optional("notify", default=True): bool,
})

RESET_STATS_SCHEMA = vol.Schema({})

FORCE_MODE_SCHEMA = vol.Schema({
    vol.Required("mode"): vol.In(["solar", "hc_night", "idle"]),
})

SMART_ACTIVATE_SCHEMA = vol.Schema({
    vol.Optional("temperature", default=20): vol.Coerce(float),
    vol.Optional("enable_notifications", default=True): bool,
    vol.Optional("enable_lights", default=False): bool,
})

# ⭐ NOUVEAU: Service de forçage manuel
FORCE_MANUAL_HEATING_SCHEMA = vol.Schema({
    vol.Required("duration"): vol.In(["constant", "2h", "1h", "30m", "15m"]),
    vol.Optional("notify", default=True): bool,
    vol.Optional("auto_disable", default=True): bool,
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configuration via YAML."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration via config flow."""
    try:
        hass.data.setdefault(DOMAIN, {})

        coordinator = SolarCumulusCoordinator(hass, entry)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN][entry.entry_id] = coordinator

        # ====== ENREGISTREMENT DES SERVICES ======

        async def handle_activate_heating(call: ServiceCall) -> None:
            """Service: Activer le chauffage."""
            await _activate_heating_service(hass, call, coordinator)

        async def handle_deactivate_heating(call: ServiceCall) -> None:
            """Service: Désactiver le chauffage."""
            await _deactivate_heating_service(hass, call, coordinator)

        async def handle_reset_stats(call: ServiceCall) -> None:
            """Service: Réinitialiser les stats."""
            await _reset_stats_service(hass, call, coordinator)

        async def handle_force_mode(call: ServiceCall) -> None:
            """Service: Forcer un mode."""
            await _force_mode_service(hass, call, coordinator)

        async def handle_smart_activate(call: ServiceCall) -> None:
            """Service: Activation intelligente."""
            await _smart_activate_service(hass, call, coordinator)

        async def handle_force_manual_heating(call: ServiceCall) -> None:
            """Service: Forçage manuel avec timer. ⭐ NOUVEAU"""
            await _force_manual_heating_service(hass, call, coordinator)

        # Enregistrer les services
        hass.services.async_register(
            DOMAIN,
            SERVICE_ACTIVATE_HEATING,
            handle_activate_heating,
            schema=ACTIVATE_SCHEMA,
        )

        hass.services.async_register(
            DOMAIN,
            SERVICE_DEACTIVATE_HEATING,
            handle_deactivate_heating,
            schema=DEACTIVATE_SCHEMA,
        )

        hass.services.async_register(
            DOMAIN,
            SERVICE_RESET_STATS,
            handle_reset_stats,
            schema=RESET_STATS_SCHEMA,
        )

        hass.services.async_register(
            DOMAIN,
            SERVICE_FORCE_MODE,
            handle_force_mode,
            schema=FORCE_MODE_SCHEMA,
        )

        hass.services.async_register(
            DOMAIN,
            SERVICE_SMART_ACTIVATE,
            handle_smart_activate,
            schema=SMART_ACTIVATE_SCHEMA,
        )

        # ⭐ ENREGISTRER LE SERVICE DE FORÇAGE MANUEL
        hass.services.async_register(
            DOMAIN,
            SERVICE_FORCE_MANUAL_HEATING,
            handle_force_manual_heating,
            schema=FORCE_MANUAL_HEATING_SCHEMA,
        )

        _LOGGER.info("✓ 6 services enregistrés pour Solar Cumulus Optimizer (HA 2026.7+)")

        # Forward entry setup to platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        return True

    except Exception as err:
        _LOGGER.error(f"Erreur configuration: {err}")
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger une entrée de configuration."""
    try:
        if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
            hass.data[DOMAIN].pop(entry.entry_id)
            return True
        return False

    except Exception as err:
        _LOGGER.error(f"Erreur déchargement: {err}")
        return False


# ====== IMPLÉMENTATION DES SERVICES ======

async def _activate_heating_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Activer le chauffage avec notification."""
    try:
        reason = call.data.get("reason", "manual")
        notify = call.data.get("notify", True)

        await coordinator._activate_relay(reason)

        if notify:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "☀️ Cumulus Solaire",
                    "message": f"Chauffage activé ({reason.upper()})",
                    "notification_id": "solar_cumulus_heating",
                },
            )

        await coordinator.async_request_refresh()
        _LOGGER.info(f"✓ Activation chauffage: {reason}")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur activation: {err}")


async def _deactivate_heating_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Désactiver le chauffage."""
    try:
        notify = call.data.get("notify", True)

        duration = coordinator.data.activation_duration if coordinator.data else 0

        await coordinator._deactivate_relay()

        if notify:
            duration_str = f"{duration}s" if duration else "N/A"
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "❌ Cumulus Solaire",
                    "message": f"Chauffage désactivé (durée: {duration_str})",
                    "notification_id": "solar_cumulus_heating",
                },
            )

        await coordinator.async_request_refresh()
        _LOGGER.info(f"✓ Désactivation chauffage ({duration}s)")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur désactivation: {err}")


async def _reset_stats_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Réinitialiser les stats du jour."""
    try:
        coordinator.data.daily_stats = {
            "solar_activations": 0,
            "solar_runtime": 0,
            "hc_activations": 0,
            "hc_runtime": 0,
        }

        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "🔄 Cumulus Solaire",
                "message": "Statistiques réinitialisées",
                "notification_id": "solar_cumulus_reset",
            },
        )

        await coordinator.async_request_refresh()
        _LOGGER.info("✓ Stats réinitialisées")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur reset stats: {err}")


async def _force_mode_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Forcer un mode de fonctionnement."""
    try:
        mode = call.data.get("mode")

        if mode == "solar":
            await coordinator._activate_relay("solar_forced")
            message = "Mode SOLAIRE forcé"
        elif mode == "hc_night":
            await coordinator._activate_relay("hc_night_forced")
            message = "Mode HC NUIT forcé"
        elif mode == "idle":
            await coordinator._deactivate_relay()
            message = "Mode IDLE forcé"
        else:
            message = f"Mode inconnu: {mode}"

        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "⚙️ Cumulus Solaire",
                "message": message,
                "notification_id": "solar_cumulus_mode",
            },
        )

        await coordinator.async_request_refresh()
        _LOGGER.info(f"✓ Force mode: {mode}")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur force mode: {err}")


async def _smart_activate_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Activation intelligente avec multiples actions."""
    try:
        temp = call.data.get("temperature", 20)
        notifications = call.data.get("enable_notifications", True)
        lights = call.data.get("enable_lights", False)

        actions = []

        await coordinator._activate_relay("smart_mode")
        _LOGGER.info("✓ Activation smart mode")

        if lights:
            actions.append(
                hass.services.async_call(
                    "light",
                    "turn_on",
                    {"entity_id": "light.kitchen", "brightness_pct": 80},
                )
            )

        if notifications:
            actions.append(
                hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {
                        "title": "🧠 Cumulus Solaire",
                        "message": f"Activation smart mode (T°={temp}°C, Lights={'ON' if lights else 'OFF'})",
                        "notification_id": "solar_cumulus_smart",
                    },
                )
            )

        if actions:
            await asyncio.gather(*actions, return_exceptions=True)

        await coordinator.async_request_refresh()
        _LOGGER.info(f"✓ Smart activation complète (T°={temp}°C)")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur smart activate: {err}")


# ⭐ NOUVEAU SERVICE: FORÇAGE MANUEL AVEC TIMER
async def _force_manual_heating_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Service de forçage manuel avec duration (constante ou X heures)."""
    try:
        duration = call.data.get("duration")
        notify = call.data.get("notify", True)
        auto_disable = call.data.get("auto_disable", True)

        # Convertir la durée en secondes
        duration_seconds = None
        duration_display = "CONSTANTE"

        if duration == "constant":
            duration_seconds = None  # Pas d'auto-désactivation
            duration_display = "CONSTANTE (marche continue)"
        elif duration == "2h":
            duration_seconds = 2 * 3600
            duration_display = "2 HEURES"
        elif duration == "1h":
            duration_seconds = 1 * 3600
            duration_display = "1 HEURE"
        elif duration == "30m":
            duration_seconds = 30 * 60
            duration_display = "30 MINUTES"
        elif duration == "15m":
            duration_seconds = 15 * 60
            duration_display = "15 MINUTES"

        # Action 1: Activer le cumulus
        await coordinator._activate_relay("manual_forced")

        # Action 2: Notification immédiate
        if notify:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "🎮 FORÇAGE MANUEL - Cumulus Solaire",
                    "message": f"Cumulus FORCÉ en marche pour: {duration_display}",
                    "notification_id": "solar_cumulus_manual_force",
                },
            )

        # Action 3: Planifier la désactivation automatique si nécessaire
        if auto_disable and duration_seconds:
            # Créer un timer avec attente
            async def auto_disable_callback():
                await asyncio.sleep(duration_seconds)
                # Vérifier que l'utilisateur n'a pas manuellement désactivé
                if coordinator.data.relay_active:
                    await coordinator._deactivate_relay()
                    if notify:
                        await hass.services.async_call(
                            "persistent_notification",
                            "create",
                            {
                                "title": "⏰ Cumulus Solaire",
                                "message": f"Forçage manuel terminé ({duration_display})",
                                "notification_id": "solar_cumulus_manual_end",
                            },
                        )
                    _LOGGER.info(f"✓ Forçage manuel expiré après {duration_display}")

            # Lancer la tâche en arrière-plan
            asyncio.create_task(auto_disable_callback())
            _LOGGER.info(f"✓ Timer de désactivation planifié pour {duration_display}")

        await coordinator.async_request_refresh()
        _LOGGER.info(f"✓ Forçage manuel activé: {duration_display}")

    except Exception as err:
        _LOGGER.error(f"❌ Erreur forçage manuel: {err}")