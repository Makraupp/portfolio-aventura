"""Gera assets/ e index.html do portfólio de aventura.

Uso: python build.py   (precisa de Pillow, pillow-heif e numpy)
Fonte das fotos: _2_Projetos/Fotografia - JOB no vault. Edite STORY e rode de novo.
"""
import html, io, json, os, struct
from PIL import Image, ImageOps, ImageStat
import pillow_heif

pillow_heif.register_heif_opener()
JOB = "G:/Meu Drive/AA Yo e dio/Obsidian/Makraupp/_2_Projetos/Fotografia - JOB/"
SURF = "SURF - precisa de edição nessas fotos, está muito nublado, cinza, precisa dar mais cor, mas de forma suave e profissional/"
LIVRE = "Imagens para usar onde quiser - só se preocupando com a composição/"
SITE = "https://makraupp.github.io/portfolio-aventura/"  # trocar se mudar de domínio
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")

# Lugares com coordenada. "~" no nome marca estimativa a confirmar.
P = {
    "mantiqueira": ("Serra da Mantiqueira", -22.40, -44.80),
    "norte-isl": ("Norte da Islândia", 65.68, -18.09),
    "godafoss": ("Goðafoss", 65.683, -17.550),
    "leste-isl": ("Fiordes do leste", 65.00, -13.80),
    "stokksnes": ("Stokksnes", 64.250, -14.970),
    "katla": ("Katla", 63.632, -19.051),
    "moher": ("Cliffs of Moher", 52.972, -9.426),
    "airshow": ("Air show~", 53.200, -6.100),
    "bled": ("Lago Bled", 46.363, 14.094),
    "braies": ("Lago di Braies", 46.694, 12.085),
    "dolomitas": ("Dolomitas", 46.540, 12.140),
    "colorado": ("El Colorado", -33.350, -70.290),
    "itatiaia": ("Itatiaia", -22.385, -44.693),
    "surf": ("Litoral norte~", -23.430, -45.070),
}

# Capítulos: (id, nome, contorno, textura, [linhas]). Linha: (layout, lugar, [arquivos], textura opcional)
# layouts: full · pair · trio · lead (grande + pequena)
STORY = [
    ("chile", "Chile", "chile", "tracks", [
        ("full", "colorado", ["Chile - El Colorado/IMG_7123.JPG"]),
        ("pair", "colorado", ["Chile - El Colorado/IMG_7195.JPG", "Chile - El Colorado/IMG_7197.JPG"]),
        ("full", "colorado", ["Chile - El Colorado/IMG_7356.JPG"]),
        ("trio", "colorado", ["Chile - El Colorado/IMG_7255.JPG", "Chile - El Colorado/IMG_7256.JPG", "Chile - El Colorado/IMG_7259.JPG"]),
        ("lead", "colorado", ["Chile - El Colorado/IMG_7336.JPG", "Chile - El Colorado/IMG_7261.JPG"]),
        ("pair", "colorado", ["Chile - El Colorado/IMG_7332.JPG", "Chile - El Colorado/IMG_7343.JPG"]),
        ("full", "colorado", ["Chile - El Colorado/IMG_7418.CR2"]),
        ("trio", "colorado", ["Chile - El Colorado/IMG_7344.JPG", "Chile - El Colorado/IMG_7347.JPG", "Chile - El Colorado/IMG_7410.CR2"]),
        ("pair", "colorado", ["Chile - El Colorado/IMG_7786.JPG", "Chile - El Colorado/IMG_7819.JPG"]),
        ("lead", "colorado", ["Chile - El Colorado/IMG_7865.JPG", "Chile - El Colorado/IMG_8039.JPG"]),
        ("trio", "colorado", ["Chile - El Colorado/IMG_7838.JPG", "Chile - El Colorado/IMG_7449.CR2", "Chile - El Colorado/IMG_8495.JPG"]),
        ("full", "colorado", ["Chile - El Colorado/IMG_8733.JPG"]),
        ("lead", "colorado", ["Chile - El Colorado/IMG_9221.JPG", "Chile - El Colorado/IMG_7135.JPG"]),
    ]),
    ("itatiaia", "Itatiaia", "brasil", "contour", [
        ("full", "itatiaia", ["Itatiatia/IMG_0946.jpeg"]),
        ("pair", "itatiaia", ["Itatiatia/IMG_1141.jpeg", "Itatiatia/IMG_4500.JPG"]),
        ("lead", "itatiaia", ["Itatiatia/IMG_4475.JPG", "Itatiatia/IMG_4494.JPG"]),
        ("pair", "itatiaia", ["Itatiatia/IMG_4552.JPG", "Itatiatia/IMG_4589.JPG"]),
        ("full", "itatiaia", ["Itatiatia/IMG_4624.JPG"]),
        ("trio", "itatiaia", ["Itatiatia/IMG_4637.JPG", "Itatiatia/IMG_4641.JPG", "Itatiatia/IMG_4705.JPG"]),
        ("lead", "itatiaia", ["Itatiatia/IMG_4685.JPG", "Itatiatia/IMG_4756.JPG"]),
        ("trio", "itatiaia", ["Itatiatia/IMG_4820.JPG", "Itatiatia/IMG_4861.JPG", "Itatiatia/IMG_4886.JPG"]),
        ("full", "itatiaia", ["Itatiatia/IMG_4841.JPG"]),
    ]),
    ("islandia", "Islândia", "islandia", "basalt", [
        ("full", "norte-isl", ["Iceland/IMG_5655.JPG"]),
        ("lead", "norte-isl", ["Iceland/IMG_5602.JPG", "Iceland/IMG_5731.JPG"]),
        ("pair", "norte-isl", ["Iceland/IMG_5701.JPG", "Iceland/IMG_5704.JPG"]),
        ("full", "godafoss", ["Iceland/IMG_5806.JPG"]),
        ("lead", "godafoss", ["Iceland/IMG_5750.JPG", "Iceland/IMG_5759.JPG"]),
        ("pair", "godafoss", ["Iceland/IMG_5743.JPG", "Iceland/IMG_5860.JPG"]),
        ("full", "godafoss", ["Iceland/IMG_5970.JPG"]),
        ("pair", "norte-isl", ["Iceland/IMG_5888.JPG", "Iceland/IMG_6081.JPG"]),
        ("full", "leste-isl", ["Iceland/IMG_6086.JPG"]),
        ("trio", "leste-isl", ["Iceland/IMG_6122.JPG", "Iceland/IMG_6127.JPG", "Iceland/IMG_6133.JPG"]),
        ("lead", "leste-isl", ["Iceland/IMG_6113.JPG", "Iceland/IMG_6139.JPG"]),
        ("full", "stokksnes", ["1 -Melhores/BFF62B52-C4EF-460D-A765-6389040DD719.jpg"]),
        ("pair", "stokksnes", ["1 -Melhores/E3F92A15-F88D-4014-990E-92A8DDA3762A.jpg", "Iceland/IMG_6196.JPG"]),
        ("full", "stokksnes", ["1 -Melhores/5EE7A548-ABB9-484A-B47B-70468D147FFE.jpg"]),
        ("full", "katla", ["Iceland/IMG_6319.JPG"]),
        ("trio", "katla", ["Iceland/IMG_6391.JPG", "Iceland/IMG_6414.JPG", "Iceland/IMG_6417.JPG"]),
        ("full", "katla", ["Iceland/IMG_6477.JPG"]),
        ("lead", "katla", ["1 -Melhores/Katla outside 4.jpg", "Iceland/IMG_6530.JPG"]),
        ("full", "katla", ["Iceland/IMG_6570.JPG"]),
    ]),
    ("dolomitas", "Dolomitas", "italia", "ridge", [
        ("full", "dolomitas", ["DOLOMITES/IMG_4325.CR2"]),
        ("pair", "dolomitas", ["DOLOMITES/IMG_4231.CR2", "DOLOMITES/IMG_4237.CR2"]),
        ("full", "dolomitas", ["DOLOMITES/IMG_4305.CR2"]),
        ("lead", "dolomitas", ["DOLOMITES/IMG_4366.CR2", "DOLOMITES/IMG_4362.CR2"]),
        ("trio", "dolomitas", ["DOLOMITES/IMG_4361.CR2", "DOLOMITES/IMG_4383.CR2", "DOLOMITES/IMG_4385.CR2"]),
        ("full", "braies", ["DOLOMITES/IMG_4446.CR2"]),
        ("pair", "dolomitas", ["DOLOMITES/IMG_4425.CR2", "DOLOMITES/IMG_4314.CR2"]),
        ("full", "dolomitas", ["DOLOMITES/IMG_4453.CR2"]),
    ]),
    ("irlanda", "Irlanda", "irlanda", "strata", [
        ("full", "moher", ["Cliffs ohf moher/IMG_5544.CR2"]),
        ("lead", "moher", ["Cliffs ohf moher/IMG_5591.CR2", "Cliffs ohf moher/IMG_5523.CR2"]),
        ("pair", "moher", ["Cliffs ohf moher/IMG_5500.CR2", "Cliffs ohf moher/IMG_5552.CR2"]),
        ("full", "airshow", ["Ireland air show/IMG_5098.CR2"], "contrail"),
        ("trio", "airshow", ["Ireland air show/IMG_5122.CR2", "Ireland air show/IMG_5127.CR2", "Ireland air show/IMG_5129.CR2"], "contrail"),
        ("pair", "airshow", ["Ireland air show/IMG_5133.CR2", "Ireland air show/IMG_5213.CR2"], "contrail"),
        ("pair", "airshow", ["Ireland air show/IMG_5141.CR2", "Ireland air show/IMG_5153.CR2"], "contrail"),
        ("lead", "airshow", ["Ireland air show/IMG_5323.CR2", "Ireland air show/IMG_5331.CR2"], "contrail"),
    ]),
    ("eslovenia", "Eslovênia", "eslovenia", "ripple", [
        ("lead", "bled", ["1 -Melhores/IMG_4002.JPG", "1 -Melhores/IMG_4038.JPG"]),
    ]),
    ("surf", "Surf", "brasil", "water", [
        ("full", "surf", [SURF + "IMG_9880.JPG"]),
        ("trio", "surf", [SURF + "IMG_0059.JPG", SURF + "IMG_0061.JPG", SURF + "IMG_0068.JPG"]),
        ("lead", "surf", [SURF + "IMG_0250.JPG", SURF + "IMG_0083.JPG"]),
        ("full", "surf", [SURF + "IMG_9977.JPG"]),
    ]),
]
DAWN = ("1 -Melhores/KLATA CAVE 2 -- final.PNG", "katla")
DUSK = (LIVRE + "IMG_1616.JPG", "mantiqueira")
INTERLUDES = {"islandia": LIVRE + "IMG_1575.JPG", "irlanda": LIVRE + "IMG_1604.JPG", "surf": LIVRE + "IMG_6886.JPG"}  # respiros antes destes capítulos


def cr2_orientation(p):
    b = open(p, "rb").read(65536)
    e = "<" if b[:2] == b"II" else ">"
    off = struct.unpack(e + "I", b[4:8])[0]
    for i in range(struct.unpack(e + "H", b[off:off + 2])[0]):
        tag = struct.unpack(e + "H", b[off + 2 + i * 12:off + 4 + i * 12])[0]
        if tag == 274:
            return struct.unpack(e + "H", b[off + 10 + i * 12:off + 12 + i * 12])[0]
    return 1


def load(rel):
    p = JOB + rel
    if p.lower().endswith(".cr2"):
        # O CR2 carrega um JPEG em resolução cheia; a rotação mora no TIFF, não nele.
        b, best, s = open(p, "rb").read(), None, 12
        while (s := b.find(b"\xff\xd8\xff", s + 3)) != -1:
            try:
                im = Image.open(io.BytesIO(b[s:]))
                if not best or im.width > best.width:
                    best = im
            except Exception:
                pass
        best.load()
        rot = {3: 180, 6: 270, 8: 90}.get(cr2_orientation(p))
        return best.convert("RGB").rotate(rot, expand=True) if rot else best.convert("RGB")
    return ImageOps.exif_transpose(Image.open(p)).convert("RGB")


def ground(im):
    r, g, b = ImageStat.Stat(im.resize((48, 48))).mean
    return "#%02x%02x%02x" % (int(r * .3 + 6), int(g * .3 + 6), int(b * .3 + 6))


done = {}


def export(rel):
    if rel in done:
        return done[rel]
    im = load(rel)
    slug = os.path.splitext(rel.replace("/", "-"))[0].split("-")[-1].lower().replace(" ", "")
    slug = f"{len(done):03d}-{slug}"[:40]
    big = im.copy(); big.thumbnail((1900, 1900), Image.LANCZOS); big.save(f"{OUT}/{slug}.webp", quality=80, method=6)
    small = im.copy(); small.thumbnail((900, 900), Image.LANCZOS); small.save(f"{OUT}/{slug}-s.webp", quality=78, method=6)
    spill = im.copy(); spill.thumbnail((40, 40), Image.LANCZOS); spill.save(f"{OUT}/{slug}-spill.webp", quality=70)
    done[rel] = dict(slug=slug, w=big.width, h=big.height, ground=ground(im))
    print(slug, big.size)
    return done[rel]


def img(m, eager=False, sizes="(max-width: 720px) 100vw, 60vw"):
    lazy = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return (f'<img src="assets/{m["slug"]}.webp" srcset="assets/{m["slug"]}-s.webp 900w, assets/{m["slug"]}.webp {max(m["w"], m["h"])}w" '
            f'sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt=""{lazy} decoding="async">')


def stop_attrs(m, place, tex=None):
    name, lat, lon = P[place]
    t = f' data-tex="{tex}"' if tex else ""
    return (f'data-ground="{m["ground"]}" data-spill="assets/{m["slug"]}-spill.webp" '
            f'data-lat="{lat}" data-lon="{lon}"{t}')


os.makedirs(OUT, exist_ok=True)
outlines = json.load(open(os.path.join(HERE, "outlines.json")))
SIZES = {"full": "(max-width: 720px) 100vw, 80vw", "pair": "(max-width: 720px) 100vw, 45vw",
         "trio": "(max-width: 720px) 100vw, 30vw", "lead": "(max-width: 720px) 100vw, 60vw"}

parts = []
for cid, name, outline, tex, rows in STORY:
    if cid in INTERLUDES:
        m = export(INTERLUDES[cid])
        parts.append(f'<section class="row full rest" {stop_attrs(m, "mantiqueira", "sun")}>'
                     f'<figure class="shot">{img(m, sizes=SIZES["full"])}</figure></section>')
    o = outlines[outline]
    parts.append(f'<div class="chapter" id="{cid}" data-outline="{outline}" data-tex="{tex}">')
    for row in rows:
        layout, place, files = row[:3]
        rtex = row[3] if len(row) > 3 else None
        ms = [export(f) for f in files]
        figs = "".join(f'<figure class="shot{" tall" if m["h"] > m["w"] else ""}">{img(m, sizes=SIZES[layout])}</figure>' for m in ms)
        parts.append(f'<section class="row {layout}" {stop_attrs(ms[0], place, rtex)}>{figs}</section>')
    parts.append("</div>")

dawn, dusk = export(DAWN[0]), export(DUSK[0])
# Prévia de link (WhatsApp, Instagram, LinkedIn): JPG 1200x630 da capa.
ImageOps.fit(load(DAWN[0]), (1200, 630), Image.LANCZOS).save(os.path.join(HERE, "og.jpg"), quality=85)
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
page = (tpl.replace("{{STORY}}", "\n".join(parts))
        .replace("{{DAWN_IMG}}", img(dawn, eager=True, sizes="100vw"))
        .replace("{{DAWN_ATTRS}}", stop_attrs(dawn, "katla", "basalt"))
        .replace("{{DUSK_IMG}}", img(dusk, sizes="100vw"))
        .replace("{{DUSK_ATTRS}}", stop_attrs(dusk, "mantiqueira", "sun"))
        .replace("{{GROUND}}", dawn["ground"])
        .replace("{{OG}}", SITE + "og.jpg").replace("{{SITE}}", SITE)
        .replace("{{OUTLINES}}", json.dumps(outlines))
        .replace("{{COUNT}}", str(len(done))))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print("ok", len(done), "fotos")
