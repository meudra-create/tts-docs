# /verif-pdf — Vérification visuelle du PDF avec Ghostscript

Procédure pour contrôler que les encadrés ne sont pas coupés entre deux pages.

## Prérequis

```bash
apt-get install -y ghostscript
gs --version   # doit afficher 10.x
```

## Étape 1 — Rasteriser toutes les pages

```bash
mkdir -p /tmp/pdf-pages
gs -dBATCH -dNOPAUSE -sDEVICE=png16m -r72 \
   -sOutputFile="/tmp/pdf-pages/page-%03d.png" \
   manuscrit-edition/LIVRE-FINAL.pdf 2>&1 | grep "^Page" | tail -3
ls /tmp/pdf-pages/ | wc -l   # nombre total de pages
```

Résolution 72 dpi suffit pour détecter les blocs de couleur (fond ardoise `#2C3A4A`).

## Étape 2 — Détecter les pages avec encadrés

```python
import os, struct, zlib

def count_encadre_pixels(filepath):
    with open(filepath, "rb") as f:
        f.read(8)
        chunks = []
        while True:
            length_bytes = f.read(4)
            if not length_bytes or len(length_bytes) < 4: break
            length = struct.unpack(">I", length_bytes)[0]
            chunk_type = f.read(4)
            data = f.read(length)
            f.read(4)
            chunks.append((chunk_type, data))
            if chunk_type == b"IEND": break
    ihdr = chunks[0][1]
    width  = struct.unpack(">I", ihdr[0:4])[0]
    height = struct.unpack(">I", ihdr[4:8])[0]
    idat_data = b"".join(c[1] for c in chunks if c[0] == b"IDAT")
    raw = zlib.decompress(idat_data)
    count = 0
    row_size = 1 + width * 3
    for y in range(0, height, 5):        # échantillonnage 1/5
        row_start = y * row_size
        for x in range(0, width, 5):
            px = row_start + 1 + x * 3
            r, g, b = raw[px], raw[px+1], raw[px+2]
            # Couleur ardoise #2C3A4A ± 15
            if 29 <= r <= 59 and 43 <= g <= 73 and 59 <= b <= 89:
                count += 1
    return count

encadre_pages = []
for i in range(1, 400):   # adapter au nb de pages
    path = f'/tmp/pdf-pages/page-{i:03d}.png'
    if os.path.exists(path):
        n = count_encadre_pixels(path)
        if n > 20:
            encadre_pages.append((i, n))

print(f"{len(encadre_pages)} pages avec encadrés :")
for p, n in encadre_pages:
    print(f"  Page {p:3d}: {n} pixels")
```

## Étape 3 — Vérifier les pages consécutives (coupures potentielles)

Pages consécutives dans la liste = encadré potentiellement coupé.

```python
# Localisation verticale des pixels ardoise
def vertical_position(filepath):
    # (réutiliser count_encadre_pixels avec top/bottom split)
    # top > bot*2 → encadré en HAUT   (début de page)
    # bot > top*2 → encadré en BAS    (fin de page)
    # sinon       → encadré ENTIER    (occupe toute la page)
    ...
```

Signature d'une coupure : page N encadré en BAS + page N+1 encadré en HAUT.

## Étape 4 — Vérification visuelle directe

```python
# Lire une page PNG dans Claude (tool Read) pour contrôle visuel
# Read("/tmp/pdf-pages/page-270.png")
```

## Résultats de référence (build 888 Ko, 305 pages, 21 juin 2026)

| Pages | Encadré | Statut |
|---|---|---|
| 67 | LA PYRAMIDE DE DOMINATION | ✓ complet |
| 68 | DÉCONSTRUCTION DU LEXIQUE IMPÉRIAL | ✓ complet |
| 270 | L'INTERVIEW DU 12 MAI, AU CRIBLE DES FAITS (7 lignes) | ✓ complet |
| 273 | LE SOMMET D'AFRICA FORWARD, AU CRIBLE DES FAITS (6 lignes) | ✓ complet |
| 278 | CONDITIONS POSSIBLES DE L'ÉCHEC | ✓ complet |
| 279 | CONDITIONS NÉCESSAIRES AU SUCCÈS | ✓ complet |

**Conclusion** : 50 emplacements détectés, 0 coupure. CSS `page-break-inside: avoid` opérationnel.

## Notes

- Pixel count > 20 = encadré réel ; entre 1-19 = entête de chapitre (bande ardoise plus étroite)
- Les entêtes de chapitre ont une bande ardoise fine → bruit normal, pas d'encadré
- Nettoyer après : `rm -rf /tmp/pdf-pages`
