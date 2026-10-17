# Instructions Claude Code — tts-docs

## Connexion Obsidian

Ce projet est connecté à un vault Obsidian via le serveur MCP `obsidian-vault` (transport REST API, port 27124).

### Prérequis (à faire une seule fois sur votre machine)

1. **Installer le plugin Obsidian** : dans Obsidian → Paramètres → Plugins tiers → chercher **Local REST API** → activer.
2. **Récupérer la clé API** : Paramètres → Local REST API → copier la clé.
3. **Définir la variable d'environnement** :
   ```bash
   export OBSIDIAN_API_KEY=votre-clé-ici
   ```
   Ajoutez cette ligne à votre `~/.zshrc` ou `~/.bashrc` pour la rendre permanente.
4. **Laisser Obsidian ouvert** avec le plugin actif avant de lancer Claude Code.

### Utilisation

Une fois connecté, utilisez ces commandes dans Claude Code :

| Commande | Action |
|---------|--------|
| `/wiki` | Vérification de l'état du vault, configuration initiale |
| `ingest [fichier]` | Ajouter un document source au vault |
| `que sais-tu sur X ?` | Interroger le vault avec citations |
| `lint the wiki` | Contrôle de santé du vault |

### Base de connaissances locale

Ce dépôt contient aussi une base de connaissances en Markdown dans `knowledge-base/`.
Consultez `knowledge-base/index.md` pour le sommaire.
Pour la mettre à jour : pointez Claude vers une source et dites « Mets à jour la base de connaissances ».
