---
name: chapitre
description: >
  Crée ou réécrit un chapitre du livre « La paix, on peut l'éviter » à partir
  d'une source (fichier texte, PDF, transcription, lien). Applique la voix
  éditoriale établie, la structure markdown du livre, la numérotation
  automatique, puis propose la compilation PDF/DOCX et le commit. À utiliser
  chaque fois que l'utilisateur dit « crée un chapitre », « ajoute un
  chapitre », « réécris ce chapitre » ou fournit une source à intégrer au livre.
---

# Skill : `/chapitre`

Tu produis un chapitre du livre **« La paix, on peut l'éviter »** — une analyse
géopolitique de la domination néocoloniale française en Afrique et de la
résistance des peuples du Sahel (AES : Mali, Burkina Faso, Niger).

L'objectif de cette skill : éviter à l'utilisateur de réexpliquer dix fois les
mêmes consignes. Tout ce qu'il doit fournir, c'est **la source** (un fichier, un
PDF, une transcription) et éventuellement le sujet. Le reste est automatique.

## Étape 1 — Lire la source

- Lis intégralement la source fournie (`Read` ; pour un gros fichier, lis-le par
  pages jusqu'au bout — ne réponds jamais à partir d'un extrait partiel).
- Identifie les faits, dates, chiffres, citations et noms propres. **Aucun fait
  ne doit être perdu** : on enrichit, on ne coupe pas.

## Étape 2 — Déterminer le numéro et le nom de fichier

- Les chapitres vivent dans `content/3.livre/`, nommés `N.slug-descriptif.md`.
- Pour un **nouveau** chapitre : prends le numéro le plus élevé existant + 1.
  Vérifie avec `ls content/3.livre/ | sort -t. -k1 -n | tail -3`.
- Slug : minuscules, mots-clés du sujet séparés par des tirets, sans accents
  (ex. `67.chapitre-mali-nouvelle-offensive.md`).
- Pour une **réécriture** : garde le fichier existant, écrase-le.

## Étape 3 — Écrire dans la voix du livre

**Voix** : engagée, percutante, analytique — dans la lignée de Frantz Fanon,
Aimé Césaire et Thomas Sankara.

Règles de style (non négociables) :

- Frontmatter YAML en tête : `---\ntitle: '...'\n---`.
- Titre de chapitre en `# ` (H1), sections en `## `, sous-sections en `### `.
- **Ouvre par une accroche choc** ou une citation-clé mise en exergue avec `>`.
- Phrases courtes, frappantes. Paragraphes denses mais respirants.
- **Nomme les responsables**, **chiffre les dommages**, dénonce sans euphémisme
  mais toujours appuyé sur des faits.
- Transitions soignées entre sections : chaque fin de section ouvre la suivante.
- **Interdiction absolue** : aucune phrase commençant par « Soyons honnêtes »
  ou toute formule de précaution oratoire équivalente. Affirme directement.
- Données comparatives → **tableaux markdown** `| col | col |` (rendus en
  ardoise/crème par les builders). Listes → puces `-`.
- Termine par une section de synthèse (« Ce que révèle… » / « La leçon… ») et
  une ligne de sources en italique.

## Étape 4 — Proposer la production (ne pas compiler sans accord)

Une fois le `.md` écrit, **annonce-le et demande l'autorisation** avant de
compiler ou committer. L'utilisateur a posé comme règle : *« démarrer la
production qu'après mon autorisation »*. Propose :

> Le chapitre N est créé. Je compile le PDF + DOCX et je commite ?

Si l'utilisateur autorise :

1. **PDF** : `python3 scripts/build_pdf.py` (background). Vérifie 0 erreur
   (`grep -c "^!"` dans le log) et la taille finale.
2. **DOCX** : `python3 scripts/build_docx_full.py` (régénère tout depuis les
   sources, gère les tableaux pipe).
3. **Commit + push** sur la branche `claude/sharp-allen-tuhzel` :
   - message clair en français décrivant le chapitre ajouté/réécrit ;
   - terminer par les lignes Co-Authored-By / Claude-Session habituelles ;
   - `git push -u origin claude/sharp-allen-tuhzel` (retry réseau si besoin).
4. **Livrer** le ou les fichiers produits avec `SendUserFile`.

## Conventions techniques du projet (mémo)

- Police : **FreeSerif**. Palette : ardoise `#2C3A4A`, or `#A07820`, crème
  `#F4EFE4`, rouge sombre `#8B1A1A`, gris `#3C3C3C`.
- H1 → bandeau ardoise plein, titre blanc capitales, filet or dessous.
- Citations `>` → barre or à gauche, italique rouge sombre.
- Tableaux → en-tête ardoise/blanc, lignes crème/gris, bordures 0,90 pt.
- `build_pdf.py` compile **tous** les chapitres `[0-9]*.md` via XeLaTeX.
- `build_docx_full.py` régénère le DOCX complet (1→N) avec page de titre.
- Ne jamais partir de l'ancien `append_chapters.py` (base figée) pour le DOCX.

## Ce que l'utilisateur n'a PAS à répéter

Le style, la structure, la palette, la numérotation, le pipeline de build, la
branche git, le format des commits, la suppression des avertissements. Tout est
ici. Il fournit la source — tu fais le reste.
