# 🚀 Guide HACS - Solar Cumulus Optimizer

## Qu'est-ce que HACS ?

**HACS** (Home Assistant Community Store) est un gestionnaire de composants personnalisés pour Home Assistant.
Il simplifie l'installation, la mise à jour et la gestion des extensions communautaires.

---

## ✅ Checklist HACS (pour mainteneurs)

### Repository GitHub
- [x] Repository public
- [x] README.md à la racine
- [x] LICENSE (MIT, Apache, etc.)
- [x] Fichier manifest.json valide
- [x] Composant dans `custom_components/`
- [x] .gitignore correctement configuré
- [x] hacs.json à la racine

### Configuration
- [x] hacs.json avec champs complets
- [x] manifest.json avec tous les champs requis
- [x] Documentation complète
- [x] Issues et discussions activées
- [x] Badges GitHub
- [x] Workflows CI/CD

### Qualité du Code
- [x] Python valide (pas d'erreurs de syntaxe)
- [x] Pas de dépendances externes
- [x] Logging avec format approprié
- [x] Code commenté
- [x] Pas de hardcoding

---

## 🔧 Configuration Requise

### Fichiers HACS Essentiels

**hacs.json** (à la racine)
```json
{
  "name": "Solar Cumulus Optimizer",
  "hacs": "1.33.0",
  "domains": ["switch", "sensor"],
  "homeassistant": "2024.1.0",
  "documentation": "https://github.com/...",
  "requirements": [],
  "render_readme": true
}
```

**manifest.json** (dans custom_components/...)
```json
{
  "domain": "solar_cumulus_optimizer",
  "name": "Solar Cumulus Optimizer",
  "version": "1.0.0",
  "homeassistant": "2024.1.0",
  "config_flow": true,
  "documentation": "https://github.com/...",
  "requirements": []
}
```

### Fichiers Recommandés

- **README.md** - Documentation principale
- **LICENSE** - Licence MIT
- **.gitignore** - Fichiers à ignorer
- **CHANGELOG.md** - Historique des versions
- **CONTRIBUTING.md** - Guide de contribution
- **.github/workflows/** - Actions CI/CD

---

## 📝 Champs hacs.json Expliqués

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `name` | string | ✅ | Nom du composant |
| `domains` | array | ✅ | Domaines utilisés (switch, sensor, etc) |
| `homeassistant` | string | ✅ | Version HA minimale (ex: "2024.1.0") |
| `documentation` | string | ✅ | URL de documentation |
| `issues` | string | ❌ | URL des issues GitHub |
| `requirements` | array | ✅ | Dépendances Python |
| `render_readme` | bool | ❌ | Afficher README dans HACS (true) |
| `iot_class` | string | ❌ | "local_polling", "local_push", etc |
| `version` | string | ✅ | Version actuelle (semver) |
| `codeowners` | array | ✅ | Mainteneurs GitHub |
| `country` | array | ❌ | Pays cibles (["FR", "US"]) |
| `topics` | array | ❌ | Tags/sujets |

**Exemple complet:**
```json
{
  "name": "Solar Cumulus Optimizer",
  "hacs": "1.33.0",
  "domains": ["switch", "sensor", "binary_sensor"],
  "homeassistant": "2024.1.0",
  "documentation": "https://github.com/votre-user/solar-cumulus-optimizer",
  "issues": "https://github.com/votre-user/solar-cumulus-optimizer/issues",
  "requirements": [],
  "render_readme": true,
  "iot_class": "local_polling",
  "version": "1.0.0",
  "codeowners": ["@votre-user"],
  "country": ["FR"],
  "topics": ["solar", "cumulus", "optimization", "linky", "autoconsumption"]
}
```

---

## 🚀 Processus d'Installation via HACS

### Pour les Utilisateurs

1. **Ouvrir HACS dans Home Assistant**
   ```
   Home Assistant → HACS (dans barre latérale)
   ```

2. **Ajouter le Repository (si pas encore dans le store)**
   ```
   Trois points (⋮) → Paramètres personnalisés
   → Ajouter un repository personnalisé
   
   URL: https://github.com/votre-user/solar-cumulus-optimizer
   Type: Integration
   Branche: main
   
   → Créer
   ```

3. **Chercher et Installer**
   ```
   HACS → Intégrations
   → Chercher "Solar Cumulus Optimizer"
   → Cliquer sur le composant
   → Installer
   ```

4. **Redémarrer Home Assistant**
   ```
   Paramètres → Système → Redémarrer
   ```

5. **Configurer**
   ```
   Paramètres → Appareils et services
   → Créer une intégration
   → Chercher "Solar Cumulus Optimizer"
   ```

---

## 🔐 Sécurité des Données

HACS n'accède à aucune de vos données:
- ✅ Les configurations restent locales
- ✅ Aucune telémétrie envoyée
- ✅ Aucune connexion à des serveurs externes
- ✅ Vos entités Linky ne quittent pas votre HA

---

## 🐛 Dépannage HACS

### "Repository not found"
→ Vérifier l'URL du repository est correcte

### "Invalid manifest"
→ Vérifier `manifest.json` est un JSON valide
```bash
python -m json.tool custom_components/solar_cumulus_optimizer/manifest.json
```

### "Component not recognized"
→ S'assurer `domain` dans manifest.json correspond au dossier

### "Not showing in HACS"
→ Attendre 24-48h pour indexation HACS
→ OU pousser une nouvelle tag de release

---

## 📤 Soumettre à HACS

Optionnel: faire accepter le composant dans le store HACS officiel

1. **S'assurer tous les critères sont met:**
   - Repository public ✓
   - README.md ✓
   - LICENSE ✓
   - manifest.json valide ✓
   - Pas d'erreurs dans les logs ✓
   - Documentation complète ✓

2. **Créer une issue dans HACS**
   - Aller à https://github.com/hacs/integration
   - "New issue" → "New repository"
   - Remplir le formulaire

3. **Review Process**
   - HACS review le code
   - Peut prendre 1-2 semaines
   - Peut demander des modifications

4. **Acceptation**
   - Une fois accepté, visible dans le HACS store
   - Mise à jour automatique à chaque release

---

## 📦 Structure HACS Validée

```
solar-cumulus-optimizer/
├── custom_components/
│   └── solar_cumulus_optimizer/
│       ├── __init__.py ✓
│       ├── config_flow.py ✓
│       ├── coordinator.py ✓
│       ├── switch.py ✓
│       ├── sensor.py ✓
│       ├── manifest.json ✓
│       └── strings.json ✓
├── hacs.json ✓
├── README.md ✓
├── LICENSE ✓
├── CHANGELOG.md ✓
├── .gitignore ✓
├── examples/ ✓
└── .github/ ✓
```

---

## 🎯 Versions et Releases

### Créer une Release
```bash
# Tagger une version
git tag v1.0.1
git push origin v1.0.1

# HACS détecte le tag et le propose aux utilisateurs
```

### Mise à Jour
HACS notifie automatiquement les utilisateurs quand une nouvelle version est disponible.

### Versionning Sémantique
```
MAJOR.MINOR.PATCH
1.0.0
│ │ │
│ │ └─ Bugfixes (v1.0.1)
│ └───── Features (v1.1.0)
└─────── Breaking changes (v2.0.0)
```

---

## 📊 Statistiques HACS

Une fois accepté dans le store, HACS affiche:
- Nombre d'utilisateurs
- Téléchargements
- Étoiles GitHub
- Issues ouvertes
- Dernière mise à jour

---

## 💬 Support HACS

- **Documentation**: https://hacs.xyz/
- **Forum**: https://community.home-assistant.io
- **Issues HACS**: https://github.com/hacs/integration/issues
- **Discord**: HACS official channel

---

## ✅ Final Checklist Avant Publication

- [ ] Tester localement dans HA
- [ ] README.md complet et à jour
- [ ] manifest.json valide
- [ ] hacs.json complet
- [ ] Pas d'erreurs de logs
- [ ] Version dans manifest.json = version du code
- [ ] CHANGELOG.md à jour
- [ ] LICENSE incluse (MIT)
- [ ] .gitignore correct
- [ ] Badges dans README
- [ ] GitHub Actions valident le code
- [ ] Repository settings corrects:
  - [ ] Discussions activées
  - [ ] Issues activées
  - [ ] Wiki activé (optionnel)
  - [ ] Projects activés (optionnel)

---

**Prêt pour HACS ! 🚀**

Votre composant est maintenant configuré pour:
- ✅ Installation facile via HACS
- ✅ Mises à jour automatiques
- ✅ Visibilité dans le community store
- ✅ Support complet de la communauté

---

*Dernière mise à jour: 2024*
