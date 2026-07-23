import base64, io, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "branding_src", "logo-source.png")
BLUE = (0, 74, 173)          # #004AAD  brand cube blue
INK  = (15, 23, 42)          # #0F172A  dark text
ADMIN  = os.path.join(ROOT, "frontend", "src", "assets")
PUBLIC = os.path.join(ROOT, "static", "public", "static")
PUB2   = os.path.join(ROOT, "frontend", "public", "static")

im = Image.open(SRC).convert("RGBA")
bb = im.getbbox()
cube = im.crop(bb)
# pad to square, transparent
s = max(cube.size)
sq = Image.new("RGBA", (s, s), (0,0,0,0))
sq.paste(cube, ((s-cube.width)//2, (s-cube.height)//2), cube)

def png_bytes(img):
    b = io.BytesIO(); img.save(b, "PNG"); return b.getvalue()

# --- favicon.png (64) ---
fav = sq.resize((64,64), Image.LANCZOS)
for d in (ADMIN, PUBLIC, PUB2):
    os.makedirs(d, exist_ok=True)
    fav.save(os.path.join(d, "favicon.png"))

# --- embedded cube for SVG (crisp 128px) ---
emb = sq.resize((128,128), Image.LANCZOS)
b64 = base64.b64encode(png_bytes(emb)).decode()
datauri = "data:image/png;base64," + b64

# --- logo-mark.svg (square icon) ---
mark = f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 32 32" role="img" aria-label="Hakobu">
  <title>Hakobu</title>
  <image href="{datauri}" x="0" y="0" width="32" height="32"/>
</svg>
'''

# --- logo.svg (wordmark: cube + Hako(dark)bu(blue)) ---
logo = f'''<svg xmlns="http://www.w3.org/2000/svg" width="176" height="40" viewBox="0 0 176 40" fill="none" role="img" aria-label="Hakobu">
  <title>Hakobu</title>
  <image href="{datauri}" x="0" y="3" width="34" height="34"/>
  <text x="44" y="28" font-family="'Segoe UI','Inter','Helvetica Neue',Arial,sans-serif" font-weight="700" font-size="23" letter-spacing="0.2">
    <tspan fill="#0F172A">Hako</tspan><tspan fill="#004AAD">bu</tspan>
  </text>
</svg>
'''
for d in (ADMIN, PUBLIC):
    open(os.path.join(d, "logo-mark.svg"), "w", encoding="utf-8").write(mark)
    open(os.path.join(d, "logo.svg"), "w", encoding="utf-8").write(logo)

# --- logo.png (raster wordmark, height ~40) ---
def make_wordmark():
    H = 44
    cube_px = 40
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 30)
    except Exception:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
    # measure text
    tmp = Image.new("RGBA",(10,10)); dd=ImageDraw.Draw(tmp)
    hako = "Hako"; bu = "bu"
    w1 = dd.textlength(hako, font=font); w2 = dd.textlength(bu, font=font)
    gap = 12
    W = cube_px + gap + int(w1 + w2) + 6
    img = Image.new("RGBA",(W,H),(0,0,0,0))
    c = sq.resize((cube_px,cube_px), Image.LANCZOS)
    img.paste(c,(0,(H-cube_px)//2),c)
    d = ImageDraw.Draw(img)
    ty = (H-30)//2 - 4
    x = cube_px + gap
    d.text((x,ty), hako, font=font, fill=INK)
    d.text((x+w1, ty), bu, font=font, fill=BLUE)
    return img
wm = make_wordmark()
for d in (ADMIN, PUBLIC):
    wm.save(os.path.join(d, "logo.png"))

print("favicon:", fav.size, "| wordmark png:", wm.size, "| svg embed:", len(b64), "b64 chars")
print("written to:", ADMIN, PUBLIC, PUB2)
