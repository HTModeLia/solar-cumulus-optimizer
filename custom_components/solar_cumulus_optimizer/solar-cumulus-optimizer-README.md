# Solar Cumulus Optimizer

Composant Home Assistant pour optimiser la recharge de votre cumulus (ballon d'eau chaude) en fonction de la production solaire, des tarifs Linky et des prévisions météorologiques.

## Caractéristiques

🌞 **Optimisation Solaire**
- Activation automatique en cas de surproduction solaire
- Détection de nuages transitoires
- Historique de puissance sur 10 minutes

⚡ **Gestion des tarifs Linky**
- Utilise les tarifs HC/HP via `ntraf`
- Chauffage automatique en HC la nuit si nécessaire
- Considère l'injection d'énergie (`sinti`)

🌡️ **Intelligence Météo**
- Intégration avec votre intégration météo
- Chauffage préventif si mauvais temps prévu
- Seuil de température extérieure configurable

🔄 **Modes de Fonctionnement**
- **Solar**: Activation lors de surproduction
- **HC Night**: Activation en tarif HC de nuit
- **Min Runtime**: Garantit 2h minimum de fonctionnement continu
- **Manual**: Contrôle manuel via switch

## Installation

### Via HACS (Recommandé)

1. Ouvrir HACS dans Home Assistant
2. Aller à "Intégrations"
3. Cliquer sur "Créer une intégration personnalisée"
4. Chercher "Solar Cumulus Optimizer"
5. Installer et redémarrer Home Assistant

### Installation Manuelle

```bash
# Dans home-assistant/custom_components/
git clone https://github.com/HTModeLia/solar-cumulus-optimizer solar_cumulus_optimizer
```

Redémarrer Home Assistant.

## Configuration

1. **Aller à Paramètres > Appareils et Services > Créer une intégration**
2. **Chercher "Solar Cumulus Optimizer"**
3. **Compléter les entités requises:**
   - Entité de puissance solaire (W) - ex: `sensor.solar_power_now`
   - Entité du relais cumulus - ex: `switch.cumulus_relay`
   - Entité météo - ex: `weather.home`
   - Linky NTRAF - ex: `sensor.linky_ntraf`
   - Linky SINTI - ex: `sensor.linky_sinti`

4. **Configurer les options** (après création):
   - Puissance solaire minimale: 500W (défaut)
   - Durée minimale: 120 min (2h)
   - Durée maximale: 180 min (3h)
   - Seuil nuages: 30%
   - Seuil température nuit: 5°C

## Utilisation

### Entités disponibles

**Switch:**
- `switch.cumulus_control_*` - Contrôle manuel du cumulus

**Sensors:**
- `sensor.cumulus_status_*` - Statut actuel (solar, hc_night, idle)
- `sensor.cumulus_solar_power_*` - Puissance solaire actuellement vue
- `sensor.cumulus_cloud_detection_*` - Détection de nuages
- `sensor.cumulus_daily_solar_activations_*` - Nombre d'activations solaire du jour
- `sensor.cumulus_daily_solar_runtime_*` - Temps solaire cumulé (secondes)
- `sensor.cumulus_daily_hc_activations_*` - Nombre d'activations HC du jour
- `sensor.cumulus_daily_hc_runtime_*` - Temps HC cumulé (secondes)
- `sensor.cumulus_last_duration_*` - Durée de la dernière activation

### Automations Exemples

**Notification quand cumulus démarre:**
```yaml
automation:
  - alias: "Cumulus activation notification"
    trigger:
      entity_id: switch.cumulus_control
      to: "on"
    action:
      service: notify.mobile_app_votre_telephone
      data:
        message: >
          Cumulus activé ({{ state_attr('switch.cumulus_control', 'reason') }})
          Puissance solaire: {{ state_attr('switch.cumulus_control', 'solar_power_w') }}W
```

**Alerte si cumulus en HC trop souvent:**
```yaml
automation:
  - alias: "HC usage alert"
    trigger:
      entity_id: sensor.cumulus_daily_hc_activations
      to: "5"
    action:
      service: notify.mobile_app_votre_telephone
      data:
        message: "Cumulus: 5+ activations HC aujourd'hui - vérifier configuration"
```

## Logique d'Optimisation

### Priorités

1. **Vérifie si runtime min pas expirée** → Continue si < 2h
2. **Mode Solaire**: 
   - Si production > seuil (500W défaut)
   - ET injection > 100W
3. **Mode HC Nuit**:
   - Entre coucher/lever du soleil
   - ET tarif HC actif (ntraf >= 2)
   - ET (température extérieure < 5°C OU mauvais temps prévu)
4. **Sinon**: Mode idle

### Détection de Nuages

- Calcule moyenne des 5 dernières lectures
- Détecte chute de puissance > seuil (30% défaut)
- Bascule en HC de nuit si nuage détecté

## Diagnostique

### Logs

```yaml
logger:
  logs:
    custom_components.solar_cumulus_optimizer: debug
```

### Attributs du switch

```
reason: solar|hc_night|idle|min_runtime|manual
active: true/false
solar_power_w: 1234.5
cloud_detected: true/false
min_runtime_end: 2024-01-15T14:32:45
last_activation: 2024-01-15T14:00:00
```

## Dépannage

**Cumulus ne s'active jamais**
- Vérifier que l'entité du relais existe
- Vérifier que puissance solaire dépasse le seuil
- Vérifier les logs en debug

**Trop d'activations HC**
- Augmenter le seuil de température
- Vérifier intégration météo
- Vérifier données Linky

**Arrêt avant 2h**
- Vérifier que `min_runtime` est bien configuré
- Vérifier que puissance solaire baisse vraiment

## Architecture

```
solar_cumulus_optimizer/
├── __init__.py              # Point d'entrée
├── config_flow.py           # Configuration UI
├── coordinator.py           # Logique d'optimisation
├── switch.py               # Platform switch
├── sensor.py               # Platform sensor
├── strings.json            # Traductions
└── manifest.json           # Métadonnées
```

## Contribuer

Les PRs sont bienvenues! Pour les changements majeurs:
1. Fork le repo
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

MIT License - voir LICENSE pour détails

## Support

Pour des questions/issues:
- Ouvrir une issue sur GitHub
- Chercher des réponses dans les discussions existantes

## Crédits

Créé pour optimiser l'autoconsommation solaire avec Home Assistant.
