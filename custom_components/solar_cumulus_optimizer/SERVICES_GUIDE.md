# 🔧 REGROUPER LES ENTITÉS DANS UN SERVICE - Solar Cumulus Optimizer

## 📌 CONCEPT

Un **service** permet d'appeler une fonction qui agit sur plusieurs entités en une seule commande.

**Exemple**: Au lieu d'appeler individuellement:
- `switch.turn_on` (relais)
- `light.turn_on` (indicateur)
- `notify.send` (notification)

Vous créez un **service `solar_cumulus.activate_heating`** qui fait tout ça d'un coup.

---

## 🎯 SERVICES À AJOUTER

Pour Solar Cumulus Optimizer, créer 3 services:

1. **`activate_heating`** - Active le cumulus + notification
2. **`deactivate_heating`** - Désactive + notification
3. **`reset_stats`** - Réinitialise les stats du jour

---

## 📝 IMPLÉMENTATION

### Étape 1: Modifier `__init__.py`

Ajouter l'enregistrement des services:

```python
"""Solar Cumulus Optimizer - Services."""

import logging
from datetime import timedelta
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol

from .coordinator import SolarCumulusCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "solar_cumulus_optimizer"
PLATFORMS: Final = [Platform.SWITCH, Platform.SENSOR]

# Définir les services
SERVICE_ACTIVATE_HEATING = "activate_heating"
SERVICE_DEACTIVATE_HEATING = "deactivate_heating"
SERVICE_RESET_STATS = "reset_stats"
SERVICE_FORCE_MODE = "force_mode"

# Schémas de validation
ACTIVATE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Optional("reason", default="manual"): str,
    vol.Optional("notify", default=True): bool,
})

DEACTIVATE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Optional("notify", default=True): bool,
})

RESET_STATS_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
})

FORCE_MODE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("mode"): vol.In(["solar", "hc_night", "idle"]),
})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Configuration du composant via YAML."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configuration du composant via config flow."""
    try:
        hass.data.setdefault(DOMAIN, {})

        coordinator = SolarCumulusCoordinator(hass, entry)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN][entry.entry_id] = coordinator

        # Enregistrer les services
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

        _LOGGER.info("Services enregistrés pour Solar Cumulus")

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


# Fonctions de service
async def _activate_heating_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Activer le chauffage avec groupement d'actions."""
    try:
        reason = call.data.get("reason", "manual")
        notify = call.data.get("notify", True)

        # Action 1: Activer le relais
        await coordinator._activate_relay(reason)

        # Action 2: Notification
        if notify:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Cumulus Solaire",
                    "message": f"Chauffage activé ({reason})",
                    "notification_id": "solar_cumulus_heating",
                },
            )

        # Action 3: Mettre à jour le coordinator
        await coordinator.async_request_refresh()

        _LOGGER.info(f"Service activate_heating appelé ({reason})")

    except Exception as err:
        _LOGGER.error(f"Erreur service activate: {err}")


async def _deactivate_heating_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Désactiver le chauffage."""
    try:
        notify = call.data.get("notify", True)

        # Action 1: Désactiver le relais
        await coordinator._deactivate_relay()

        # Action 2: Notification
        if notify:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Cumulus Solaire",
                    "message": f"Chauffage désactivé après {coordinator.data.activation_duration}s",
                    "notification_id": "solar_cumulus_heating",
                },
            )

        # Action 3: Mettre à jour
        await coordinator.async_request_refresh()

        _LOGGER.info("Service deactivate_heating appelé")

    except Exception as err:
        _LOGGER.error(f"Erreur service deactivate: {err}")


async def _reset_stats_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Réinitialiser les stats du jour."""
    try:
        # Réinitialiser les stats
        coordinator.data.daily_stats = {
            "solar_activations": 0,
            "solar_runtime": 0,
            "hc_activations": 0,
            "hc_runtime": 0,
        }

        # Notifier
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "Cumulus Solaire",
                "message": "Statistiques réinitialisées",
                "notification_id": "solar_cumulus_reset",
            },
        )

        # Mettre à jour
        await coordinator.async_request_refresh()

        _LOGGER.info("Service reset_stats appelé")

    except Exception as err:
        _LOGGER.error(f"Erreur service reset: {err}")


async def _force_mode_service(hass: HomeAssistant, call: ServiceCall, coordinator) -> None:
    """Forcer un mode de fonctionnement."""
    try:
        mode = call.data.get("mode")

        if mode == "solar":
            await coordinator._activate_relay("solar_forced")
        elif mode == "hc_night":
            await coordinator._activate_relay("hc_night_forced")
        elif mode == "idle":
            await coordinator._deactivate_relay()

        # Notifier
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "Cumulus Solaire",
                "message": f"Mode forcé: {mode}",
                "notification_id": "solar_cumulus_mode",
            },
        )

        await coordinator.async_request_refresh()

        _LOGGER.info(f"Service force_mode appelé ({mode})")

    except Exception as err:
        _LOGGER.error(f"Erreur service force_mode: {err}")
```

---

## 📚 UTILISER LES SERVICES

### Dans les Automations YAML

```yaml
# automation.yaml

- alias: "Activer chauffage cumulus"
  trigger:
    platform: time_pattern
    minutes: 0
  action:
    service: solar_cumulus_optimizer.activate_heating
    data:
      entity_id: solar_cumulus_optimizer
      reason: "solar"
      notify: true

- alias: "Désactiver chauffage"
  trigger:
    platform: time_pattern
    minutes: 30
  action:
    service: solar_cumulus_optimizer.deactivate_heating
    data:
      entity_id: solar_cumulus_optimizer
      notify: true

- alias: "Réinitialiser stats chaque jour"
  trigger:
    platform: time
    at: "00:00:00"
  action:
    service: solar_cumulus_optimizer.reset_stats
    data:
      entity_id: solar_cumulus_optimizer
```

### Via Home Assistant UI

1. **Paramètres → Automations et scripts → Créer automatisation**
2. **Action → Service**
3. **Service**: `solar_cumulus_optimizer.activate_heating`
4. **Données**:
   ```json
   {
     "entity_id": "solar_cumulus_optimizer",
     "reason": "solar",
     "notify": true
   }
   ```

### Via appels de service directs

```yaml
service: solar_cumulus_optimizer.activate_heating
data:
  entity_id: solar_cumulus_optimizer
  reason: manual
  notify: true
```

---

## 🎨 DASHBOARD - BOUTONS DE SERVICE

```yaml
# Lovelace dashboard

type: vertical-stack
cards:
  - type: heading
    heading: Contrôle Manuel

  - type: grid
    columns: 2
    cards:
      # Bouton Activer
      - type: button
        name: Activer Chauffage
        icon: mdi:power
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.activate_heating
          data:
            entity_id: solar_cumulus_optimizer
            reason: manual
            notify: true

      # Bouton Désactiver
      - type: button
        name: Désactiver
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.deactivate_heating
          data:
            entity_id: solar_cumulus_optimizer
            notify: true

  - type: entities
    entities:
      - entity: switch.cumulus_solaire_controle
      - entity: sensor.cumulus_statut
      - entity: sensor.cumulus_puissance_solaire

  - type: button
    name: Réinitialiser Stats
    icon: mdi:refresh
    tap_action:
      action: call-service
      service: solar_cumulus_optimizer.reset_stats
      data:
        entity_id: solar_cumulus_optimizer
```

---

## 🔧 GROUPER PLUSIEURS SERVICES

### Créer un service "Super"

```python
# Dans __init__.py

SERVICE_SMART_ACTIVATE = "smart_activate"

SMART_ACTIVATE_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("temperature"): vol.Coerce(float),
    vol.Required("enable_notifications"): bool,
    vol.Required("enable_lights"): bool,
})

async def handle_smart_activate(call: ServiceCall) -> None:
    """Service intelligente activation."""
    try:
        temp = call.data.get("temperature")
        notifications = call.data.get("enable_notifications")
        lights = call.data.get("enable_lights")

        # 1. Activer le chauffage
        await coordinator._activate_relay("smart_mode")

        # 2. Allumer les lumières si demandé
        if lights:
            await hass.services.async_call(
                "light",
                "turn_on",
                {"entity_id": "light.kitchen"},
            )

        # 3. Envoyer notification si demandé
        if notifications:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {"title": "Cumulus", "message": f"Activation smart (T°={temp}°C)"},
            )

        # 4. Envoyer webhook
        await hass.services.async_call(
            "rest_command",
            "notify_cloud",
            {"message": "Cumulus activated"},
        )

        _LOGGER.info("Smart activation complete")

    except Exception as err:
        _LOGGER.error(f"Erreur smart activate: {err}")

hass.services.async_register(
    DOMAIN,
    SERVICE_SMART_ACTIVATE,
    handle_smart_activate,
    schema=SMART_ACTIVATE_SCHEMA,
)
```

**Usage**:
```yaml
service: solar_cumulus_optimizer.smart_activate
data:
  entity_id: solar_cumulus_optimizer
  temperature: 15.5
  enable_notifications: true
  enable_lights: true
```

---

## 📊 EXEMPLE COMPLET: SERVICE AVEC MULTIPLES ACTIONS

```python
SERVICE_FULL_CONTROL = "full_control"

FULL_CONTROL_SCHEMA = vol.Schema({
    vol.Required("entity_id"): str,
    vol.Required("action"): vol.In(["start", "stop", "pause"]),
    vol.Optional("duration"): vol.Coerce(int),
    vol.Optional("temperature_target"): vol.Coerce(float),
    vol.Optional("notify_phone"): bool,
    vol.Optional("notify_web"): bool,
    vol.Optional("log_to_influx"): bool,
})

async def handle_full_control(call: ServiceCall) -> None:
    """Service avec contrôle complet."""
    action = call.data.get("action")
    duration = call.data.get("duration")
    temp_target = call.data.get("temperature_target")
    notify_phone = call.data.get("notify_phone", False)
    notify_web = call.data.get("notify_web", False)
    log_influx = call.data.get("log_to_influx", False)

    try:
        # Action principale
        if action == "start":
            await coordinator._activate_relay("full_control")
        elif action == "stop":
            await coordinator._deactivate_relay()
        elif action == "pause":
            # Pause 30 minutes
            coordinator.data.paused = True

        # Notifications (groupées)
        notifications = []
        
        if notify_phone:
            notifications.append(
                hass.services.async_call(
                    "notify",
                    "mobile_app_iphone",
                    {"message": f"Cumulus {action}ed"},
                )
            )

        if notify_web:
            notifications.append(
                hass.services.async_call(
                    "persistent_notification",
                    "create",
                    {"title": "Cumulus", "message": f"Action: {action}"},
                )
            )

        # Exécuter toutes les notifications en parallèle
        if notifications:
            await asyncio.gather(*notifications)

        # Logging
        if log_influx:
            await hass.services.async_call(
                "influxdb",
                "write",
                {
                    "measurement": "cumulus",
                    "tags": {"action": action},
                    "fields": {"status": 1},
                },
            )

        # Data
        await coordinator.async_request_refresh()

        _LOGGER.info(f"Full control {action} completed")

    except Exception as err:
        _LOGGER.error(f"Erreur full_control: {err}")

hass.services.async_register(
    DOMAIN,
    SERVICE_FULL_CONTROL,
    handle_full_control,
    schema=FULL_CONTROL_SCHEMA,
)
```

**Usage**:
```yaml
service: solar_cumulus_optimizer.full_control
data:
  entity_id: solar_cumulus_optimizer
  action: start
  duration: 120
  temperature_target: 60
  notify_phone: true
  notify_web: true
  log_to_influx: true
```

---

## 🎯 AVANTAGES DES SERVICES

| Avantage | Description |
|----------|-------------|
| **Regroupement** | Une seule commande = plusieurs actions |
| **Réutilisabilité** | Utiliser dans automations et scripts |
| **Paramètres** | Passer des paramètres dynamiques |
| **Atomicité** | Actions regroupées = plus fiable |
| **Logging** | Tracer les appels de service |
| **UI** | Accessible dans l'UI Home Assistant |

---

## 🔍 VÉRIFIER LES SERVICES

**Paramètres → Outils → Développeur → Services**

Chercher: `solar_cumulus_optimizer`

Vous verrez:
- `solar_cumulus_optimizer.activate_heating`
- `solar_cumulus_optimizer.deactivate_heating`
- `solar_cumulus_optimizer.reset_stats`
- `solar_cumulus_optimizer.force_mode`

---

## 📞 EXEMPLE PRATIQUE COMPLET

**Automation: Chauffage intelligent**

```yaml
automation:
  - alias: "Cumulus - Chauffage Solaire Intelligent"
    trigger:
      - platform: time_pattern
        minutes: 0  # Chaque heure
    condition:
      - condition: template
        value_template: "{{ state_attr('sensor.cumulus_puissance_solaire', 'native_value') | float(0) > 500 }}"
    action:
      # Action 1: Service activation
      - service: solar_cumulus_optimizer.activate_heating
        data:
          entity_id: solar_cumulus_optimizer
          reason: "solar_auto"
          notify: true
      
      # Action 2: Envoyer SMS optionnel
      - service: notify.telegram
        data:
          message: "Cumulus activé automatiquement (solaire)"
      
      # Action 3: Logger
      - service: logger.log
        data:
          level: INFO
          message: "Cumulus heating activated"
```

---

## ✅ RÉSUMÉ

**Avec les services, vous pouvez**:

1. ✅ Regrouper plusieurs actions en une seule commande
2. ✅ Paramétrer dynamiquement les appels
3. ✅ Utiliser dans automations, scripts et UI
4. ✅ Logging et traçage centralisés
5. ✅ Meilleure maintenabilité du code

**Fichier à modifier**: `__init__.py`

**Copier-coller** les fonctions ci-dessus et adapter à vos besoins!

---

**Version**: 1.0.1  
**Difficulté**: Intermédiaire  
**Temps**: 30-45 min  
