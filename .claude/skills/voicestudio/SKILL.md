---
name: voicestudio
description: Générer de la voix (TTS), transcrire de l'audio et automatiser doublage ou narration avec VoiceStudio via son API REST ou son serveur MCP. À utiliser quand l'utilisateur veut travailler avec VoiceStudio ou le connecter à un agent ou une automatisation.
---

# VoiceStudio

Utiliser le backend VoiceStudio de l'utilisateur. Privilégier le traitement local ; traduction cloud, téléchargement de modèles et connexions distantes nécessitent son accord explicite.

Installation locale : `/home/user/VoiceStudio` (dépendances installées avec `bun install` et `uv sync`).

## Connexion et découverte

Backend par défaut : `http://localhost:3900` (respecter l'adresse configurée par l'utilisateur).

1. Vérifier `GET /health`.
2. Découvrir les contrats avec `GET /openapi.json` et les voix/moteurs avec `GET /v1/audio/voices`. Ne jamais inventer d'ID de profil ni déduire les modèles installés d'un catalogue.
3. Si le backend est indisponible : lancer l'app installée, ou depuis les sources `bun install`, `bun run setup:api`, puis `bun run dev` à la racine du dépôt. Ne pas installer un second backend ni écraser un checkout existant.
4. Une réponse 401/403 est une erreur d'authentification : ne pas désactiver l'auth, ne jamais afficher de jeton.

## Générer de la voix

Écrire `speech-request.json` (remplacer `voice` par un ID de profil découvert si l'utilisateur en a choisi un) :

```json
{"model":"tts-1","voice":"alloy","input":"Texte à dire.","response_format":"wav"}
```

```sh
curl --fail-with-body --show-error http://localhost:3900/v1/audio/speech \
  -H 'Content-Type: application/json' --data-binary @speech-request.json \
  --output speech.wav
```

- `tts-1` / `tts-1-hd` sont des alias, pas des garanties de qualité ; les noms de voix OpenAI sont des alias de compatibilité.
- Préférer une voix enregistrée pour une narration répétable.
- Vérifier le statut HTTP et sonder le fichier (durée, format) avant de le déclarer valide : une erreur peut être écrite dans le fichier de sortie. Ne jamais annoncer un succès non vérifié.

## Transcrire

```sh
curl --fail-with-body --show-error http://localhost:3900/v1/audio/transcriptions \
  -F file=@clip.wav -F model=whisper-1 -F response_format=verbose_json
```

`json`/`text` pour le texte, `verbose_json` pour les timestamps, `srt`/`vtt` pour les sous-titres (selon le schéma). Vérifier qu'un modèle de transcription est installé ; sinon, demander l'autorisation de le télécharger.

## Clonage, design vocal, doublage, tâches longues

Utiliser l'OpenAPI du backend pour trouver les endpoints (profils, références, génération, doublage, jobs).

- Ne cloner que des voix que l'utilisateur est autorisé à utiliser ; conserver références et profils existants.
- Design vocal : noter ton, diction, langue, texte d'exemple ; vérifier le support du moteur.
- Doublage : conserver le média source, les locuteurs, le timing des segments et la musique/audio non vocal si demandé. Traduction terminée ≠ doublage rendu. Inspecter segments échoués et dépassements de durée avant export ; livrer un fichier séparé.
- Tâches asynchrones : suivre les IDs de job et statuts ; ne pas relancer aveuglément après un timeout.

## MCP et automatisation

Endpoint MCP : `http://localhost:3900/mcp` (transport HTTP, outils découverts à l'exécution). Clients stdio uniquement : voir https://github.com/debpalash/VoiceStudio/blob/main/docs/mcp.md. Depuis un conteneur (n8n, etc.), `localhost` désigne le conteneur : rendre le backend joignable.

## Erreurs

Lire le corps de la réponse et distinguer : backend indisponible, modèle manquant, capacité non supportée, authentification, matériel occupé. Corriger la cause signalée ; ne pas basculer vers un fournisseur hébergé ni télécharger un modèle sans autorisation.
