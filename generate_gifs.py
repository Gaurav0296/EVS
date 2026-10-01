#!/usr/bin/env python3
"""Generates 4 high-quality animated GIFs from vector SVG frames.

Zero Python third-party packages required (uses standard library + ImageMagick/ffmpeg).
Generates:
  1. assets/1_sunrise_balloons.gif  - Morning Sunrise & Floating Balloons
  2. assets/2_floating_hearts.gif   - Afternoon Floating Hearts & Love Letter
  3. assets/3_birthday_cake.gif     - Evening Birthday Cake & Flickering Candles
  4. assets/4_starry_fireworks.gif  - Midnight Starry Sky & Fireworks Finale
"""

import math
import os
import random
import shutil
import subprocess
import tempfile

WIDTH, HEIGHT = 560, 320
FRAMES = 24


def render_svg_frames_to_gif(svg_frames, out_gif_path, fps=15):
  with tempfile.TemporaryDirectory() as tmpdir:
    png_paths = []
    for idx, svg_content in enumerate(svg_frames):
      svg_path = os.path.join(tmpdir, f"frame_{idx:03d}.svg")
      png_path = os.path.join(tmpdir, f"frame_{idx:03d}.png")
      with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
      subprocess.run(
          ["convert", "-background", "none", svg_path, png_path],
          check=True,
      )
      png_paths.append(png_path)

    if shutil.which("ffmpeg"):
      palette_path = os.path.join(tmpdir, "palette.png")
      subprocess.run(
          [
              "ffmpeg", "-y", "-framerate", str(fps),
              "-i", os.path.join(tmpdir, "frame_%03d.png"),
              "-vf", "palettegen=stats_mode=diff",
              palette_path,
          ],
          check=True,
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
      )
      subprocess.run(
          [
              "ffmpeg", "-y", "-framerate", str(fps),
              "-i", os.path.join(tmpdir, "frame_%03d.png"),
              "-i", palette_path,
              "-lavfi", "paletteuse=dither=bayer:bayer_scale=5",
              out_gif_path,
          ],
          check=True,
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
      )
    else:
      subprocess.run(
          ["convert", "-delay", str(int(100 / fps)), "-loop", "0"] + png_paths + [out_gif_path],
          check=True,
      )


def build_sunrise_balloons_frames():
  balloons = [
      {"x": 90, "phase": 0.00, "r": 28, "c1": "#ff758f", "c2": "#ff4d6d"},
      {"x": 165, "phase": 0.35, "r": 24, "c1": "#ffb703", "c2": "#fb8500"},
      {"x": 245, "phase": 0.70, "r": 31, "c1": "#c77dff", "c2": "#9d4edd"},
      {"x": 330, "phase": 0.18, "r": 26, "c1": "#ff8fa3", "c2": "#ff4d6d"},
      {"x": 410, "phase": 0.55, "r": 25, "c1": "#72efdd", "c2": "#48bfe3"},
      {"x": 475, "phase": 0.85, "r": 28, "c1": "#ffccd5", "c2": "#ff758f"},
  ]
  random.seed(42)
  sparkles = [
      (random.randint(40, WIDTH - 40), random.randint(25, HEIGHT - 60), random.random() * 6.28)
      for _ in range(16)
  ]

  frames = []
  for f in range(FRAMES):
    t = f / FRAMES
    angle = t * 2 * math.pi
    sun_y = 205 - 10 * math.sin(angle)
    sun_r = 72 + 4 * math.sin(angle * 2)

    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#fde2e4"/>
          <stop offset="55%" stop-color="#fff1e6"/>
          <stop offset="100%" stop-color="#fde4cf"/>
        </linearGradient>
        <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ffbe0b" stop-opacity="0.75"/>
          <stop offset="55%" stop-color="#fb5607" stop-opacity="0.25"/>
          <stop offset="100%" stop-color="#fb5607" stop-opacity="0"/>
        </radialGradient>
    ''']
    for idx, b in enumerate(balloons):
      parts.append(f'''
        <radialGradient id="bgrad{idx}" cx="35%" cy="30%" r="65%">
          <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>
          <stop offset="25%" stop-color="{b['c1']}"/>
          <stop offset="100%" stop-color="{b['c2']}"/>
        </radialGradient>
      ''')
    parts.append('</defs>')
    parts.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)" rx="16"/>')

    # Sun & glow
    parts.append(f'<circle cx="{WIDTH/2}" cy="{sun_y}" r="{sun_r*1.85:.1f}" fill="url(#sunGlow)"/>')
    parts.append(f'<circle cx="{WIDTH/2}" cy="{sun_y}" r="{sun_r:.1f}" fill="#ffCA3A" opacity="0.85"/>')

    # Soft morning clouds
    for cx, cy, rx, ry in [(115, 285, 95, 28), (285, 295, 135, 34), (455, 285, 105, 28)]:
      ox = 8 * math.sin(angle + cx * 0.02)
      parts.append(f'<ellipse cx="{cx+ox:.1f}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" opacity="0.75"/>')

    # Twinkling stars/sparkles
    for sx, sy, sp in sparkles:
      sc = 0.5 + 0.5 * math.sin(angle * 2 + sp)
      r = 2.0 + 4.0 * sc
      parts.append(
          f'<path d="M {sx} {sy-r} Q {sx} {sy} {sx+r} {sy} Q {sx} {sy} {sx} {sy+r} Q {sx} {sy} {sx-r} {sy} Q {sx} {sy} {sx} {sy-r} Z" fill="#ffb703" opacity="{0.35 + 0.65*sc:.2f}"/>'
      )

    # Floating balloons
    for idx, b in enumerate(balloons):
      prog = (t + b["phase"]) % 1.0
      by = HEIGHT + 55 - prog * (HEIGHT + 115)
      bx = b["x"] + 11 * math.sin(angle + b["phase"] * 6.28)
      r = b["r"]
      sway = 6 * math.cos(angle + b["phase"] * 6.28)
      # String
      parts.append(
          f'<path d="M {bx:.1f} {by+r+3:.1f} Q {bx+sway:.1f} {by+r+28:.1f} {bx-sway*0.6:.1f} {by+r+55:.1f}" stroke="#b5838d" stroke-width="1.8" fill="none" opacity="0.7"/>'
      )
      # Knot
      parts.append(
          f'<polygon points="{bx-4:.1f},{by+r+5:.1f} {bx+4:.1f},{by+r+5:.1f} {bx:.1f},{by+r-1:.1f}" fill="{b["c2"]}"/>'
      )
      # Balloon oval
      parts.append(
          f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{r}" ry="{r*1.15:.1f}" fill="url(#bgrad{idx})"/>'
      )

    parts.append('</svg>')
    frames.append("".join(parts))
  return frames


def build_floating_hearts_frames():
  random.seed(99)
  hearts = [
      {
          "x": 65 + i * 43,
          "phase": (i * 0.29) % 1.0,
          "scale": 0.65 + (i % 4) * 0.22,
          "sway": 10 + (i % 3) * 5,
          "color": ["#ff4d6d", "#ff758f", "#e05780", "#c9184a"][i % 4],
      }
      for i in range(11)
  ]

  frames = []
  for f in range(FRAMES):
    t = f / FRAMES
    angle = t * 2 * math.pi
    pulse = 1.0 + 0.08 * math.sin(angle * 2)
    env_y = HEIGHT / 2 + 12 + 6 * math.sin(angle)

    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
      <defs>
        <linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#fff0f3"/>
          <stop offset="50%" stop-color="#ffccd5"/>
          <stop offset="100%" stop-color="#ffe5ec"/>
        </linearGradient>
        <radialGradient id="aura" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ff4d6d" stop-opacity="0.28"/>
          <stop offset="100%" stop-color="#ff4d6d" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg2)" rx="16"/>
      <circle cx="{WIDTH/2}" cy="{HEIGHT/2}" r="{135*pulse:.1f}" fill="url(#aura)"/>
    ''']

    # Rising hearts
    for h in hearts:
      prog = (t + h["phase"]) % 1.0
      hy = HEIGHT + 30 - prog * (HEIGHT + 70)
      hx = h["x"] + h["sway"] * math.sin(angle + h["phase"] * 6.28)
      s = h["scale"]
      op = min(1.0, (1.0 - prog) * 2.2)
      parts.append(
          f'<g transform="translate({hx:.1f},{hy:.1f}) scale({s:.2f})" opacity="{op:.2f}">'
          f'<path d="M 0 8 C -12 -4 -22 6 -12 18 L 0 30 L 12 18 C 22 6 12 -4 0 8 Z" fill="{h["color"]}"/>'
          f'</g>'
      )

    # Central floating love letter
    cx = WIDTH / 2
    parts.append(f'''
      <g transform="translate({cx:.1f},{env_y:.1f})">
        <rect x="-72" y="-44" width="144" height="92" rx="12" fill="#e5989b" opacity="0.35" transform="translate(4,6)"/>
        <rect x="-72" y="-44" width="144" height="92" rx="12" fill="#ffffff" stroke="#ff758f" stroke-width="3"/>
        <path d="M -70 -41 L 0 12 L 70 -41" fill="none" stroke="#ff8fa3" stroke-width="3" stroke-linecap="round"/>
        <path d="M -70 45 L -22 4 M 70 45 L 22 4" fill="none" stroke="#ffccd5" stroke-width="2.5"/>
        <g transform="scale({pulse:.2f}) translate(0, -8)">
          <path d="M 0 4 C -10 -6 -20 3 -10 14 L 0 24 L 10 14 C 20 3 10 -6 0 4 Z" fill="#d90429"/>
        </g>
      </g>
    ''')

    parts.append('</svg>')
    frames.append("".join(parts))
  return frames


def build_birthday_cake_frames():
  random.seed(7)
  confetti = [
      {
          "x": random.randint(25, WIDTH - 25),
          "phase": random.random(),
          "color": random.choice(["#ff4d6d", "#ffbe0b", "#06d6a0", "#4cc9f0", "#c77dff", "#ff9ebb"]),
          "rot": random.randint(0, 180),
      }
      for _ in range(30)
  ]

  frames = []
  for f in range(FRAMES):
    t = f / FRAMES
    angle = t * 2 * math.pi
    cx = WIDTH / 2
    base_y = 272

    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
      <defs>
        <linearGradient id="bg3" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#2b193d"/>
          <stop offset="100%" stop-color="#4c2a69"/>
        </linearGradient>
        <radialGradient id="candleGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#ffbe0b" stop-opacity="0.55"/>
          <stop offset="100%" stop-color="#ffbe0b" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg3)" rx="16"/>
    ''']

    # Falling confetti
    for c in confetti:
      prog = (t + c["phase"]) % 1.0
      cy = -15 + prog * (HEIGHT + 30)
      qx = c["x"] + 12 * math.sin(angle + c["phase"] * 6.28)
      rot = c["rot"] + prog * 360
      parts.append(
          f'<rect x="-5" y="-3" width="10" height="6" rx="2" fill="{c["color"]}" transform="translate({qx:.1f},{cy:.1f}) rotate({rot:.0f})"/>'
      )

    # Cake stand & tiers
    parts.append(f'''
      <ellipse cx="{cx}" cy="{base_y+4}" rx="125" ry="14" fill="#e2e8f0"/>
      <ellipse cx="{cx}" cy="{base_y}" rx="110" ry="10" fill="#f8fafc"/>
      <!-- Bottom tier -->
      <rect x="{cx-95}" y="{base_y-78}" width="190" height="78" rx="12" fill="#ffafcc" stroke="#ff758f" stroke-width="2"/>
      <rect x="{cx-95}" y="{base_y-80}" width="190" height="18" rx="9" fill="#fff0f3"/>
    ''')
    for dx in range(int(cx - 78), int(cx + 82), 26):
      parts.append(f'<circle cx="{dx}" cy="{base_y-66}" r="13" fill="#fff0f3"/>')

    # Top tier
    parts.append(f'''
      <rect x="{cx-68}" y="{base_y-138}" width="136" height="62" rx="10" fill="#fde68a" stroke="#fbbf24" stroke-width="2"/>
      <rect x="{cx-68}" y="{base_y-140}" width="136" height="15" rx="7" fill="#fffbeb"/>
    ''')
    for dx in range(int(cx - 55), int(cx + 58), 22):
      parts.append(f'<circle cx="{dx}" cy="{base_y-128}" r="11" fill="#fffbeb"/>')
    for bx in range(int(cx - 52), int(cx + 56), 26):
      parts.append(f'<circle cx="{bx}" cy="{base_y-142}" r="6" fill="#e11d48"/>')

    # 3 Candles + flickering flames
    for i, kx in enumerate([cx - 36, cx, cx + 36]):
      ky_top = base_y - 182
      fx = kx + 2.5 * math.sin(angle * 3 + i * 2.1)
      fy = ky_top - 14 + 2.0 * math.cos(angle * 4 + i * 1.5)
      glow_r = 34 + 6 * math.sin(angle * 3 + i)
      parts.append(f'''
        <rect x="{kx-6}" y="{ky_top}" width="12" height="42" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
        <line x1="{kx-5}" y1="{ky_top+12}" x2="{kx+5}" y2="{ky_top+20}" stroke="#ff4d6d" stroke-width="3"/>
        <line x1="{kx-5}" y1="{ky_top+26}" x2="{kx+5}" y2="{ky_top+34}" stroke="#ff4d6d" stroke-width="3"/>
        <line x1="{kx}" y1="{ky_top-5}" x2="{kx}" y2="{ky_top}" stroke="#475569" stroke-width="2"/>
        <circle cx="{fx:.1f}" cy="{fy:.1f}" r="{glow_r:.1f}" fill="url(#candleGlow)"/>
        <path d="M {fx:.1f} {fy-15:.1f} Q {fx-10:.1f} {fy+4:.1f} {fx:.1f} {fy+10:.1f} Q {fx+10:.1f} {fy+4:.1f} {fx:.1f} {fy-15:.1f} Z" fill="#fb923c"/>
        <path d="M {fx:.1f} {fy-8:.1f} Q {fx-5:.1f} {fy+3:.1f} {fx:.1f} {fy+7:.1f} Q {fx+5:.1f} {fy+3:.1f} {fx:.1f} {fy-8:.1f} Z" fill="#fef08a"/>
      ''')

    parts.append('</svg>')
    frames.append("".join(parts))
  return frames


def build_starry_fireworks_frames():
  random.seed(123)
  stars = [
      (random.randint(18, WIDTH - 18), random.randint(18, HEIGHT - 40), random.random() * 6.28)
      for _ in range(42)
  ]
  bursts = [
      {"cx": 145, "cy": 115, "offset": 0.00, "color": "#ff4d6d", "sub": "#ffccd5", "max_r": 80},
      {"cx": 415, "cy": 105, "offset": 0.33, "color": "#ffbe0b", "sub": "#fef08a", "max_r": 84},
      {"cx": 280, "cy": 88, "offset": 0.66, "color": "#c77dff", "sub": "#e0aaff", "max_r": 90},
  ]

  frames = []
  for f in range(FRAMES):
    t = f / FRAMES
    angle = t * 2 * math.pi
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
      <defs>
        <linearGradient id="night" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#0b132b"/>
          <stop offset="60%" stop-color="#1c2541"/>
          <stop offset="100%" stop-color="#3a1c71"/>
        </linearGradient>
      </defs>
      <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#night)" rx="16"/>
      <!-- Crescent Moon -->
      <circle cx="490" cy="52" r="24" fill="#fef9c3"/>
      <circle cx="500" cy="46" r="22" fill="#101835"/>
    ''']

    for sx, sy, sp in stars:
      op = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(angle * 2 + sp))
      r = 2.0 if op > 0.75 else 1.2
      parts.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="#ffffff" opacity="{op:.2f}"/>')

    for burst in bursts:
      bt = (t + burst["offset"]) % 1.0
      r = bt * burst["max_r"]
      op = max(0.0, 1.0 - bt * 1.05)
      num_rays = 16
      for i in range(num_rays):
        theta = (i / num_rays) * 2 * math.pi
        x1 = burst["cx"] + math.cos(theta) * (r * 0.25)
        y1 = burst["cy"] + math.sin(theta) * (r * 0.25) + bt * bt * 18
        x2 = burst["cx"] + math.cos(theta) * r
        y2 = burst["cy"] + math.sin(theta) * r + bt * bt * 26
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{burst["color"]}" stroke-width="2.4" stroke-linecap="round" opacity="{op:.2f}"/>'
            f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3.2" fill="{burst["sub"]}" opacity="{op:.2f}"/>'
        )

    parts.append('</svg>')
    frames.append("".join(parts))
  return frames


def main():
  assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
  os.makedirs(assets_dir, exist_ok=True)

  jobs = [
      ("1_sunrise_balloons.gif", build_sunrise_balloons_frames()),
      ("2_floating_hearts.gif", build_floating_hearts_frames()),
      ("3_birthday_cake.gif", build_birthday_cake_frames()),
      ("4_starry_fireworks.gif", build_starry_fireworks_frames()),
  ]
  for filename, svg_frames in jobs:
    out_path = os.path.join(assets_dir, filename)
    render_svg_frames_to_gif(svg_frames, out_path)
    print(f"Generated {out_path} ({os.path.getsize(out_path) // 1024} KB)")


if __name__ == "__main__":
  main()
