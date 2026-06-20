# /habillage — Règles de mise en forme du livre « La paix, on peut l'éviter »

Référence complète des décisions typographiques et visuelles appliquées au manuscrit.

## Thème Ardoise & Or

| Élément | Valeur |
|---|---|
| Police corps | EB Garamond 11,5 pt |
| Police titres | Crimson Text |
| Couleur ardoise | `#2C3A4A` |
| Couleur or | `#A07820` |
| Fond page | blanc `#FFFFFF` |
| Fond crème (encadrés) | `#F7F4EF` |
| Format | KDP 6 × 9 in |
| Marges | haut 0,80 / ext 0,60 / bas 0,80 / int 0,90 in |
| Numérotation | `— N —` pied de page centré |

## Séparateurs d'étoiles

- Forme correcte : `★★★` (sans espaces)
- Dans le script : `<div class="stars">★★★</div>`
- Le regex de détection accepte les formes espacées dans le .md : `^\s*★\s*★\s*★\s*$`

## Tableaux (encadrés)

### Marqueurs dans le .md
```
---ENCADRE---
**TITRE EN MAJUSCULES**
- Item 1
- Item 2
---FIN---
```

### Règles de titre
- Le titre est une ligne `**...**` seule (sans tiret `-`)
- Détection : ratio majuscules/lettres (pas les chiffres ni la ponctuation) > 50 %
- Exemple valide : `**BERLIN, 1884-1885**` (les chiffres sont exclus du calcul)
- Titre → entête bleue ardoise (`enc-th`)
- Sans titre → tableau sans entête

### Règles de contenu
- Items : commencent par `- ` (tiret espace)
- **Pas de gras** dans les items — écrire `- Label: texte` et non `- **Label**: texte`
- Le gras est réservé au titre uniquement

### Préfixe interdit
- Ne pas écrire `**ENCADRÉ — TITRE**` — supprimer le préfixe `ENCADRÉ — `
- Écrire directement `**TITRE**`

### CSS généré
```css
table.enc        → bordure ardoise, page-break-inside: avoid
.enc-th          → fond ardoise, texte blanc, Crimson Text 9,5 pt
.enc-td          → fond crème, padding 0,55em 1em
```

## Bandeaux de chapitres

- Pleine largeur bord à bord (débord gauche −1,2 in, padding compensé)
- Fond ardoise, titre aligné sur le corps de texte
- Filet or edge-to-edge sous le bandeau
- Parité recto/verso identique visuellement

## Citations en exergue

- Format `> « citation » — Auteur, lieu, date`
- Citation en rouge `#8B1A1A`, auteur en ardoise
- Guillemets français « »

## Corrections appliquées en session (à ne pas réintroduire)

1. Préfixe `ENCADRÉ — ` supprimé des 7 titres (p. 40, 46, 50, 55, 61, 67, 68)
2. Gras retiré des items dans les encadrés tardifs (p. 213, 219, 231)
3. Entête bleue restaurée sur `BERLIN, 1884-1885` (fix détection ratio lettres)
4. Étoiles `★ ★ ★` → `★★★` sur les 55 occurrences

## Script de build

```bash
python3 manuscrit-edition/build_pdf.py
```

Sortie : `manuscrit-edition/LIVRE-FINAL.pdf`
