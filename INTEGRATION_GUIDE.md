# 🚀 Guide Complet d'Intégration Solar Cumulus Optimizer

## 1️⃣ Préparatifs

### Vérifier vos entités Home Assistant

Avant de commencer, assurez-vous d'avoir :

**Nécessaire :**
- Une entité de puissance solaire instantanée (en Watts)
  ```yaml
  # Exemple InfluxDB, MQTT, ou intégration solaire
  sensor.solar_power_now  # W
  sensor.solar_power      # W
  ```

- Un relais/switch pour contrôler le cumulus
  ```yaml
  switch.cumulus_relay    # State: on/off
  switch.water_heater     # State: on/off
  ```

- Linky NTRAF (1=HP, 2+=HC)
  ```yaml
  sensor.linky_ntraf      # State: 1 ou 2+
  ```

- Linky SINTI (injection en W)
  ```yaml
  sensor.linky_sinti      # W (positif = injection)
  ```

- Une entité météo Home Assistant
  ```yaml
  weather.home           # Fournie par intégration météo
  weather.maison         # (OpenWeatherMap, etc)
  ```

**Recommandé :**
- Capteur température extérieure
  ```yaml
  sensor.outside_temperature    # °C
  sensor.temp_ext              # °C
  ```

### Vérifier vos entités Linky

Pour obtenir les bonnes entités Linky :

1. **Installation Linky** :
```
HACS → Intégrations → Chercher "Linky" → Installer
Redémarrer Home Assistant
Paramètres → Appareils et services → Créer intégration → "Linky"
```

2. **Identifier les entités** :
```yaml
# Allez à Outils de développement > États
# Cherchez les entités comme :
- sensor.linky_ntraf  # Tarif actuel
- sensor.linky_sinti  # Injection
```

### Vérifier production solaire

Pour obtenir la puissance solaire instantanée :

**Option 1 : Inverseur Solax/Fronius/SMA**
```yaml
# Cherchez entités comme :
sensor.fronius_ac_power         # Puissance AC
sensor.solax_total_pv_power     # Puissance PV totale
sensor.sma_power_ac             # Puissance AC
```

**Option 2 : MQTT**
```yaml
# Publier depuis votre inverseur en MQTT
mosquitto_pub -h 192.168.1.100 -t 'solar/power' -m '2500'
# Créer capteur :
mqtt:
  sensor:
    - name: "Solar Power Now"
      state_topic: "solar/power"
      unit_of_measurement: "W"
```

**Option 3 : InfluxDB**
```yaml
# Créer capteur depuis InfluxDB
influxdb:
  scan_interval: 60
  sensor:
    - name: Solar Power
      unit_of_measurement: W
      measurement: solar_power_now
```

---

## 2️⃣ Préparation GitHub (optionnel mais recommandé)

### Créer un repository

1. Sur GitHub, créer un nouveau repo :
   - Nom: `solar-cumulus-optimizer`
   - Description: "Solar Cumulus Optimizer for Home Assistant"
   - Public (pour HACS)

2. Cloner et commencer :
```bash
git clone https://github.com/votre-user/solar-cumulus-optimizer.git
cd solar-cumulus-optimizer
```

3. Structure du repo :
```
solar-cumulus-optimizer/
├── custom_components/
│   └── solar_cumulus_optimizer/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── coordinator.py
│       ├── switch.py
│       ├── sensor.py
│       ├── strings.json
│       └── manifest.json
├── README.md
├── LICENSE (MIT)
└── .gitignore
```

4. Fichier .gitignore :
```
.DS_Store
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
```

5. Committer et pusher :
```bash
git add .
git commit -m "Initial commit: Solar Cumulus Optimizer"
git push origin main
```

---

## 3️⃣ Installation HACS

### Méthode 1 : Installation directe (sans GitHub)

1. **Créer manuellement le répertoire** :
```bash
mkdir -p /home/homeassistant/.homeassistant/custom_components/solar_cumulus_optimizer
```

2. **Copier les fichiers du composant** dans ce dossier

3. **Redémarrer Home Assistant** via l'interface

### Méthode 2 : Installation via HACS (avec GitHub)

1. **Enregistrer le repo dans HACS** :
   - Ouvrir HACS
   - Menu (≡) → Paramètres personnalisés (custom repositories)
   - Ajouter :
     ```
     URL: https://github.com/votre-user/solar-cumulus-optimizer
     Type: Integration
     Branche: main
     ```

2. **Installer** :
   - HACS → Intégrations
   - Chercher "Solar Cumulus Optimizer"
   - Cliquer "Installer"
   - Redémarrer Home Assistant

---

## 4️⃣ Configuration du Composant

### Via l'Interface

1. **Créer l'intégration** :
   - Paramètres → Appareils et services
   - Créer une intégration
   - Chercher "Solar Cumulus Optimizer"

2. **Configuration initiale** :
   - **Nom** : Donnez un nom (ex: "Cumulus Solaire")
   - **Solar Power Entity** : `sensor.solax_total_pv_power`
   - **Cumulus Relay Entity** : `switch.cumulus_relay`
   - **Weather Entity** : `weather.home`
   - **Linky NTRAF Entity** : `sensor.linky_ntraf`
   - **Linky SINTI Entity** : `sensor.linky_sinti`

3. **Valider** → L'intégration se crée

4. **Configurer les options** :
   - Cliquer sur l'intégration créée
   - Onglet "Options"
   - Régler :
     - **Puissance solaire minimale** : 500W (défaut)
       - ⬆️ Pour être plus sélectif
       - ⬇️ Pour plus de sensibilité
     - **Durée minimale** : 120 min (2h)
     - **Durée maximale** : 180 min (3h)
     - **Seuil de nuages** : 30% (détection chute de puissance)
     - **Seuil température nuit** : 5°C
     - **Entité température** : `sensor.outside_temperature` (optionnel)

---

## 5️⃣ Configuration Dashboard

### Importer le Dashboard

1. **Créer un nouveau dashboard** :
   - Accueil → Créer un nouveau tableau de bord
   - Nom : "Cumulus Solaire"

2. **Ajouter via YAML** :
   - Cliquer sur les 3 points (⋮)
   - Mode YAML (Modifier)
   - Copier-coller le contenu du fichier `solar-cumulus-dashboard.yaml`
   - Sauvegarder

3. **Ou ajouter manuellement** :
   - Cliquer "Ajouter une carte"
   - Type: "Entities" ou "Custom cards"

### Dépendances de cartes Custom (si nécessaire)

Pour le dashboard complet, installer les cartes customs :

```yaml
# HACS → Frontend
# Chercher et installer :
- mushroom-cards
- mini-graph-card
- apexcharts-card
- fold-entity-row
```

### Configuration simplifiée (sans cartes customs)

Si vous ne voulez pas les cartes customs :

```yaml
type: entities
title: Solar Cumulus Optimizer
entities:
  - entity: switch.cumulus_control
  - entity: sensor.cumulus_status
  - entity: sensor.cumulus_solar_power
  - entity: sensor.cumulus_cloud_detection
  - entity: sensor.cumulus_daily_solar_activations
  - entity: sensor.cumulus_daily_solar_runtime
  - entity: sensor.cumulus_daily_hc_activations
  - entity: sensor.cumulus_daily_hc_runtime
```

---

## 6️⃣ Configuration Automations

### Ajouter les automations

1. **Via YAML** :
   ```yaml
   # Dans configuration.yaml ou automation: !include automations.yaml
   automation: !include automations.yaml
   script: !include scripts.yaml
   ```

2. **Copier les exemples** :
   - Copier contenu `solar-cumulus-automations-examples.yaml`
   - Adapter les entités
   - Sauvegarder dans `automations/cumulus/` par ex

3. **Via Interface** :
   - Automatisation → Créer une automatisation
   - Ajouter les conditions/actions manuellement

### Exemples essentiels à ajouter

Au minimum :

```yaml
automation:
  - alias: Cumulus Solar Activation
    trigger:
      platform: state
      entity_id: switch.cumulus_control
      to: 'on'
    condition:
      - condition: template
        value_template: "{{ 'solar' in state_attr('switch.cumulus_control', 'reason') }}"
    action:
      - service: notify.mobile_app_votre_telephone
        data:
          title: ☀️ Cumulus Solaire Activé
          message: "Puissance: {{ states('sensor.cumulus_solar_power') }}W"
```

---

## 7️⃣ Vérification et Debugging

### Vérifier que tout fonctionne

1. **États et attributs** :
   - Outils développement → États
   - Chercher `switch.cumulus_control`
   - Vérifier les attributs

2. **Logs** :
   ```yaml
   # configuration.yaml
   logger:
     logs:
       custom_components.solar_cumulus_optimizer: debug
   ```
   - Redémarrer
   - Chercher "Solar Cumulus" dans les logs

3. **Activer manuellement** :
   - Cliquer sur le switch du dashboard
   - Vérifier que le relais s'active

### Troubleshooting

**Entités manquantes** :
```yaml
# Vérifier dans Outils > États
- Tous les capteurs existent ?
- Leurs valeurs ont du sens ?
```

**Relais ne s'active pas** :
- Vérifier que `switch.cumulus_relay` existe
- Essayer de l'activer manuellement
- Vérifier les permissions

**Puissance solaire nulle** :
- Vérifier l'inverseur/source de données
- Tester en mode manuel
- Vérifier les logs InfluxDB/MQTT

---

## 8️⃣ Optimisation Fine-tuning

### Ajuster les seuils

**Pour maximiser production solaire** :
- Baisser "Puissance solaire minimale" (ex: 300W)
- Baisser "Seuil de nuages" (ex: 20%)

**Pour réduire coûts HC** :
- Augmenter "Seuil température nuit" (ex: 8°C)
- Désactiver HC si mauvais temps rarement

**Pour économies** :
- Augmenter "Puissance minimale" (ex: 800W)
- Augmenter "Durée minimale" (ex: 180 min)

### Monitoring des coûts

```yaml
# Ajouter un helper template pour coûts
template:
  - sensor:
      - name: "Cumulus Daily Cost"
        unique_id: cumulus_daily_cost
        unit_of_measurement: "€"
        state: >
          {% set hc_runtime = states('sensor.cumulus_daily_hc_runtime') | int(0) %}
          {% set hc_hours = hc_runtime / 3600 %}
          {% set hc_price_kwh = 0.15 %}
          {% set kwh = 2.0 %}
          {{ (hc_hours * kwh * hc_price_kwh / 1000) | round(2) }}
```

---

## 9️⃣ Support et Contribution

### Signaler un bug
```
GitHub Issues :
- Description précise du problème
- Logs pertinents (en debug mode)
- Configuration utilisée
```

### Contribuer
```bash
# Fork du repo
git checkout -b feature/my-improvement
git commit -m "Add amazing feature"
git push origin feature/my-improvement
# Créer une Pull Request
```

---

## 🔟 Checklist Final

- [ ] Toutes les entités existent et ont des valeurs
- [ ] Intégration créée sans erreurs
- [ ] Switch cumulus accessible
- [ ] Dashboard importé
- [ ] Au moins 1 automation configurée
- [ ] Logs en debug consultables
- [ ] Relais s'active manuellement
- [ ] Production solaire détectée
- [ ] Tests en conditions réelles (ensoleillé, nuageux, nuit)

---

**🎉 Bravo ! Votre optimisation solaire est prête !**

Pour les questions :
- Consulter la documentation : https://github.com/votre-user/solar-cumulus-optimizer/wiki
- Ouvrir une issue GitHub
- Chercher dans les discussions existantes
