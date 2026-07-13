# 🤝 Contribuer

Les contributions sont les bienvenues ! Que ce soit des bugs, features, ou documentation.

## Signaler un Bug

1. Vérifier que le bug n'existe pas déjà
2. Créer une issue avec:
   - Description claire du problème
   - Étapes pour reproduire
   - Logs en mode debug
   - Version HA et version du composant
   - Configuration utilisée

## Proposer une Feature

1. Créer une issue de type "enhancement"
2. Décrire le cas d'usage
3. Expliquer comment cela améliore le composant

## Soumettre une PR

### Setup

```bash
git clone https://github.com/votre-fork/solar-cumulus-optimizer
cd solar-cumulus-optimizer
git checkout -b feature/ma-feature
```

### Code

- Respecter le style de code existant
- Ajouter des commentaires si complexe
- Tester les changements localement

### Commit

```bash
git add .
git commit -m "Add: Nouvelle feature" # ou Fix:, Docs:, etc
git push origin feature/ma-feature
```

### Pull Request

1. Créer la PR
2. Décrire les changements
3. Lier les issues si applicable

## Standards

- **Python**: PEP 8 + Black
- **Logs**: Utiliser logging.info/warning/error
- **Tests**: Tester les changements avant PR
- **Docs**: Mettre à jour README si nécessaire

## Merci ! 🙏

Chaque contribution aide à améliorer le projet pour tous.
