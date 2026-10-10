"""Generate illustrated sample images for the Petoria seed (macOS: qlmanage rasterizes SVG, sips converts to JPEG).

Usage: python3 scripts/seed/generate-images.py
Output: scripts/seed/images/*.jpg (committed, so the seed itself does not need macOS).
"""

import json
import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'images')
SIZE = 800

TYPE_BG = {
    'PET': ('#EB6753', '#F6A77B'),
    'FOOD': ('#3A86FF', '#5FC4E8'),
    'TOY': ('#8E44AD', '#D16BA5'),
    'ACCESSORY': ('#2A9D8F', '#8AB17D'),
}
ALT_BG = {
    'PET': ('#F2A65A', '#F2C14E'),
    'FOOD': ('#5FA8E8', '#9AD0EC'),
    'TOY': ('#D16BA5', '#F6A77B'),
    'ACCESSORY': ('#8AB17D', '#E9C46A'),
}
FUR = {
    'DOG': ['#D9A066', '#8B5A2B', '#F2D0A4', '#C97B3A'],
    'CAT': ['#5C5C5C', '#E8E8E8', '#F2A65A', '#8B7D6B'],
    'BIRD': ['#5FA8E8', '#F2C14E', '#7BC47F', '#E86A5F'],
    'FISH': ['#F08A24', '#5FA8E8', '#E85D8F', '#F2C14E'],
}


def shade(hex_color, factor):
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    f = lambda c: max(0, min(255, int(c + (255 - c) * factor if factor > 0 else c * (1 + factor))))
    return '#%02X%02X%02X' % (f(r), f(g), f(b))


def dog(c):
    d = shade(c, -0.35)
    return f'''
<ellipse cx="-88" cy="-10" rx="38" ry="78" fill="{d}" transform="rotate(18 -88 -10)"/>
<ellipse cx="88" cy="-10" rx="38" ry="78" fill="{d}" transform="rotate(-18 88 -10)"/>
<circle r="100" fill="{c}"/>
<ellipse cy="42" rx="58" ry="44" fill="{shade(c, 0.55)}"/>
<circle cx="-38" cy="-18" r="12" fill="#1F1F24"/><circle cx="38" cy="-18" r="12" fill="#1F1F24"/>
<circle cx="-34" cy="-22" r="4" fill="#fff"/><circle cx="42" cy="-22" r="4" fill="#fff"/>
<ellipse cy="20" rx="19" ry="13" fill="#1F1F24"/>
<path d="M-16 44 Q0 58 16 44" stroke="#1F1F24" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cy="62" rx="10" ry="13" fill="#F28B9B"/>'''


def cat(c):
    d = shade(c, -0.3)
    return f'''
<path d="M-92 -30 L-78 -128 L-18 -88 Z" fill="{d}"/><path d="M92 -30 L78 -128 L18 -88 Z" fill="{d}"/>
<path d="M-78 -50 L-72 -106 L-38 -84 Z" fill="#F7B6C2"/><path d="M78 -50 L72 -106 L38 -84 Z" fill="#F7B6C2"/>
<ellipse rx="108" ry="94" fill="{c}"/>
<ellipse cx="-40" cy="-10" rx="14" ry="18" fill="#7BC47F"/><ellipse cx="40" cy="-10" rx="14" ry="18" fill="#7BC47F"/>
<ellipse cx="-40" cy="-10" rx="5" ry="15" fill="#1F1F24"/><ellipse cx="40" cy="-10" rx="5" ry="15" fill="#1F1F24"/>
<path d="M-10 20 L10 20 L0 32 Z" fill="#F28B9B"/>
<path d="M0 32 Q-12 46 -26 38 M0 32 Q12 46 26 38" stroke="#1F1F24" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M-40 26 H-110 M-40 36 L-104 50 M40 26 H110 M40 36 L104 50" stroke="{shade(c, -0.5)}" stroke-width="3" stroke-linecap="round"/>'''


def bird(c):
    return f'''
<ellipse cx="-14" cy="-102" rx="9" ry="22" fill="{shade(c, -0.3)}" transform="rotate(-20 -14 -102)"/>
<ellipse cx="6" cy="-104" rx="9" ry="24" fill="{shade(c, -0.3)}" transform="rotate(10 6 -104)"/>
<circle cy="10" r="96" fill="{c}"/>
<ellipse cy="48" rx="62" ry="46" fill="{shade(c, 0.55)}"/>
<ellipse cx="58" cy="26" rx="34" ry="56" fill="{shade(c, -0.25)}" transform="rotate(-22 58 26)"/>
<circle cx="-30" cy="-22" r="13" fill="#1F1F24"/><circle cx="-26" cy="-26" r="4" fill="#fff"/>
<path d="M-90 -6 L-140 10 L-90 26 Z" fill="#F2A65A"/>
<path d="M-24 104 V128 M24 104 V128" stroke="#F2A65A" stroke-width="7" stroke-linecap="round"/>'''


def fish(c):
    d = shade(c, -0.3)
    return f'''
<path d="M88 0 L170 -62 L158 0 L170 62 Z" fill="{d}"/>
<path d="M-10 -66 Q30 -120 70 -60 Z" fill="{d}"/>
<ellipse rx="118" ry="74" fill="{c}"/>
<path d="M-10 -70 Q-30 0 -10 70 M30 -66 Q12 0 30 66" stroke="{shade(c, 0.4)}" stroke-width="10" fill="none" opacity="0.7"/>
<circle cx="-62" cy="-14" r="15" fill="#fff"/><circle cx="-62" cy="-14" r="8" fill="#1F1F24"/>
<path d="M-112 14 Q-98 24 -86 14" stroke="#1F1F24" stroke-width="4" fill="none" stroke-linecap="round"/>
<circle cx="-150" cy="-70" r="12" fill="none" stroke="#fff" stroke-width="4" opacity="0.8"/>
<circle cx="-172" cy="-112" r="8" fill="none" stroke="#fff" stroke-width="3" opacity="0.7"/>'''


ANIMALS = {'DOG': dog, 'CAT': cat, 'BIRD': bird, 'FISH': fish}


def bowl(accent):
    return f'''
<ellipse cy="-6" rx="138" ry="40" fill="#8B5A2B"/>
<g fill="#C97B3A"><circle cx="-60" cy="-22" r="16"/><circle cx="-24" cy="-34" r="16"/><circle cx="14" cy="-30" r="16"/>
<circle cx="52" cy="-22" r="16"/><circle cx="-6" cy="-12" r="16"/><circle cx="30" cy="-10" r="15"/><circle cx="-40" cy="-8" r="15"/></g>
<path d="M-150 0 H150 Q140 118 0 122 Q-140 118 -150 0 Z" fill="{accent}"/>
<path d="M-142 34 H142" stroke="#fff" stroke-width="10" opacity="0.6"/>'''


def toy(accent):
    return f'''
<circle r="112" fill="{accent}"/>
<path d="M-112 0 Q0 -60 112 0 M-112 0 Q0 60 112 0" stroke="#fff" stroke-width="10" fill="none"/>
<path d="M0 -112 Q-50 0 0 112" stroke="#fff" stroke-width="10" fill="none" opacity="0.6"/>
<circle cx="-42" cy="-48" r="18" fill="#fff" opacity="0.5"/>'''


def accessory(accent):
    return f'''
<ellipse rx="128" ry="80" fill="none" stroke="{accent}" stroke-width="34"/>
<ellipse rx="128" ry="80" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="10 12" opacity="0.7"/>
<rect x="-26" y="62" width="52" height="34" rx="8" fill="#F2C14E"/>
<circle cy="132" r="34" fill="#F2C14E"/><circle cy="132" r="16" fill="#fff" opacity="0.7"/>'''


ITEMS = {'FOOD': bowl, 'TOY': toy, 'ACCESSORY': accessory}
ITEM_ACCENT = {'FOOD': '#FFFFFF', 'TOY': '#F2C14E', 'ACCESSORY': '#E86A5F'}


def paws(opacity):
    spots = [(90, 110, -20), (690, 140, 20), (140, 660, 30), (650, 690, -25), (400, 90, 0), (60, 400, 15), (740, 420, -10)]
    out = []
    for x, y, r in spots:
        out.append(
            f'<g transform="translate({x} {y}) rotate({r}) scale(2.2)" fill="#fff" fill-opacity="{opacity}">'
            '<ellipse cx="-7" cy="-3" rx="2.6" ry="3.3"/><ellipse cx="-2.6" cy="-8" rx="2.8" ry="3.6"/>'
            '<ellipse cx="2.6" cy="-8" rx="2.8" ry="3.6"/><ellipse cx="7" cy="-3" rx="2.6" ry="3.3"/>'
            '<path d="M0 9C-5.6 5.2-7.4 2-5.4-0.6C-3.8-2.6-1.2-2.2 0 -0.2C1.2-2.2 3.8-2.6 5.4-0.6C7.4 2 5.6 5.2 0 9Z"/></g>'
        )
    return ''.join(out)


def svg(body, bg):
    a, b = bg
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<rect width="{SIZE}" height="{SIZE}" fill="url(#bg)"/>
<circle cx="620" cy="160" r="220" fill="#fff" fill-opacity="0.12"/>
<circle cx="160" cy="680" r="180" fill="#fff" fill-opacity="0.1"/>
{paws(0.16)}
{body}
</svg>'''


def product_svg(ptype, species, variant):
    color = FUR[species][variant % len(FUR[species])]
    animal = ANIMALS[species](color)
    bg = TYPE_BG[ptype] if variant % 2 == 0 else ALT_BG[ptype]
    if ptype == 'PET':
        body = f'<g transform="translate(400 420) scale(2.3)">{animal}</g>'
    else:
        item = ITEMS[ptype](ITEM_ACCENT[ptype])
        body = (f'<ellipse cx="400" cy="700" rx="230" ry="26" fill="#000" fill-opacity="0.12"/>'
                f'<g transform="translate(400 520) scale(1.45)">{item}</g>'
                f'<g transform="translate({250 if variant % 2 else 560} 230) scale(1.05)">{animal}</g>')
    return svg(body, bg)


def avatar_svg(species, variant):
    color = FUR[species][variant % len(FUR[species])]
    bg = list(TYPE_BG.values())[variant % 4]
    return svg(f'<g transform="translate(400 420) scale(2.4)">{ANIMALS[species](color)}</g>', bg)


def rasterize(svg_text, name, tmp):
    src = os.path.join(tmp, f'{name}.svg')
    with open(src, 'w') as f:
        f.write(svg_text)
    subprocess.run(['qlmanage', '-t', '-s', str(SIZE), '-o', tmp, src], check=True, capture_output=True)
    subprocess.run(
        ['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', '-Z', str(SIZE),
         os.path.join(tmp, f'{name}.svg.png'), '--out', os.path.join(OUT, f'{name}.jpg')],
        check=True, capture_output=True)


def main():
    data = json.load(open(os.path.join(HERE, 'data.json')))
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for i, p in enumerate(data['products']):
            for v in range(2):
                rasterize(product_svg(p['productType'], p['productSpecies'], i + v), f"{p['key']}-{v + 1}", tmp)
        for i, m in enumerate(data['members']):
            rasterize(avatar_svg(m['avatar'], i), f"avatar-{m['memberNick']}", tmp)
        for i, a in enumerate(data['articles']):
            species = a['image']
            ptype = ['PET', 'TOY', 'FOOD', 'ACCESSORY'][i % 4]
            rasterize(product_svg(ptype, species, i), f'article-{i + 1}', tmp)
    print('images written to', OUT)


if __name__ == '__main__':
    main()
