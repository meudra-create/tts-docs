---
name: renommage-google
description: Renomme les fichiers Google (Docs, Sheets, Slides) dont le titre est vague, tronqué ou générique, dans tous les emplacements de Google Drive (Mon Drive, sous-dossiers, Drives partagés, partagés avec moi), en déduisant le nouveau titre du contenu. À utiliser quand l'utilisateur demande de renommer, nettoyer ou corriger les titres de fichiers Google Docs/Drive, éventuellement depuis une date donnée.
---

# Renommage de fichiers Google

## 1. Cadrer
- Période : celle donnée par l'utilisateur (ex. « depuis octobre » → `modifiedTime > 'AAAA-10-01T00:00:00Z'`). Sans période, demander.
- Types : Docs par défaut (`mimeType = 'application/vnd.google-apps.document'`), ajouter Sheets/Slides si demandé.
- Ne pas poser d'autres questions : appliquer les règles ci-dessous.

## 2. Lister dans tous les emplacements
Utiliser Drive `search_files` avec `orderBy: modifiedTime desc`, `pageSize: 50`, `excludeContentSnippets: true`, et suivre `nextPageToken` jusqu'à épuisement (les pages peuvent se répéter, dédoublonner par id). Couvrir :
- fichiers dont `owner = 'me'` (tous dossiers confondus, y compris sous-dossiers) ;
- `sharedWithMe = true` ;
- Drives partagés (`list_shared_drives`, puis recherche dans chacun).

Les gros résultats sont sauvegardés dans un fichier : extraire `id`, `createdTime`, `title`, `parentId`, `capabilities.canEdit` avec `jq`, sans relire le JSON entier.

## 3. Repérer les titres à renommer
Vagues ou tronqués : « Document sans titre », « https---www », « https---youtu », « Aller au contenu », « Se connecter », « S'abonner », 1 à 3 mots génériques (« Amb », « 26 mars », « Larry C »), salutations (« Bonjour à toutes et à tous », « Welcome back »), phrase coupée en plein milieu, début de transcription brut, titre de page web parasite.

À laisser tel quel : titres complets et descriptifs, séries numérotées (« 93 – La diplomatie du carnet de chèques »).

## 4. Déduire le titre du contenu
- Lire chaque document avec `read_file_content` (déléguer à un sous-agent si plus de ~10 fichiers ; il ne fait que lire et renvoie un tableau `id | titre actuel | titre proposé | base`).
- Format : français, 80 caractères maximum, sans guillemets ni point final. Schéma conseillé : `Source ou intervenant – Sujet (date)`.
- Ne jamais inventer : date, nom ou chiffre uniquement s'ils figurent dans le document.
- Si deux documents ont le même contenu, ajouter « (copie) » au second.

## 5. Renommer
- Drive `update_file` avec `fileId` et `title` seulement. Le lien du fichier reste identique.
- Lancer les appels en parallèle, par lots.
- Ne pas renommer et ne pas supprimer : documents vides, documents personnels sensibles (courrier, dossier administratif), liens seuls sans contenu, titres dont le contenu est introuvable.
- Ne jamais mettre un fichier à la corbeille.

## 6. Rapport (court)
- Nombre de fichiers renommés.
- Liste des fichiers non renommés avec la raison.
- Rien d'autre.
