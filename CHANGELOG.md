# Changelog

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
https://github.com/votre-user/solar-cumulus-optimizer/issues
