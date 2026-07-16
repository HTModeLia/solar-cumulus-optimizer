# 🎮 SERVICE DE FORÇAGE MANUEL - Solar Cumulus Optimizer
## Pour HTModeLia - Home Assistant 2026.7+

---

## 📌 RÉSUMÉ

**Nouveau Service**: `force_manual_heating`

**But**: Forcer la marche du cumulus à la demande, soit constamment soit pour une durée spécifique (2h, 1h, 30m, 15m)

**Utilité**: 
- Forcer la marche quand vous le désirez
- Marche constante pour chauffage complet
- Marche temporaire automatiquement limitée
- Redémarrage auto après durée

---

## 🎯 OPTIONS DISPONIBLES

### Durée constante
```yaml
service: solar_cumulus_optimizer.force_manual_heating
data:
  duration: "constant"  # Marche continue, pas d'arrêt auto
  notify: true
  auto_disable: true
```

**Résultat**: Cumulus marche indéfiniment jusqu'à arrêt manuel

---

### Durée 2 heures
```yaml
service: solar_cumulus_optimizer.force_manual_heating
data:
  duration: "2h"        # Arrêt auto après 2 heures
  notify: true
  auto_disable: true
```

**Résultat**: Cumulus marche 2h, puis s'arrête automatiquement

---

### Autres durées disponibles
```yaml
duration: "1h"   # 1 heure
duration: "30m"  # 30 minutes
duration: "15m"  # 15 minutes
```

---

## 🎨 DASHBOARD LOVELACE - BOUTONS RAPIDES

**Boutons pour forcer le cumulus**:

```yaml
type: vertical-stack
cards:
  - type: heading
    heading: 🎮 Forçage Manuel Cumulus

  - type: grid
    columns: 2
    cards:
      # Bouton: Marche Constante
      - type: button
        name: "⏸️ Marche Constante"
        icon: mdi:power
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.force_manual_heating
          data:
            duration: "constant"
            notify: true
            auto_disable: true

      # Bouton: Marche 2 Heures
      - type: button
        name: "⏱️ Marche 2h"
        icon: mdi:timer
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.force_manual_heating
          data:
            duration: "2h"
            notify: true
            auto_disable: true

  - type: grid
    columns: 2
    cards:
      # Bouton: Marche 1 Heure
      - type: button
        name: "⏱️ Marche 1h"
        icon: mdi:timer-outline
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.force_manual_heating
          data:
            duration: "1h"
            notify: true
            auto_disable: true

      # Bouton: Marche 30 Minutes
      - type: button
        name: "⏱️ Marche 30m"
        icon: mdi:timer-sand-empty
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.force_manual_heating
          data:
            duration: "30m"
            notify: true
            auto_disable: true

  - type: grid
    columns: 2
    cards:
      # Bouton: Marche 15 Minutes
      - type: button
        name: "⏱️ Marche 15m"
        icon: mdi:timer-sand-empty
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.force_manual_heating
          data:
            duration: "15m"
            notify: true
            auto_disable: true

      # Bouton: Arrêt
      - type: button
        name: "❌ Arrêt"
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: solar_cumulus_optimizer.deactivate_heating
          data:
            notify: true
```

---

## 📲 UTILISATION

### Via le Dashboard
1. **Aller dans le dashboard Cumulus**
2. **Cliquer sur un des boutons**:
   - ⏸️ Marche Constante → Marche continue
   - ⏱️ Marche 2h → Arrêt auto après 2h
   - ⏱️ Marche 1h → Arrêt auto après 1h
   - ⏱️ Marche 30m → Arrêt auto après 30 min
   - ⏱️ Marche 15m → Arrêt auto après 15 min
   - ❌ Arrêt → Arrêt immédiat

### Via une Automation
```yaml
automation:
  - alias: "Cumulus - Forçage Manuel Planifié"
    trigger:
      platform: time
      at: "10:00:00"  # 10h du matin
    action:
      - service: solar_cumulus_optimizer.force_manual_heating
        data:
          duration: "2h"  # Forcer pendant 2h
          notify: true
          auto_disable: true
```

### Via Script
```yaml
script:
  cumulus_force_2h:
    alias: "Forcer Cumulus 2h"
    sequence:
      - service: solar_cumulus_optimizer.force_manual_heating
        data:
          duration: "2h"
          notify: true
          auto_disable: true
```

### Via Appel Direct Service
```bash
# Ligne de commande
curl -X POST http://homeassistant:8123/api/services/solar_cumulus_optimizer/force_manual_heating \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "duration": "2h",
    "notify": true,
    "auto_disable": true
  }'
```

---

## 📊 PARAMÈTRES DÉTAILLÉS

### `duration` (Requis)
**Options**:
- `"constant"` → Marche continue
- `"2h"` → 2 heures
- `"1h"` → 1 heure
- `"30m"` → 30 minutes
- `"15m"` → 15 minutes

### `notify` (Optionnel, défaut: true)
**Options**:
- `true` → Envoyer notification persistante
- `false` → Pas de notification

### `auto_disable` (Optionnel, défaut: true)
**Options**:
- `true` → Arrêt automatique après durée
- `false` → Pas d'arrêt auto (durée ignorée)

---

## 🔔 NOTIFICATIONS

**Quand le cumulus est forcé**:
```
Titre: 🎮 FORÇAGE MANUEL - Cumulus Solaire
Message: Cumulus FORCÉ en marche pour: 2 HEURES
```

**Quand le timer s'écoule**:
```
Titre: ⏰ Cumulus Solaire
Message: Forçage manuel terminé (2 HEURES)
```

---

## 💡 CAS D'USAGE

### 1. Vous avez peu d'eau chaude → Forçage constant
```yaml
duration: "constant"  # Marche jusqu'à arrêt manuel
```

### 2. Vous voulez un bain d'eau chaude → Forçage 2h
```yaml
duration: "2h"  # Arrêt auto après 2h
```

### 3. Chauffage rapide avant visite → Forçage 30m
```yaml
duration: "30m"  # Chauffage rapide
```

### 4. Préparation matin → Forçage 1h
```yaml
duration: "1h"  # Préparation avant lever
```

---

## ⚙️ CONFIGURATION COMPLÈTE

### 1. Remplacer `__init__.py`
```bash
# Télécharger INIT_WITH_MANUAL_FORCE.py
# Renommer en __init__.py
# Copier dans ~/.homeassistant/custom_components/solar_cumulus_optimizer/

cp INIT_WITH_MANUAL_FORCE.py ~/.homeassistant/custom_components/solar_cumulus_optimizer/__init__.py
```

### 2. Redémarrer Home Assistant
```
Paramètres → Système → Redémarrer
```

### 3. Vérifier le service
```
Paramètres → Outils → Développeur → Services
Chercher: solar_cumulus_optimizer.force_manual_heating
```

---

## 🔍 LOGS ET DÉBUGAGE

**Voir les logs du service**:
```
Configuration → Outils → Logs
Chercher: "solar_cumulus_optimizer"
Chercher: "Forçage manuel"
```

**Logs attendus**:
```
✓ Forçage manuel activé: 2 HEURES
✓ Timer de désactivation planifié pour 2 HEURES
✓ Forçage manuel expiré après 2 HEURES
```

---

## ✅ CHECKLIST

Avant d'utiliser:

- [ ] Fichier `INIT_WITH_MANUAL_FORCE.py` téléchargé
- [ ] Copié en `__init__.py` dans custom_components/
- [ ] HA redémarré
- [ ] Service visible dans Développeur → Services
- [ ] Boutons du dashboard créés (optionnel)
- [ ] Test d'un bouton effectué
- [ ] Notification reçue

---

## 🆘 DÉPANNAGE

### Le service n'apparaît pas

**Solution**:
1. Redémarrer HA
2. Attendre 30 secondes
3. Rafraîchir page (F5)
4. Vérifier logs pour erreurs

### Le timer n'arrête pas le cumulus

**Solution**:
1. Vérifier `auto_disable: true` dans les données
2. Vérifier logs pour erreurs
3. Arrêt manuel si nécessaire

### Notification ne s'affiche pas

**Solution**:
1. Vérifier `notify: true`
2. Vérifier que persistent_notification est actif
3. Vérifier logs

---

## 🎯 RÉSUMÉ POUR HTMODELLIA

**Vous avez maintenant**:
✅ Service pour forcer le cumulus à la demande
✅ Marche constante (indéfinie)
✅ Marche temporaire (2h, 1h, 30m, 15m)
✅ Arrêt automatique après durée
✅ Notifications à chaque action
✅ Boutons rapides dans le dashboard
✅ Compatible HA 2026.7+

**À retenir**:
- Durée "constant" = marche continue
- Durée "2h" = arrêt auto après 2h
- Les boutons sont instantanés
- Les notifications vous informent

---

## 📚 FICHIERS ASSOCIÉS

- `INIT_WITH_MANUAL_FORCE.py` → Code à installer
- `SERVICES_GUIDE.md` → Guide complet des services
- `AUTOMATIONS_EXEMPLE.yaml` → Exemples automations

---

## 🚀 PRÊT À UTILISER!

Téléchargez `INIT_WITH_MANUAL_FORCE.py` et installez!

**Temps**: 5 minutes  
**Difficulté**: Facile  
**Bénéfice**: Contrôle total du cumulus  

Bon courage, HTModeLia! 💪

---

**Version**: 1.0.2 (Forçage manuel)  
**HA Minimum**: 2024.1  
**HA Testé**: 2026.7  
**Username**: HTModeLia  
**Date**: 2024-07-14  
