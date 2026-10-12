#!/usr/bin/env python3
"""
Builds dark_mode.svg and light_mode.svg from custom ASCII text files.

Requirements:
    pip install pillow

Usage:
    python generate_svg.py

ASCII file priority:
    Dark:  my_ascii_dark.txt -> my_ascii.txt
    Light: my_ascii_light.txt -> my_ascii.txt

The GitHub Action can update the statistics afterward.
"""

import os
import re
from html import escape

# ======================= EDIT YOUR INFO HERE =======================

HANDLE = "abderrahmane@ar-software"

INFO = [
    ("OS", "CachyOS Linux"),
    ("Brand", "ArSoftware"),
    ("Role", "Full Stack Web Developer"),
    ("Environment", "Hyprland"),
    None,
    ("Stack.Frontend", "React, JavaScript, HTML, CSS, Tailwind CSS"),
    ("Stack.Backend", "PHP, Laravel, Node.js, Express"),
    ("Stack.Database", "MongoDB, MySQL"),
    ("Stack.Tools", "Git, GitHub, Vercel, Docker"),
    None,
    ("Interests.Software", "Web apps, useful tools, product ideas"),
    ("Interests.Design", "Clean UI, simple user experiences"),
    ("Interests.Building", "Turning ideas into working applications"),
]

CONTACT = [
    ("Email", "abderrahmanerb.contact@gmail.com"),
    ("Portfolio", "aarab-abderrahmane.vercel.app"),
    ("GitHub", "github.com/aarab-abderrahmane"),
    ("LinkedIn", "aarab-abderrahmane-2b9509336"),
]

# ===================================================================

# ======================= LAYOUT SETTINGS ===========================

WIDTH = 1000
ART_BOX_W = 380

# Horizontal positions
ART_X = 15
INFO_X = 390

# Text layout
WIDTH_CHARS = 60
ART_FS = 12
LH = 20

# ===================================================================

THEMES = {
    "dark": dict(
        art="#c9d1d9",
        txt="#c9d1d9",
        key="#ffa657",
        val="#a5d6ff",
        add="#3fb950",
        dele="#f85149",
        cc="#616e7f",
    ),
    "light": dict(
        art="#24292f",
        txt="#24292f",
        key="#953800",
        val="#0a3069",
        add="#1a7f37",
        dele="#cf222e",
        cc="#c2cfde",
    ),
}

ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def load_custom(theme_name):
    """
    Load custom ASCII art and remove common leading indentation
    without changing the relative alignment of the characters.
    """

    candidates = (
        f"my_ascii_{theme_name}.txt",
        "my_ascii.txt",
    )

    for path in candidates:
        if not os.path.isfile(path):
            continue

        with open(path, "r", encoding="utf-8", errors="replace") as file:
            text = file.read()

        # Remove terminal ANSI color codes.
        text = ANSI.sub("", text)

        # Normalize line endings and tabs.
        lines = [
            line.expandtabs(4).rstrip()
            for line in text.replace("\r", "").split("\n")
        ]

        # Remove blank lines at the beginning and end.
        while lines and not lines[0].strip():
            lines.pop(0)

        while lines and not lines[-1].strip():
            lines.pop()

        if not lines:
            continue

        # Remove shared indentation from all non-empty lines.
        non_empty = [line for line in lines if line.strip()]

        indent = min(
            len(line) - len(line.lstrip())
            for line in non_empty
        )

        if indent:
            lines = [line[indent:] for line in lines]

        print(f"Loaded custom ASCII: {path}")
        return lines

    raise FileNotFoundError(
        f"No custom ASCII file found for theme '{theme_name}'. "
        f"Create my_ascii_{theme_name}.txt or my_ascii.txt."
    )


def fit(lines):
    """
    Calculate a font size that keeps the ASCII art within ART_BOX_W.
    """

    cols = max(len(line) for line in lines)

    if cols == 0:
        return ART_FS, ART_FS * 1.17

    font_size = min(
        ART_FS,
        ART_BOX_W / (cols * 0.6),
    )

    line_height = font_size * 1.17

    return round(font_size, 2), round(line_height, 2)


class Info:
    def __init__(self):
        self.y = 30
        self.rows = []

    def blank(self):
        self.y += LH

    def raw(self, markup):
        self.rows.append(
            f'<tspan x="{INFO_X}" y="{self.y}"{markup}'
        )
        self.y += LH

    def header(self, text):
        fill = WIDTH_CHARS - len(text) - 1

        self.raw(
            f'>{escape(text)}</tspan> -'
            f'{"—" * max(0, fill - 3)}-—-'
        )

    def kv(self, key, value, vid=None, did=None):
        left = 2 + len(key) + 1
        n = max(1, WIDTH_CHARS - left - 2 - len(value))

        key_markup = ".".join(
            f'<tspan class="key">{escape(part)}</tspan>'
            for part in key.split(".")
        )

        dots_id = f' id="{did}"' if did else ""
        value_id = f' id="{vid}"' if vid else ""

        self.raw(
            f' class="cc">. </tspan>'
            f'{key_markup}:'
            f'<tspan class="cc"{dots_id}> {"." * n} </tspan>'
            f'<tspan class="value"{value_id}>'
            f'{escape(value)}</tspan>'
        )


def stats_block(info):
    """Create GitHub statistics fields for the external updater."""

    info.raw(
        ' class="cc">. </tspan>'
        '<tspan class="key">Repos</tspan>:'
        '<tspan class="cc" id="repo_data_dots"> .... </tspan>'
        '<tspan class="value" id="repo_data">0</tspan>'
        ' {<tspan class="key">Contributed</tspan>: '
        '<tspan class="value" id="contrib_data">0</tspan>'
        '} | <tspan class="key">Stars</tspan>:'
        '<tspan class="cc" id="star_data_dots"> ........... </tspan>'
        '<tspan class="value" id="star_data">0</tspan>'
    )

    info.raw(
        ' class="cc">. </tspan>'
        '<tspan class="key">Commits</tspan>:'
        '<tspan class="cc" id="commit_data_dots"> ................. </tspan>'
        '<tspan class="value" id="commit_data">0</tspan>'
        ' | <tspan class="key">Followers</tspan>:'
        '<tspan class="cc" id="follower_data_dots"> ....... </tspan>'
        '<tspan class="value" id="follower_data">0</tspan>'
    )

    info.raw(
        ' class="cc">. </tspan>'
        '<tspan class="key">Lines of Code on GitHub</tspan>:'
        '<tspan class="cc" id="loc_data_dots">. </tspan>'
        '<tspan class="value" id="loc_data">0</tspan>'
        ' ( <tspan class="addColor" id="loc_add">0</tspan>'
        '<tspan class="addColor">++</tspan>, '
        '<tspan id="loc_del_dots"> </tspan>'
        '<tspan class="delColor" id="loc_del">0</tspan>'
        '<tspan class="delColor">--</tspan> )'
    )


def build_info():
    info = Info()

    info.header(HANDLE)

    for item in INFO:
        if item is None:
            info.blank()
        elif item[0] == "Uptime":
            info.kv(
                "Uptime",
                item[1],
                vid="age_data",
                did="age_data_dots",
            )
        else:
            info.kv(*item)

    info.blank()
    info.header("- Contact")

    for item in CONTACT:
        info.kv(*item)

    info.blank()
    info.header("- GitHub Stats")

    stats_block(info)

    return info


def write_svgs():
    """
    Generate dark_mode.svg and light_mode.svg using custom ASCII only.
    """

    info = build_info()
    arts = {}

    # Load custom ASCII for each theme.
    for theme_name in THEMES:
        arts[theme_name] = load_custom(theme_name)

    # Calculate a shared SVG height.
    heights = []

    for theme_name in THEMES:
        _, line_height = fit(arts[theme_name])

        art_height = (
            30 + len(arts[theme_name]) * line_height + 20
        )

        heights.append(art_height)

    height = int(max(max(heights), info.y + 10))

    # Generate both SVG files.
    for theme_name, theme in THEMES.items():
        lines = arts[theme_name]
        font_size, line_height = fit(lines)

        y0 = 30

        # Every ASCII line starts at ART_X.
        art_svg = "\n".join(
            f'<tspan x="{ART_X}" '
            f'y="{y0 + i * line_height:.2f}">'
            f'{escape(line)}</tspan>'
            for i, line in enumerate(lines)
        )

        svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}px"
     height="{height}px"
     font-family="Consolas, 'Courier New', monospace"
     font-size="16px">

<style>
.key {{ fill: {theme["key"]}; }}
.value {{ fill: {theme["val"]}; }}
.addColor {{ fill: {theme["add"]}; }}
.delColor {{ fill: {theme["dele"]}; }}
.cc {{ fill: {theme["cc"]}; }}
text, tspan {{ white-space: pre; }}
</style>

<rect width="{WIDTH}px"
      height="{height}px"
      rx="15"/>

<text x="{ART_X}"
      y="{y0}"
      fill="{theme["art"]}"
      font-size="{font_size}px"
      xml:space="preserve">
{art_svg}
</text>

<text x="{INFO_X}" y="30" fill="{theme["txt"]}">
{chr(10).join(info.rows)}
</text>

</svg>
"""

        filename = f"{theme_name}_mode.svg"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg)

        print(
            f"Generated {filename} "
            f"({WIDTH}x{height}, artwork font {font_size}px, "
            f"ART_X={ART_X}, INFO_X={INFO_X})"
        )


if __name__ == "__main__":
    write_svgs()