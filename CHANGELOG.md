# Changelog

## [0.0.14] - 2026-07-18

### 🧩 HACS
- ✅ Mise à jour de la préparation de version pour que l’icône HACS soit correctement prise en compte dans la publication
- 🖼️ Vérification de la présence des fichiers d’icône racine pour l’affichage dans HACS

## [0.0.12] - 2026-07-18

### ✨ Fonctionnalités
- 🧩 Dashboard natif, mixte et avancé disponibles pour Home Assistant 2026.7
- 🔄 Réconfiguration de l’intégration sans erreur 500
- ⚙️ Logiciel d’activation solaire/HC plus robuste

### 🐛 Corrections
- Correction de la logique d’activation solaire et HC
- Amélioration du flow de configuration
- Mise à jour des métadonnées de version

---

## [1.0.0] - 2024-01-15

### ✨ Fonctionnalités
- ☀️ Optimisation automatique recharge cumulus sur production solaire
- ⚡ Gestion intelligente des tarifs Linky (HC/HP)
- 🌤️ Intégration météo pour chauffage préemptif
- 🌡️ Détection nuages transitoires (historique 10 min)
- 📊 Statistiques temps réel (activations, durée, coûts)
- 🎛️ Configuration simple par UI (pas de YAML brut)
- 📱 Dashboard Lovelace professionnel (3 vues)
- 🤖 10+ automations d'exemple incluses
- 💾 Persistent state (survit aux redémarrages)

### 🐛 Corrections
- Gestion correcte du runtime minimum (2h)
- Détection d'hysteresis pour éviter oscillations
- Logging détaillé pour débugage
- Gestion des entités manquantes

### 📚 Documentation
- README complet avec cas d'usage
- Guide d'intégration pas-à-pas
- Architecture et logique expliquées
- Exemples d'automations

### 🔧 Technique
- Python 3.11+ compatible
- Home Assistant 2024.1.0+
- Zéro dépendances externes
- Coordinateur avec update interval configurable
- Support complet des options

---

## Roadmap

### v1.1.0 (À venir)
- [ ] Service pour reset stats quotidiennes
- [ ] Graphique historique étendu
- [ ] Alertes email/SMS
- [ ] Intégration calcul coûts exacts
- [ ] Export données InfluxDB

### v1.2.0 (À venir)
- [ ] Support plusieurs relais
- [ ] Prédiction IA consommation
- [ ] Planification optimisée pour la semaine
- [ ] API REST pour accès externe

---

Pour signaler des bugs ou proposer des features:
https://github.com/HTModeLia/solar-cumulus-optimizer/issues
