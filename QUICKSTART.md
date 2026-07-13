# ⚡ Démarrage Rapide (5 minutes)

## 1️⃣ Installation

### Méthode A : HACS (Recommandé)
```
HACS → Intégrations
Menu (⋮) → Paramètres personnalisés
Ajouter:
  URL: https://github.com/votre-user/solar-cumulus-optimizer
  Type: Integration
  Branche: main
  
Chercher "Solar Cumulus Optimizer" → Installer → Redémarrer
```

### Méthode B : Manuel
```bash
mkdir -p ~/.homeassistant/custom_components/
git clone https://github.com/votre-user/solar-cumulus-optimizer \
  ~/.homeassistant/custom_components/solar_cumulus_optimizer
# Redémarrer Home Assistant
```

## 2️⃣ Configuration

1. **Paramètres → Appareils et services → Créer intégration**
2. **Chercher "Solar Cumulus Optimizer"**
3. **Remplir les entités requises:**
   - Puissance solaire: `sensor.solar_power_now`
   - Relais: `switch.cumulus_relay`
   - Météo: `weather.home`
   - Linky NTRAF: `sensor.linky_ntraf`
   - Linky SINTI: `sensor.linky_sinti`

4. **Configurer les options** (après création)

## 3️⃣ Dashboard

Copier le contenu de `examples/solar-cumulus-dashboard.yaml` dans un nouveau dashboard.

## 4️⃣ Automations

Ajouter vos automations depuis `examples/solar-cumulus-automations-examples.yaml`

---

**C'est tout ! 🎉**

Pour plus de détails → Lire **INTEGRATION_GUIDE.md**
