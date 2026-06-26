# CLAUDE.md — Projet « La paix, on peut l'éviter »

Mémoire permanente du projet. Lue automatiquement à chaque session.

## Nature du projet

Livre d'analyse géopolitique : **« La paix, on peut l'éviter »** — la domination
néocoloniale française en Afrique et la rupture des peuples du Sahel (AES :
Mali, Burkina Faso, Niger). Le dépôt est un site de docs Nuxt ; le manuscrit
vit en markdown dans `content/3.livre/`, et des scripts produisent un PDF et un
DOCX mis en page.

## Branche de travail

- Développer **uniquement** sur `claude/sharp-allen-tuhzel`.
- Ne jamais pousser sur une autre branche sans autorisation explicite.
- `git push -u origin claude/sharp-allen-tuhzel` (retry réseau avec backoff).

## Règle de production (impérative)

**Ne jamais compiler (PDF/DOCX), committer ou pousser sans l'autorisation
explicite de l'utilisateur.** Annoncer le travail fait, puis demander.

## Structure du manuscrit

- Chapitres : `content/3.livre/N.slug-descriptif.md` (N = ordre, slug sans accents).
- Frontmatter YAML obligatoire : `---\ntitle: '...'\n---`.
- Titres : `# ` chapitre (H1), `## ` section, `### ` sous-section.
- Nouveau chapitre → numéro le plus élevé existant + 1.
- Pages de partie (insérées par `build_pdf.py`, voir `PART_PAGES`) :
  - I (ch. 4) L'Afrique avant la domination
  - II (ch. 8) Comment la dépendance a été organisée
  - III (ch. 14) La guerre du Sahel
  - IV (ch. 19) La révolution de la souveraineté
  - V (ch. 25) Le réveil panafricain
  - VI (ch. 29) Les défis de demain

## Voix éditoriale

Engagée, percutante, analytique — lignée Fanon / Césaire / Sankara.
- Accroche choc ou citation en exergue (`>`) en ouverture de chapitre.
- Phrases courtes. Responsables nommés. Dommages chiffrés. Pas d'euphémisme.
- **Interdit** : toute phrase commençant par « Soyons honnêtes » ou formule de
  précaution oratoire équivalente — affirmer directement.
- Ne jamais supprimer un fait, une donnée ou une citation : enrichir, pas couper.
- Données comparatives → tableaux markdown `| col | col |`. Listes → `-`.
- Clore par une synthèse (« Ce que révèle… ») et une ligne de sources en italique.

## Identité visuelle (PDF + DOCX)

- Police : **FreeSerif** (Bold, Italic, Bold Italic).
- Palette : ardoise `#2C3A4A`, or `#A07820`, crème `#F4EFE4`,
  rouge sombre `#8B1A1A`, gris `#3C3C3C`.
- H1 → bandeau ardoise plein, titre blanc capitales, filet or dessous.
- Citations → barre or à gauche, italique rouge sombre.
- Tableaux → en-tête ardoise/blanc, lignes crème/gris, bordures 0,90 pt.

## Pipeline de build

- **PDF** : `python3 scripts/build_pdf.py` — compile tous les `[0-9]*.md` via
  XeLaTeX, insère les pages de partie, gère les tableaux pipe. Vérifier 0 erreur
  (`grep -c "^!"` dans le log). Sortie : `la-paix-on-peut-leviter.pdf`.
- **DOCX** : `python3 scripts/build_docx_full.py` — régénère le DOCX **complet**
  (1→N) depuis les sources réécrites, avec page de titre et tableaux pipe.
  Sortie : `la-paix-on-peut-leviter.docx`.
- **Ne pas** utiliser `scripts/append_chapters.py` pour le DOCX : il part d'une
  base figée (chapitres ≤ 39 obsolètes). Conservé pour référence seulement.

## Format des commits

Message en français décrivant le changement, terminé par :

```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016YUsTGkJ7s85TXfcngyaWu
```

## Skills du projet

- `/chapitre` (`.claude/skills/chapitre/`) : crée ou réécrit un chapitre à partir
  d'une source, applique tout ce qui précède automatiquement.
