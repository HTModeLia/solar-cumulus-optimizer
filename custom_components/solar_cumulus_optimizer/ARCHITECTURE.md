# 🏗️ Architecture - Solar Cumulus Optimizer

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                   HOME ASSISTANT                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │     Solar Cumulus Optimizer (custom component)      │    │
│  │                                                      │    │
│  │  ┌────────────────────────────────────────────┐    │    │
│  │  │ SolarCumulusCoordinator                    │    │    │
│  │  │ ├─ Récupère données (Linky, solaire, etc) │    │    │
│  │  │ ├─ Analyze conditions                      │    │    │
│  │  │ ├─ Décide activation/désactivation         │    │    │
│  │  │ └─ Maintient l'état global                │    │    │
│  │  └────────────────────────────────────────────┘    │    │
│  │                         ▲                             │    │
│  │                         │ Met à jour chaque minute    │    │
│  │                         ▼                             │    │
│  │  ┌────────────────────────────────────────────┐    │    │
│  │  │          OptimizationState                  │    │    │
│  │  │  ├─ relay_active: bool                     │    │    │
│  │  │  ├─ relay_reason: str                      │    │    │
│  │  │  ├─ solar_power: float                     │    │    │
│  │  │  ├─ cloud_detected: bool                   │    │    │
│  │  │  └─ daily_stats: dict                      │    │    │
│  │  └────────────────────────────────────────────┘    │    │
│  │           ▲                             ▼            │    │
│  │           │                             │            │    │
│  │  ┌────────┴────────────────────────────┴──┐        │    │
│  │  │                                         │        │    │
│  │  ├─ switch.py (Switch entity)            │        │    │
│  │  ├─ sensor.py (Sensor entities)          │        │    │
│  │  └─ config_flow.py (Configuration UI)    │        │    │
│  │                                            │        │    │
│  └────────────────────────────────────────────┘        │    │
│                                                          │    │
└─────────────────────────────────────────────────────────────┘

         ▲                                          ▼
         │                                          │
    ┌────┴─────────────────────────────────────────┴──────┐
    │            ENTITÉS HOME ASSISTANT                   │
    ├──────────────────────────────────────────────────────┤
    │                                                       │
    │  ENTRÉES (lecture):                                  │
    │  ├─ sensor.solar_power_now (W)                      │
    │  ├─ sensor.linky_ntraf (1=HP, 2+=HC)               │
    │  ├─ sensor.linky_sinti (injection W)               │
    │  ├─ weather.home (conditions)                       │
    │  └─ sensor.outside_temperature (°C)                 │
    │                                                       │
    │  SORTIES (contrôle):                                │
    │  └─ switch.cumulus_relay (on/off)                   │
    │                                                       │
    └──────────────────────────────────────────────────────┘
              ▲                                      ▼
              │                                      │
         ┌────┴──────────────────────────────────────┴────┐
         │         SOURCES DE DONNÉES EXTERNES            │
         ├────────────────────────────────────────────────┤
         │                                                 │
         │  ☀️ INVERSEUR SOLAIRE                         │
         │  (Fronius, Solax, SMA, etc)                   │
         │                                                 │
         │  ⚡ LINKY (ENEDIS)                            │
         │  (NTRAF, SINTI, etc)                          │
         │                                                 │
         │  🌤️ SERVICE MÉTÉO                             │
         │  (OpenWeatherMap, MeteoFrance, etc)           │
         │                                                 │
         └────────────────────────────────────────────────┘
```

## Flux Logique d'Optimisation

```
┌─ Chaque minute ─┐
│                 ▼
│         Récupère données:
│    ├─ Puissance solaire
│    ├─ Tarif Linky (HP/HC)
│    ├─ Injection réseau
│    ├─ Conditions météo
│    └─ Température ext
│                 │
│                 ▼
│         Détecte nuages?
│    ├─ Calcule moyenne 5 min
│    └─ Chute > seuil?
│                 │
│                 ▼
│         Vérifie runtime min
│    └─ Pas expiré? → Continue
│                 │
│                 ▼
│         Logique activation:
│    ├─ Mode SOLAR:
│    │  ├─ Jour?
│    │  ├─ Puissance > seuil?
│    │  └─ Injection > 100W?
│    │
│    ├─ Mode HC NUIT:
│    │  ├─ Nuit?
│    │  ├─ Tarif HC?
│    │  └─ T° ext < seuil OU mauvais temps?
│    │
│    └─ Sinon: IDLE
│                 │
│                 ▼
│         Activation/Désactivation
│    └─ Envoie commande relais
│                 │
│                 ▼
│         Mise à jour stats
│    ├─ Nombre activations
│    ├─ Temps cumulé
│    └─ Consommation estimée
│                 │
│                 ▼
│         Actualise UI
│    └─ Dashboard + Sensors
│                 │
└─────────── Boucle ──────────┘
```

## États et Transitions

```
                    ┌──────────┐
                    │  IDLE    │
                    └─────┬────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
      ┌────────┐   ┌────────┐   ┌────────────┐
      │ SOLAR  │   │HC_NIGHT│   │MIN_RUNTIME │
      └────────┘   └────────┘   └────────────┘
            │             │             │
            └─────────────┼─────────────┘
                          │
                          ▼
                 Relais ACTIF (ON)
                          │
                ┌─────────┴─────────┐
                │                   │
            Dés-activation      Runtime min
            manuelle            expiré
                │                   │
                └─────────┬─────────┘
                          ▼
                    Retour IDLE
```

## Historique de Puissance

Pour détecter les nuages transitoires :

```
Temps (minutes)
│
│ 2500W ┌──────────┐
│       │  Normal  │
│ 2000W │      ┌───┴────┐
│       │      │ Nuage  │ ← Chute 40%
│ 1000W │  ────┤        │────
│       │      └─────────┘
│    0W ├────────────────────→
│       0    2    4    6    8

Détection:
- Moyenne 5 dernières minutes
- Si chute > 30% → cloud_detected = True
- Bascule possible en HC de nuit
```

## Entités et Attributs

### Switch: `switch.cumulus_control`

**État:**
- `on`: Relais actif
- `off`: Relais inactif

**Attributs:**
```json
{
  "reason": "solar|hc_night|idle|min_runtime|manual",
  "active": true,
  "solar_power_w": 1234.5,
  "cloud_detected": false,
  "min_runtime_end": "2024-01-15T14:32:45",
  "last_activation": "2024-01-15T14:00:00"
}
```

### Sensors

| Entity ID | Type | Unité | Description |
|-----------|------|-------|-------------|
| `sensor.cumulus_status` | Chaîne | - | Raison activation |
| `sensor.cumulus_solar_power` | Nombre | W | Puissance instantanée |
| `sensor.cumulus_cloud_detection` | Chaîne | - | État ciel |
| `sensor.cumulus_daily_solar_activations` | Nombre | - | Compteur jour |
| `sensor.cumulus_daily_solar_runtime` | Nombre | s | Temps jour |
| `sensor.cumulus_daily_hc_activations` | Nombre | - | Compteur jour |
| `sensor.cumulus_daily_hc_runtime` | Nombre | s | Temps jour |
| `sensor.cumulus_last_duration` | Nombre | s | Dernière durée |

## Configuration Options

```python
Config = {
    # Seuils
    "min_solar_power": 500,          # W - Activation solaire
    "cloud_threshold": 30,           # % - Détection nuage
    "hysteresis": 50,                # W - Hystérésis (non utilisé actuellement)
    
    # Durées
    "min_runtime": 120,              # min - Runtime minimum
    "max_runtime": 180,              # min - Runtime maximum (non appliqué)
    
    # Température
    "night_temp_threshold": 5,       # °C - Seuil HC nuit
    
    # Entités
    "solar_power_entity": "sensor.solar_power_now",
    "cumulus_relay_entity": "switch.cumulus_relay",
    "weather_entity": "weather.home",
    "linky_ntraf_entity": "sensor.linky_ntraf",
    "linky_sinti_entity": "sensor.linky_sinti",
    "temp_outside_entity": "sensor.outside_temperature"
}
```

## Cycle de Vie

### Initialisation
1. Composant chargé
2. Config flow récupère entités
3. Coordinator créé
4. Entities (switch, sensors) initialisées
5. Premier refresh des données

### Fonctionnement
1. Coordinator update toutes les minutes
2. Récupère états entités
3. Applique logique d'optimisation
4. Change état si nécessaire
5. Met à jour sensors

### Shutdown
1. Composant déchargé
2. Coordinator arrêté
3. Listeners supprimés
4. Relais reste dans son état actuel

## Points de Customisation

### Pour les développeurs

**Ajouter nouvelle logique d'activation:**
```python
# Dans coordinator.py - _should_activate_relay()
if some_new_condition:
    return "new_mode"
```

**Ajouter nouveau sensor:**
```python
# Dans sensor.py
class NewSensor(SensorEntity):
    @property
    def native_value(self):
        return self.coordinator.state.some_value
```

**Modifier seuils:**
```yaml
# Options de l'intégration
min_solar_power: 300  # Plus sensible
cloud_threshold: 20   # Meilleure détection nuages
```

## Performances

- **Update interval**: 1 minute
- **Historique puissance**: 10 lectures (10 min)
- **Memory usage**: ~5-10 MB
- **CPU usage**: Minimal (~0.1%)
- **Latence activation**: <30 secondes

## Sécurité

- Aucune authentification externe
- Données locales (Home Assistant)
- Relais reste dans l'état actuel si crash
- Pas de dépendances externes
- Compatibilité Python 3.11+

---

**Version**: 1.0.0  
**Dernière mise à jour**: 2024  
**Compatibilité**: Home Assistant 2024.1.0+
