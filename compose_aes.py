from PIL import Image, ImageDraw, ImageFont
import numpy as np

POSTER_PATH = "/root/.claude/uploads/d02e277f-fff6-4cf7-827d-9a040b193b34/68ec4185-15036.png"
FLAG_PATH   = "/root/.claude/uploads/d02e277f-fff6-4cf7-827d-9a040b193b34/d66d9da6-15030.jpg"
OUT_PATH    = "/home/user/tts-docs/aes_poster_final.png"
BOLD_FONT   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# ─── Load ─────────────────────────────────────────────────────────────────────
poster = Image.open(POSTER_PATH).convert("RGBA")
flag   = Image.open(FLAG_PATH).convert("RGBA")
W, H   = poster.size          # 1007 × 1562
fw, fh = flag.size            # 1024 × 706
cx_f, cy_f, r_f = 512, 353, 225

# ─── 1. CUSTOM AES GREEN BACKGROUND ──────────────────────────────────────────
# Build a full-size dark-green solid background
AES_BG = (10, 70, 10, 255)
green_bg = Image.new("RGBA", (W, H), AES_BG)

# Tile the darkened AES flag (at 40 % brightness) in the upper half for texture
scale   = W / fw
flag_tile = flag.resize((W, int(fh * scale)), Image.LANCZOS)
farr = np.array(flag_tile, dtype=np.float32) * 0.42
flag_tile_d = Image.fromarray(np.clip(farr, 0, 255).astype(np.uint8), "RGBA")
green_bg.paste(flag_tile_d, (0, 0))

# ─── 2. BLEND GREEN BACKGROUND WITH ORIGINAL POSTER ──────────────────────────
# Use a per-row alpha gradient:
#   rows 0 – 155     : fully replaced (title area) → alpha=1.0
#   rows 155 – 620   : soldier zone — moderate blend so faces/uniforms are clear
#   rows 620 – 950   : PEACE text band — partial tint
#   rows 950 – H     : handled separately (tree + dark)
poster_arr = np.array(poster,   dtype=np.float32)
bg_arr     = np.array(green_bg, dtype=np.float32)

soldier_top = 155
soldier_bot = 620
peace_bot   = 950

for row in range(soldier_top, H):
    if row < soldier_bot:
        # Soldier zone: blend 65 % green — suppresses US flag/text, faces still legible
        t = 0.65
    elif row < peace_bot:
        # PEACE text zone: 68 % green
        t = 0.68
    else:
        t = 0.0   # handled below
    poster_arr[row, :, :3] = (
        poster_arr[row, :, :3] * (1 - t) + bg_arr[row, :, :3] * t
    )

# Top zone (title row): fully replaced with dark
poster_arr[:soldier_top, :, :3] = bg_arr[:soldier_top, :, :3] * 0.20

poster = Image.fromarray(np.clip(poster_arr, 0, 255).astype(np.uint8), "RGBA")

# ─── 3. "SAHEL STATES" BIG WATERMARK (buries remaining "UNITED STATES" ghost) ─
wm_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wm_draw  = ImageDraw.Draw(wm_layer)
wm_font  = ImageFont.truetype(BOLD_FONT, 190)
wm_color = (0, 50, 0, 110)
for txt, y in [("SAHEL", 155), ("STATES", 340)]:
    tw = wm_draw.textlength(txt, font=wm_font)
    wm_draw.text(((W - tw) / 2, y), txt, fill=wm_color, font=wm_font)
poster = Image.alpha_composite(poster, wm_layer)

# ─── 4. BAOBAB TREE (tight crop = only sun+tree, no red ring) ─────────────────
# Inner sun radius is ~190 px → crop with r=175 to stay well inside
r_inner = 168
tree_crop = flag.crop((cx_f - r_inner, cy_f - 5,
                        cx_f + r_inner, cy_f + r_inner + 45))  # 336 × 218
# Scale to 74 % of poster width (centred)
tree_w  = int(W * 0.74)
tree_h  = int(tree_w * tree_crop.size[1] / tree_crop.size[0])
tree    = tree_crop.resize((tree_w, tree_h), Image.LANCZOS)
tarr    = np.array(tree, dtype=np.float32)
tarr[..., :3] *= 0.55
# Add a vignette: darken the left/right edges so the tree blends with the green margins
th, tw2 = tarr.shape[:2]
for col in range(tw2):
    edge_dist = min(col, tw2 - 1 - col) / (tw2 * 0.10)
    edge_dist = min(edge_dist, 1.0)
    tarr[:, col, :3] *= edge_dist
tree_dark = Image.fromarray(np.clip(tarr, 0, 255).astype(np.uint8), "RGBA")

# ─── 5. ERASE STATUE OF LIBERTY + BUILDINGS (dark gradient then tree) ─────────
poster_arr2 = np.array(poster, dtype=np.float32)
statue_top  = int(H * 0.60)
statue_bot  = int(H * 0.92)
for row in range(statue_top, statue_bot):
    t = 0.94 * ((row - statue_top) / (statue_bot - statue_top))
    poster_arr2[row, :, :3] *= (1 - t)
poster_arr2 = np.clip(poster_arr2, 0, 255).astype(np.uint8)
poster = Image.fromarray(poster_arr2, "RGBA")

# Paste tree centred in the lower section
city_top = int(H * 0.60)
city_bot = int(H * 0.97)
zone_h   = city_bot - city_top
tree_final = tree_dark.resize((tree_w, zone_h), Image.LANCZOS)
tree_x  = (W - tree_w) // 2
poster.paste(tree_final, (tree_x, city_top), mask=tree_final)

# Fill sides of tree zone with AES dark green
draw2 = ImageDraw.Draw(poster)
if tree_x > 0:
    draw2.rectangle([(0, city_top), (tree_x - 1, city_bot)], fill=(10, 55, 10, 255))
    draw2.rectangle([(tree_x + tree_w, city_top), (W, city_bot)], fill=(10, 55, 10, 255))

# ─── 6. AES LOGO EMBLEM (watermark behind soldiers) ──────────────────────────
logo_crop = flag.crop((cx_f - r_f - 20, cy_f - r_f - 20,
                        cx_f + r_f + 20, cy_f + r_f + 20))
logo_size = int(W * 0.54)
logo      = logo_crop.resize((logo_size, logo_size), Image.LANCZOS)
larr = np.array(logo, dtype=np.float32)
larr[..., :3] *= 0.40
larr[..., 3]  *= 0.55
logo_wm = Image.fromarray(np.clip(larr, 0, 255).astype(np.uint8), "RGBA")
logo_x = (W - logo_size) // 2
poster.paste(logo_wm, (logo_x, 158), mask=logo_wm)

# ─── 7. TITLE BAR ─────────────────────────────────────────────────────────────
draw = ImageDraw.Draw(poster)
draw.rectangle([(0, 0), (W, 3)],   fill=(180, 140, 30, 255))   # gold top strip
draw.rectangle([(0, 3), (W, 153)], fill=(5, 5, 5, 248))        # dark title bg
draw.rectangle([(0, 151), (W, 155)], fill=(180, 140, 30, 255)) # gold bottom strip

gold  = (212, 175, 55, 255)
white = (255, 255, 255, 255)

# Star row
sf = ImageFont.truetype(BOLD_FONT, 21)
stars = "★  ★  ★  ★  ★"
sw = draw.textlength(stars, font=sf)
draw.text(((W - sw) / 2, 8), stars, fill=gold, font=sf)

# "ALLIANCE OF"
f1 = ImageFont.truetype(BOLD_FONT, 52)
t1 = "ALLIANCE OF"
draw.text(((W - draw.textlength(t1, font=f1)) / 2, 35), t1, fill=white, font=f1)

# "SAHEL STATES" — gold, drop-shadowed
f2 = ImageFont.truetype(BOLD_FONT, 78)
t2 = "SAHEL STATES"
x2 = (W - draw.textlength(t2, font=f2)) / 2
draw.text((x2 + 2, 92), t2, fill=(20, 20, 20, 200), font=f2)   # shadow
draw.text((x2,     90), t2, fill=gold,               font=f2)

# ─── 8. SAVE ──────────────────────────────────────────────────────────────────
poster.convert("RGB").save(OUT_PATH, "PNG")
print("Done →", OUT_PATH)
