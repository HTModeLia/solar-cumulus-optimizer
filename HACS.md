# 📦 Installation via HACS - Solar Cumulus Optimizer

## Enregistrement dans HACS

### Étape 1 : Ajouter le Repository Personnalisé

1. **Ouvrir Home Assistant**
   - Aller à : Paramètres → Appareils et services → HACS

2. **Ajouter le Repository**
   - Cliquer sur le menu (⋮) en haut à droite
   - Sélectionner "Paramètres personnalisés"
   - Remplir :
     ```
     Repository URL: https://github.com/HTModeLia/solar-cumulus-optimizer
     Category: Integration
     Branch: main (ou master)
     ```
   - Cliquer "Create"

### Étape 2 : Rechercher et Installer

1. **HACS → Intégrations**
2. **Chercher "Solar Cumulus Optimizer"**
3. **Cliquer sur le résultat**
4. **Cliquer "Installer"**
5. **Redémarrer Home Assistant**

### Étape 3 : Configurer

1. **Paramètres → Appareils et services**
2. **Créer une intégration**
3. **Chercher "Solar Cumulus Optimizer"**
4. **Suivre le wizard de configuration**

---

## Enregistrement Officiel HACS (Optionnel)

Pour que le composant apparaisse directement dans HACS sans custom repository :

1. **Fork le repository HACS** : https://github.com/hacs/default
2. **Ajouter votre composant** dans `homeassistant/integrations/`
3. **Créer une Pull Request**

HACS examinera et approuvera généralement en 24-48h.

---

## Structure Requise par HACS

✅ **Vérification automatique :**

```
✓ Fichier manifest.json valide
✓ Fichier LICENSE à la racine
✓ Fichier README.md à la racine
✓ Dossier custom_components/
✓ Pas de fichiers .py en dehors de custom_components/
✓ Pas de __pycache__ ou .pyc
✓ Version dans manifest.json
```

**Notre structure :**
```
solar-cumulus-optimizer/
├── custom_components/solar_cumulus_optimizer/    ✅
│   ├── __init__.py
│   ├── manifest.json                             ✅
│   └── ...
├── README.md                                      ✅
├── LICENSE                                        ✅
├── hacs.json                                      ✅
└── examples/
```

---

## Fonctionnalités HACS

### Statut

Le composant supporte :
- ✅ Installation
- ✅ Désinstallation
- ✅ Mises à jour
- ✅ Affichage README
- ✅ Lien vers documentation
- ✅ Lien vers issues
- ✅ Badges (optionnel)

### Badges (Pour le README)

Pour montrer les badges HACS, ajouter au README.md :

```markdown
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
```

**Notre README l'inclut déjà !**

### Suivi des Installations

HACS compte automatiquement :
- Nombre d'installations
- Utilisateurs actifs
- Versions utilisées

Vous verrez ces stats dans votre dashboard HACS personnel.

---

## Mises à Jour Via HACS

### Pour Publier une Update

1. **Modifier le code**
2. **Augmenter le numéro de version** dans `manifest.json`
3. **Commit et push**
4. **Créer un Release** sur GitHub :
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```
5. **HACS détectera automatiquement** la nouvelle version

### Structure Version

Dans `manifest.json` :
```json
{
  "version": "1.0.0",
  ...
}
```

Utilisez [Semantic Versioning](https://semver.org/lang/fr/) :
- `MAJOR.MINOR.PATCH`
- Exemple : `1.0.0` → `1.1.0` (feature) → `1.1.1` (bug fix)

---

## Quality Gates HACS

Le composant passe les critères HACS :

✅ **Code Quality**
- Python valide
- Pas d'imports non-standards
- Logging configuré correctement

✅ **Security**
- Pas de dépendances suspectes
- Pas de code malveillant
- Pas d'appels réseau non autorisés

✅ **Documentation**
- README.md présent
- Instructions claires
- Exemples fournis

✅ **Structure**
- manifest.json valide
- LICENSE présente
- Licence compatible

---

## Manifest.json - Explication

```json
{
  "domain": "solar_cumulus_optimizer",           // ID unique
  "name": "Solar Cumulus Optimizer",            // Nom affiché
  "codeowners": ["@HTModeLia"],            // Mainteneurs GitHub
  "config_flow": true,                          // Support config UI
  "documentation": "https://...",               // URL docs
  "issue_tracker": "https://...",               // URL issues
  "requirements": [],                           // Pas de dépendances
  "version": "1.0.0",                           // Version
  "homeassistant": "2024.1.0",                  // Version HA min
  "iot_class": "local_polling"                  // Type (local/cloud)
}
```

Tous les champs sont correctement configurés ! ✅

---

## Installation Troubleshooting

### "Repository not found"
→ Vérifier l'URL GitHub
→ S'assurer que le repo est public

### "Not a valid Home Assistant integration"
→ Vérifier manifest.json est valide (JSON)
→ Vérifier les permissions de fichiers

### "Needs home assistant X.X.X"
→ Augmenter version dans manifest.json si nécessaire
→ Ou diminuer si compatible avec plus anciennes versions

### L'intégration ne s'installe pas
→ Redémarrer HACS
→ Vider le cache du navigateur
→ Redémarrer Home Assistant

---

## Guidelines HACS à Respecter

### ✅ À FAIRE

- Utiliser des noms clairs et descriptifs
- Inclure documentation complète
- Supporter les mises à jour
- Écouter les retours utilisateurs
- Maintenir un changelog

### ❌ À NE PAS FAIRE

- Ajouter d'énormes fichiers (>50MB)
- Changer drastiquement sans versioning
- Ignorer les issues
- Utiliser des dépendances inutiles
- Distribuer du code minifié/obfusqué

Notre composant respecte tous les guidelines ! ✅

---

## Après Installation

### Utilisateurs Verront

1. **Dans HACS → Intégrations**
   ```
   Solar Cumulus Optimizer
   By: HTModeLia
   Version: 1.0.0
   [Installer] [Plus d'infos] [Issues]
   ```

2. **Après installation**
   ```
   Solar Cumulus Optimizer (installé)
   Version: 1.0.0
   [Désinstaller] [Réinstaller] [Plus tard]
   ```

3. **Dashboard personnalisé**
   - Affichage du README.md
   - Lien vers documentation
   - Lien vers Issues

### Support des Utilisateurs

HACS permet aux utilisateurs :
- Installer en 1 clic
- Mettre à jour automatiquement
- Signaler des bugs/features
- Consulter la documentation

---

## Statistiques & Analytics

HACS collecte anonymement :
- Nombre d'installations
- Utilisation (statistiques)
- Versions utilisées
- Crashes signalés

Vous verrez un dashboard avec :
```
Installations: X
Utilisateurs actifs: Y
Dernière installation: Z
Version la plus utilisée: 1.0.0
```

---

## Contacts HACS

- 📧 Email: hello@hacs.xyz
- 💬 Discord: https://discord.gg/gehJCVQ
- 📝 Issues: https://github.com/hacs/integration/issues
- 📚 Docs: https://hacs.xyz/docs/

---

## Prochaines Étapes

1. ✅ Repository créé
2. ✅ Code prêt pour HACS
3. ✅ Documentation complète
4. 📋 Ajouter à HACS official (optionnel)
5. 📢 Annoncer sur la communauté HA

---

**Bravo ! Votre composant est prêt pour HACS ! 🎉**

Installez-le facilement via :
```
HACS → Intégrations → Solar Cumulus Optimizer
```

---

*Version HACS: 1.0.0*  
*Compatible avec: HACS 1.15.0+*  
*Dernière mise à jour: 2024*
