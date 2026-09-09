#!/usr/bin/env python3
"""Rebuild the original SVG artwork and one-shot GIF. Requires Pillow for the GIF."""
from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
PALETTES = {
    "dark": dict(bg="#0B1220", panel="#111D30", ink="#F1F6FF", muted="#A6B6CC", line="#263952", cyan="#67E8F9", violet="#B8A1FF", glow="#102F47"),
    "light": dict(bg="#F4F8FF", panel="#FFFFFF", ink="#14233B", muted="#4D617E", line="#D1DEF0", cyan="#00788C", violet="#7151CE", glow="#DDF3FC"),
}


def text(x, y, content, size, fill, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" {extra}>{escape(content)}</text>'


def svg(width, height, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>{body}</svg>\n'


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def monogram(x, y, scale, p):
    return f'''<g transform="translate({x} {y}) scale({scale})">
      <circle cx="150" cy="150" r="144" fill="none" stroke="{p['line']}"/>
      <circle cx="150" cy="150" r="118" fill="none" stroke="{p['line']}" stroke-dasharray="2 12"/>
      <path d="M6 150H47 M253 150H294 M150 6V47 M150 253V294" stroke="{p['cyan']}" stroke-width="2"/>
      <rect x="54" y="54" width="192" height="192" rx="38" fill="{p['panel']}" stroke="{p['line']}" transform="rotate(-12 150 150)"/>
      <rect x="54" y="54" width="192" height="192" rx="38" fill="{p['panel']}" stroke="{p['line']}" transform="rotate(8 150 150)"/>
      <path d="M88 205V100L150 172L212 100V205" fill="none" stroke="{p['violet']}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" opacity="0.2" transform="translate(5 7)"/>
      <path d="M88 198V93L150 165L212 93V198" fill="none" stroke="url(#brand)" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="274" cy="78" r="6" fill="{p['cyan']}"/>
      <circle cx="35" cy="233" r="5" fill="{p['violet']}"/>
    </g>'''


def hero(theme, compact=False):
    p = PALETTES[theme]
    w, h = (640, 530) if compact else (1200, 480)
    body = f'''<defs>
      <linearGradient id="brand" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{p['cyan']}"/><stop offset="1" stop-color="{p['violet']}"/></linearGradient>
      <radialGradient id="glow"><stop stop-color="{p['glow']}"/><stop offset="1" stop-color="{p['bg']}"/></radialGradient>
      <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="{p['line']}" stroke-width="0.6"/></pattern>
      <clipPath id="clip"><rect width="{w}" height="{h}" rx="26"/></clipPath>
    </defs>
    <g clip-path="url(#clip)">
      <rect width="{w}" height="{h}" fill="{p['bg']}"/>
      <ellipse cx="{w - 60}" cy="{h // 2}" rx="450" ry="420" fill="url(#glow)"/>
      <rect x="{w // 2}" width="{w // 2}" height="{h}" fill="url(#grid)" opacity="0.52"/>
      <path d="M1 1H{w - 1}" stroke="url(#brand)" stroke-width="4"/>
    '''
    if compact:
        body += monogram(436, 25, .55, p)
        body += text(38, 61, "M / 002", 19, p['cyan'], 700, 'letter-spacing="3"')
        body += text(38, 178, "Mallesh.", 87, p['ink'], 700, 'letter-spacing="-4"')
        body += text(40, 259, "Thoughtful APIs.", 42, p['ink'], 600, 'letter-spacing="-1"')
        body += text(40, 311, "Reliable systems.", 42, p['ink'], 600, 'letter-spacing="-1"')
        body += text(40, 376, "Full stack developer", 27, p['muted'])
        body += text(40, 414, "Backend focus", 27, p['muted'])
        body += f'<path d="M40 455H600" stroke="{p["line"]}"/>'
        body += text(40, 493, "APIs  /  DATA  /  AI", 20, p['cyan'], 600, 'letter-spacing="2"')
    else:
        body += text(56, 61, "M / 002", 18, p['cyan'], 700, 'letter-spacing="3"')
        body += text(56, 186, "Mallesh.", 116, p['ink'], 700, 'letter-spacing="-5"')
        body += text(60, 260, "Thoughtful APIs.", 43, p['ink'], 600, 'letter-spacing="-1"')
        body += text(60, 313, "Reliable systems.", 43, p['ink'], 600, 'letter-spacing="-1"')
        body += text(60, 365, "Full stack developer · Backend focus", 23, p['muted'])
        body += monogram(810, 62, 1.02, p)
        body += f'<path d="M60 409H1140" stroke="{p["line"]}"/>'
        body += text(60, 447, "APIs  /  DATA  /  AI", 17, p['cyan'], 600, 'letter-spacing="2"')
        body += text(1140, 447, "github.com/mallesh002", 17, p['muted'], extra='text-anchor="end"')
    body += f'</g><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="26" fill="none" stroke="{p["line"]}"/>'
    write(f'hero-{theme}{"-mobile" if compact else ""}.svg', svg(w, h, 'Mallesh. Thoughtful APIs. Reliable systems. Full stack developer with a backend focus.', body))


STACK = [
    ("nodedotjs", "Node.js", "#7ACB71", "#34772C"),
    ("typescript", "TypeScript", "#78B7FF", "#2765A8"),
    ("express", "Express", "#DCE7F7", "#243C5B"),
    ("mysql", "MySQL", "#83C8E4", "#176783"),
    ("drizzle", "Drizzle ORM", "#C5F74F", "#56780F"),
    ("react", "React", "#67E8F9", "#087A8A"),
    ("tailwindcss", "Tailwind CSS", "#56D8EE", "#067A8E"),
    ("reactquery", "React Query", "#FF8995", "#B52F49"),
]


def stack_tiles():
    for key, label, dark, light in STACK:
        root = ET.parse(ASSETS / "icons" / f"{key}.svg").getroot()
        paths = ''.join(f'<path d="{escape(el.attrib["d"], quote=True)}"/>' for el in root.iter() if el.tag.endswith("path"))
        for theme, p in PALETTES.items():
            color = dark if theme == "dark" else light
            body = f'<rect x=".5" y=".5" width="291" height="111" rx="20" fill="{p["panel"]}" stroke="{p["line"]}"/>'
            body += f'<g transform="translate(22 32) scale(2)" fill="{color}">{paths}</g>'
            body += text(88, 66, label, 25 if len(label) > 10 else 27, p['ink'], 600)
            write(f"stack/{key}-{theme}.svg", svg(292, 112, label, body))


def footer(theme):
    p = PALETTES[theme]
    body = f'<rect width="960" height="116" rx="20" fill="{p["bg"]}"/>'
    body += f'<path d="M30 0H930" stroke="{p["line"]}"/>'
    body += text(480, 54, "Build with intent. Ship with care.", 29, p['ink'], 600, 'text-anchor="middle"')
    body += text(480, 88, "MALLESH  /  @mallesh002", 16, p['muted'], 500, 'text-anchor="middle" letter-spacing="2"')
    write(f'footer-{theme}.svg', svg(960, 116, 'Build with intent. Ship with care. Mallesh / @mallesh002', body))


def intro(font_path=None):
    from PIL import Image, ImageDraw, ImageFont
    default = Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    font_path = Path(font_path) if font_path else default
    if not font_path.is_file():
        raise SystemExit('Supply a monospace TrueType font with --font /path/to/font.ttf')
    w, h, s = 720, 142, 2
    main = ImageFont.truetype(str(font_path), 31 * s)
    small = ImageFont.truetype(str(font_path), 16 * s)
    phrase = 'From API to interface.'
    def frame(n, cursor=False):
        im = Image.new('RGB', (w*s, h*s), '#0B1220')
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((1, 1, w*s-2, h*s-2), 18*s, fill='#0B1220', outline='#263952', width=2)
        for i, c in enumerate(['#FF9FA9','#F4CC7B','#7AE4B5']):
            x=(23+i*19)*s
            d.ellipse((x,20*s,x+7*s,27*s),fill=c)
        d.text((97*s,16*s),'mallesh / engineering',font=small,fill='#A6B6CC')
        d.line((20*s,49*s,700*s,49*s),fill='#263952',width=s)
        d.text((24*s,73*s),'>',font=main,fill='#67E8F9')
        d.text((63*s,73*s),phrase[:n],font=main,fill='#F1F6FF')
        if cursor:
            x=int(63*s+d.textlength(phrase[:n],font=main)+3*s)
            d.rectangle((x,79*s,x+2*s,111*s),fill='#B8A1FF')
        return im
    # The complete first frame also reads well in viewers that suppress animation.
    frames=[frame(len(phrase))]+[frame(i,True) for i in range(len(phrase)+1)]+[frame(len(phrase))]
    durations=[450]+[65]*(len(phrase)+1)+[1500]
    palette=frames[0].quantize(colors=64)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    # No loop extension: the animation runs once, then rests on the final sentence.
    indexed[0].save(ASSETS/'intro.gif',save_all=True,append_images=indexed[1:],duration=durations,optimize=True,disposal=1)
    p=PALETTES['dark']
    body=f'<rect x=".5" y=".5" width="719" height="141" rx="18" fill="{p["bg"]}" stroke="{p["line"]}"/>'
    for i,c in enumerate(['#FF9FA9','#F4CC7B','#7AE4B5']):
        body+=f'<circle cx="{27+i*19}" cy="24" r="3.5" fill="{c}"/>'
    body+=text(97,33,'mallesh / engineering',16,p['muted'])
    body+=f'<path d="M20 49H700" stroke="{p["line"]}"/>'
    body+=text(24,104,'> From API to interface.',31,p['ink'],500)
    write('intro-static.svg',svg(w,h,'From API to interface.',body))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--font',help='Path to a monospace TrueType font for the GIF')
    args=parser.parse_args()
    for theme in PALETTES:
        hero(theme)
        hero(theme,True)
        footer(theme)
    stack_tiles()
    intro(args.font)
    print('Rebuilt hero, stack tiles, footer, and one-shot intro GIF.')


if __name__=='__main__':
    main()
