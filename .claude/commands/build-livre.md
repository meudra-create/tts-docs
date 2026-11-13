# /build-livre — Générer le PDF du livre avec la date du jour

Génère `LIVRE-FINAL.pdf` depuis `LIVRE-FINAL.md` avec le thème **Ardoise & Or**.

## Étapes

1. Afficher la date du jour au format `JJ/MM/AAAA`
2. Lancer la génération :
   ```bash
   python3 manuscrit-edition/build_pdf.py
   ```
3. Copier le PDF daté dans `manuscrit-edition/exports/` :
   ```bash
   mkdir -p manuscrit-edition/exports
   cp manuscrit-edition/LIVRE-FINAL.pdf manuscrit-edition/exports/LIVRE-$(date +%Y-%m-%d).pdf
   ```
4. Afficher la taille du fichier généré et le chemin de l'export daté

## Thème appliqué

- Police corps : EB Garamond 11,5 pt
- Police titres : Crimson Text
- Couleurs : Ardoise `#2C3A4A` / Or satiné `#A07820` / Fond blanc
- Format KDP : 6 × 9 in, marges 0,80/0,60/0,80/0,90 in
- Numérotation : `— N —` en pied de page centré

## Notes

- Le PDF final est toujours écrasé dans `manuscrit-edition/LIVRE-FINAL.pdf`
- Le PDF daté dans `exports/` est conservé comme archive de version
- Ne pas committer automatiquement — attendre instruction explicite
