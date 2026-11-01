"""Generates the demonstration illustration pairs (same wheel, same angle).
Not photographs. Replace with real Autochrome photo pairs (see README)."""
import math, random, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'img')
C = 400  # centre
DESIGNS = [
  # name, spokes, style, after-face colour stops, nut colour
  ("pair-1", 5, "fat",   ("#f4f6f8", "#b9c0c8", "#7d868f"), "Five-spoke wheel, silver finish"),
  ("pair-2", 10, "split", ("#6b7178", "#3d4248", "#24282c"), "Split ten-spoke wheel, gunmetal finish"),
  ("pair-3", 14, "thin", ("#2b2e33", "#16181b", "#0b0c0e"), "Multi-spoke wheel, gloss black finish"),
  ("pair-4", 6, "y",    ("#e8ebee", "#a9b1ba", "#666f78"), "Y-spoke wheel, bright silver finish"),
]
def spoke_paths(n, style):
    ps = []
    for i in range(n):
        a = 2*math.pi*i/n - math.pi/2
        def pt(r, da):
            return f"{C+r*math.cos(a+da):.1f},{C+r*math.sin(a+da):.1f}"
        if style == "fat":
            ps.append(f"M{pt(70,-0.26)} L{pt(262,-0.17)} Q{pt(272,0)} {pt(262,0.17)} L{pt(70,0.26)} Z")
        elif style == "split":
            for o in (-0.07, 0.07):
                ps.append(f"M{pt(70,o-0.09)} L{pt(264,o-0.035)} L{pt(264,o+0.035)} L{pt(70,o+0.09)} Z")
        elif style == "thin":
            ps.append(f"M{pt(68,-0.09)} L{pt(266,-0.03)} L{pt(266,0.03)} L{pt(68,0.09)} Z")
        else:  # y
            ps.append(f"M{pt(70,-0.2)} L{pt(160,-0.07)} L{pt(264,-0.2)} L{pt(264,-0.12)} L{pt(175,0)} L{pt(264,0.12)} L{pt(264,0.2)} L{pt(160,0.07)} L{pt(70,0.2)} Z")
    return ps
def wheel(design, before):
    name, n, style, stops, label = design
    rnd = random.Random(name)
    s0, s1, s2 = stops
    if before:  # dull, oxidised, desaturated lacquer
        s0, s1, s2 = ("#9ea19f", "#7f8380", "#5b5f5c") if s0 > "#8" else ("#5c5f5d", "#46494a", "#2f3132")
    spokes = "".join(f'<path d="{d}"/>' for d in spoke_paths(n, style))
    defs = f'''<defs>
<radialGradient id="tyre" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#2a2c2f"/><stop offset="1" stop-color="#0c0d0e"/></radialGradient>
<linearGradient id="face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{s0}"/><stop offset=".55" stop-color="{s1}"/><stop offset="1" stop-color="{s2}"/></linearGradient>
<linearGradient id="lip" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{'#c9ccca' if before else '#ffffff'}"/><stop offset=".5" stop-color="{'#6f7370' if before else '#8a939c'}"/><stop offset="1" stop-color="{'#a3a6a3' if before else '#e9eef2'}"/></linearGradient>
<radialGradient id="barrel" cx="50%" cy="50%" r="50%"><stop offset=".2" stop-color="#2a2d31"/><stop offset="1" stop-color="#050506"/></radialGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .3  0 0 0 0 .25  0 0 0 .55 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<clipPath id="wclip"><circle cx="{C}" cy="{C}" r="300"/></clipPath>
</defs>'''
    bg = f'<rect width="800" height="800" fill="#16181b"/><circle cx="{C}" cy="{C}" r="392" fill="url(#tyre)"/>'
    # tyre tread hints
    bg += "".join(f'<line x1="{C+360*math.cos(t):.1f}" y1="{C+360*math.sin(t):.1f}" x2="{C+388*math.cos(t):.1f}" y2="{C+388*math.sin(t):.1f}" stroke="#000" stroke-opacity=".35" stroke-width="5"/>' for t in [i*math.pi/36 for i in range(72)])
    w = f'<circle cx="{C}" cy="{C}" r="300" fill="url(#lip)"/><circle cx="{C}" cy="{C}" r="282" fill="url(#barrel)"/>'
    w += f'<circle cx="{C}" cy="{C}" r="288" fill="none" stroke="url(#face)" stroke-width="10"/>'
    w += f'<g fill="url(#face)" stroke="{'#000' if before else '#cfd6dd'}" stroke-opacity="{'.35' if before else '.35'}" stroke-width="2">{spokes}</g>'
    w += f'<circle cx="{C}" cy="{C}" r="80" fill="url(#face)" stroke="#000" stroke-opacity=".3" stroke-width="3"/>'
    w += f'<circle cx="{C}" cy="{C}" r="34" fill="#0e0f11"/><circle cx="{C}" cy="{C}" r="26" fill="{"#555" if before else "#c9ced3"}"/>'
    for i in range(5):
        a = 2*math.pi*i/5 + 0.3
        w += f'<circle cx="{C+56*math.cos(a):.1f}" cy="{C+56*math.sin(a):.1f}" r="8" fill="{"#6d6a63" if before else "#dfe3e7"}" stroke="#000" stroke-opacity=".5" stroke-width="2"/>'
    dmg = ""
    if before:
        # dull film over everything
        dmg += f'<circle cx="{C}" cy="{C}" r="300" fill="#8a8170" fill-opacity=".14"/>'
        # kerb rash on outer lip: jagged arcs
        for k in range(3):
            a0 = rnd.uniform(0, 2*math.pi); span = rnd.uniform(0.35, 0.8)
            pts = []
            steps = 26
            for j in range(steps+1):
                t = a0 + span*j/steps
                r = 300 - rnd.uniform(0, 14)
                pts.append(f"{C+r*math.cos(t):.1f},{C+r*math.sin(t):.1f}")
            for j in range(steps, -1, -1):
                t = a0 + span*j/steps
                pts.append(f"{C+301*math.cos(t):.1f},{C+301*math.sin(t):.1f}")
            dmg += f'<polygon points="{" ".join(pts)}" fill="#4a4740"/>'
            for j in range(18):
                t = a0 + rnd.uniform(0, span); r = rnd.uniform(286, 299)
                dmg += f'<line x1="{C+r*math.cos(t):.1f}" y1="{C+r*math.sin(t):.1f}" x2="{C+(r-rnd.uniform(4,12))*math.cos(t+0.01):.1f}" y2="{C+(r-rnd.uniform(4,12))*math.sin(t+0.01):.1f}" stroke="#d8d4c8" stroke-width="1.6" stroke-opacity=".8"/>'
        # corrosion blooms + lacquer peel
        for k in range(26):
            t = rnd.uniform(0, 2*math.pi); r = rnd.uniform(90, 280); sz = rnd.uniform(3, 11)
            dmg += f'<circle cx="{C+r*math.cos(t):.1f}" cy="{C+r*math.sin(t):.1f}" r="{sz:.1f}" fill="#efe6d2" fill-opacity="{rnd.uniform(.35,.7):.2f}"/>'
        for k in range(5):
            t = rnd.uniform(0, 2*math.pi); r = rnd.uniform(110, 240)
            x, y = C+r*math.cos(t), C+r*math.sin(t)
            dmg += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rnd.uniform(14,30):.1f}" ry="{rnd.uniform(6,14):.1f}" transform="rotate({rnd.uniform(0,180):.0f} {x:.1f} {y:.1f})" fill="#c8b48a" fill-opacity=".35" stroke="#e9e1cf" stroke-opacity=".5" stroke-width="1.5"/>'
        # brake dust
        dmg += f'<g clip-path="url(#wclip)"><circle cx="{C}" cy="{C}" r="300" fill="#3a3025" filter="url(#grain)" opacity=".4"/></g>'
    else:
        dmg += f'<circle cx="{C}" cy="{C}" r="300" fill="url(#gloss)"/>'
        dmg += f'<path d="M{C-250},{C-120} A280,280 0 0 1 {C-60},{C-275}" stroke="#fff" stroke-opacity=".7" stroke-width="5" fill="none" stroke-linecap="round"/>'
    title = f'{label} — {"before" if before else "after"} (demonstration illustration)'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" role="img"><title>{title}</title>{defs}{bg}{w}{dmg}</svg>'
for d in DESIGNS:
    for before in (True, False):
        with open(os.path.join(OUT, f'{d[0]}-{"before" if before else "after"}.svg'), 'w') as f:
            f.write(wheel(d, before))
print("done")
