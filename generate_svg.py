#!/usr/bin/env python3
"""
Builds dark_mode.svg and light_mode.svg (Andrew6rant-style profile card).
Run ONCE locally (the GitHub Action only updates the numbers afterwards):

    pip install pillow
    python generate_svg.py me.png              # your photo (PNG, background removed = best)
    python generate_svg.py me.png --cols 56    # more detail
    python generate_svg.py                     # no photo -> placeholder silhouette

Everything marked  # TODO  is a PLACEHOLDER or a guess: edit it, then re-run.
"""
import argparse
from html import escape
from PIL import Image, ImageDraw, ImageEnhance, ImageOps, ImageFilter

# ======================= EDIT YOUR INFO HERE =======================
HANDLE = "abderrahmane@ar-software"          # header line (user@host)
INFO = [                                      # (key, value) ; None = blank line ; "Uptime" is auto-updated
    ("OS", "Windows 11, Linux"),                              # TODO guess
    ("Uptime", "0 years, 0 months, 0 days"),                  # auto-updated from BIRTHDAY in today.py
    ("Host", "AR Software"),
    ("Kernel", "Full Stack Developer"),
    ("IDE", "VS Code"),                                       # TODO guess
    None,
    ("Languages.Programming", "TypeScript, JavaScript, PHP, Python"),
    ("Languages.Web", "HTML, CSS, Tailwind"),
    ("Languages.Real", "Arabic, French, English"),            # TODO guess
    None,
    ("Hobbies.Software", "Desktop apps, AI integrations"),
    ("Hobbies.Hardware", "YOUR_HARDWARE_HOBBY"),              # TODO PLACEHOLDER (or delete this line)
]
CONTACT = [
    ("Email.Personal", "abderrahmanerb.contact@gmail.com"),
    ("Portfolio", "aarab-abderrahmane.vercel.app"),
    ("LinkedIn", "aarab-abderrahmane"),
    ("Discord", "YOUR_DISCORD_HANDLE"),                       # TODO PLACEHOLDER (or delete this line)
]
# ===================================================================

WIDTH_CHARS = 60                      # width of the info column (matches today.py dot lengths)
ART_FS, ART_CW, ART_LH = 12, 7.2, 14  # ascii font size / char width / line height
LH = 20                               # info line height
INFO_X, ART_X = 400, 15

RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
THEMES = {
    "dark":  dict(bg="#161b22", art="#c9d1d9", txt="#c9d1d9", key="#ffa657", val="#a5d6ff",
                  add="#3fb950", dele="#f85149", cc="#616e7f", rev=False),
    "light": dict(bg="#f6f8fa", art="#24292f", txt="#24292f", key="#953800", val="#0a3069",
                  add="#1a7f37", dele="#cf222e", cc="#c2cfde", rev=True),
}


def placeholder_photo():
    im = Image.new("RGBA", (400, 500), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((60, 330, 340, 640), fill=(200, 200, 200, 255))          # shoulders
    d.rectangle((165, 250, 235, 360), fill=(170, 170, 170, 255))       # neck
    d.ellipse((115, 60, 285, 290), fill=(215, 215, 215, 255))          # head
    d.ellipse((150, 150, 180, 170), fill=(60, 60, 60, 255))            # eyes
    d.ellipse((220, 150, 250, 170), fill=(60, 60, 60, 255))
    d.arc((160, 190, 240, 250), 20, 160, fill=(60, 60, 60, 255), width=5)
    return im.filter(ImageFilter.GaussianBlur(1.5))


def photo_cells(path, cols, contrast):
    im = Image.open(path).convert("RGBA") if path else placeholder_photo()
    rows = max(1, int(cols * im.height / im.width * (ART_CW / ART_LH)))
    im = im.resize((cols, rows), Image.LANCZOS)
    alpha = im.getchannel("A")
    flat = Image.alpha_composite(Image.new("RGBA", im.size, (0, 0, 0, 255)), im).convert("L")
    gray = ImageEnhance.Contrast(ImageOps.autocontrast(flat, cutoff=2)).enhance(contrast)
    return gray, alpha, rows


def art_lines(gray, alpha, rows, cols, rev):
    ramp = RAMP[::-1] if rev else RAMP
    lines = []
    for y in range(rows):
        row = ""
        for x in range(cols):
            if alpha.getpixel((x, y)) < 100:
                row += " "
            else:
                row += ramp[min(len(ramp) - 1, gray.getpixel((x, y)) * len(ramp) // 256)]
        lines.append(row.rstrip())
    return lines


class Info:
    def __init__(self):
        self.y, self.rows = 30, []

    def blank(self):
        self.y += LH

    def raw(self, markup):
        self.rows.append(f'<tspan x="{INFO_X}" y="{self.y}"{markup}')
        self.y += LH

    def header(self, text):
        fill = WIDTH_CHARS - len(text) - 1
        self.raw(f'>{escape(text)}</tspan> -{"—" * (fill - 3)}-—-')

    def kv(self, key, value, vid=None, did=None):
        left = 2 + len(key) + 1                                  # ". Key:"
        n = max(1, WIDTH_CHARS - left - 2 - len(value))
        key_markup = '.'.join(f'<tspan class="key">{escape(k)}</tspan>' for k in key.split('.'))
        dots = f' id="{did}"' if did else ''
        vals = f' id="{vid}"' if vid else ''
        self.raw(f' class="cc">. </tspan>{key_markup}:<tspan class="cc"{dots}> {"." * n} </tspan>'
                 f'<tspan class="value"{vals}>{escape(value)}</tspan>')


def stats_block(info):
    # Same layout/lengths Andrew's today.py expects (ids are filled by the GitHub Action)
    info.raw(' class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan>'
             '<tspan class="value" id="repo_data">0</tspan> {<tspan class="key">Contributed</tspan>: '
             '<tspan class="value" id="contrib_data">0</tspan>} | <tspan class="key">Stars</tspan>:'
             '<tspan class="cc" id="star_data_dots"> ........... </tspan><tspan class="value" id="star_data">0</tspan>')
    info.raw(' class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> ................. </tspan>'
             '<tspan class="value" id="commit_data">0</tspan> | <tspan class="key">Followers</tspan>:'
             '<tspan class="cc" id="follower_data_dots"> ....... </tspan><tspan class="value" id="follower_data">0</tspan>')
    info.raw(' class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan>'
             '<tspan class="value" id="loc_data">0</tspan> ( <tspan class="addColor" id="loc_add">0</tspan>'
             '<tspan class="addColor">++</tspan>, <tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
             '<tspan class="delColor">--</tspan> )')


def build_info():
    info = Info()
    info.header(HANDLE)
    for it in INFO:
        if it is None:
            info.blank()
        elif it[0] == "Uptime":
            info.kv("Uptime", it[1], vid="age_data", did="age_data_dots")
        else:
            info.kv(*it)
    info.blank()
    info.header("- Contact")
    for it in CONTACT:
        info.kv(*it)
    info.blank()
    info.header("- GitHub Stats")
    stats_block(info)
    return info


def write_svgs(photo, cols, contrast):
    gray, alpha, rows = photo_cells(photo, cols, contrast)
    info = build_info()
    height = max(rows * ART_LH + 40, info.y + 10)
    width = 1000
    for name, t in THEMES.items():
        art = art_lines(gray, alpha, rows, cols, t["rev"])
        art_svg = "\n".join(f'<tspan x="{ART_X}" y="{30 + i * ART_LH}">{escape(l)}</tspan>' for i, l in enumerate(art))
        svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{width}px" height="{height}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {t["key"]};}}
.value {{fill: {t["val"]};}}
.addColor {{fill: {t["add"]};}}
.delColor {{fill: {t["dele"]};}}
.cc {{fill: {t["cc"]};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{width}px" height="{height}px" fill="{t["bg"]}" rx="15"/>
<text x="{ART_X}" y="30" fill="{t["art"]}" font-size="{ART_FS}px" class="ascii">
{art_svg}
</text>
<text x="{INFO_X}" y="30" fill="{t["txt"]}">
{chr(10).join(info.rows)}
</text>
</svg>
"""
        with open(f"{name}_mode.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {name}_mode.svg ({width}x{height})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", nargs="?", help="PNG/JPG of you (omit for placeholder)")
    ap.add_argument("--cols", type=int, default=50, help="ASCII width in characters (max ~53)")
    ap.add_argument("--contrast", type=float, default=1.3)
    a = ap.parse_args()
    write_svgs(a.photo, min(a.cols, 53), a.contrast)
