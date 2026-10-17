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

## Traduction anglaise

- Vit dans `content/4.the-book-en/`, numérotation `N.slug-en.md` en miroir
  exact de `content/3.livre/` (même N, même ordre, mêmes frontières de
  parties I à VI) — ne jamais désynchroniser la numérotation entre les deux.
- Traduction intégrale et fidèle : aucun fait, chiffre, date ou citation
  coupé (même règle qu'en français, cf. Voix éditoriale). Citations
  traduites en anglais avec attribution et date conservées.
- Toute modification de contenu (nouveau chapitre, enrichissement, correction)
  faite côté français doit être répercutée côté anglais, et réciproquement.

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
- H1 (chapitre) → bandeau ardoise **plein**, titre blanc capitales, filet or dessous.
- Citations → barre or à gauche, italique rouge sombre.
- Tableaux → en-tête ardoise/blanc, lignes crème/gris, bordures 0,90 pt.
- **Page de partie** (PARTIE I à VI) : **fond BLANC** (pas de remplissage) —
  label « PARTIE X » (ardoise, petit, lettres espacées) puis titre (ardoise,
  grand, MAJUSCULES, centré) puis un **filet or court (≈8cm), centré**, sous
  le titre. Bloc centré verticalement sur la page. **Ne jamais confondre avec
  le bandeau H1** (qui lui est fond ardoise plein + texte blanc) : c'est
  l'erreur commise et corrigée dans ce projet — vérifier visuellement (XML ou
  rendu) après toute modification de `add_part_page` / `\partpage`.

## Pipeline de build

- **PDF** : `python3 scripts/build_pdf.py` (FR) / `scripts/build_pdf_en.py`
  (EN) — compile tous les `[0-9]*.md` via XeLaTeX, insère les pages de
  partie, gère les tableaux pipe. Vérifier 0 erreur (`grep -c "^!"` dans le
  log). Sorties : `la-paix-on-peut-leviter.pdf` / `peace-we-can-avoid-it.pdf`.
- **DOCX** : `python3 scripts/build_docx_full.py` (FR) /
  `scripts/build_docx_full_en.py` (EN) — régénère le DOCX **complet** depuis
  les sources markdown, avec page de titre, sommaire (champ TOC natif Word
  limité aux H1 via `outlineLvl=0`), pages de partie et tableaux pipe. La
  mise en page DOCX doit rester **rigoureusement identique** à celle du PDF
  (mêmes couleurs, mêmes structures) — toute modification d'un des deux
  scripts de build doit être répercutée sur l'autre. Sorties :
  `la-paix-on-peut-leviter.docx` / `peace-we-can-avoid-it.docx`.
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
