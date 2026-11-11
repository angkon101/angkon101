import os
import json
import urllib.request
import math

def fetch_github_stats(username):
    stats = {
        'total_repos': 24,
        'followers': 9,
        'following': 7,
        'languages': {'Python': 5, 'TypeScript': 4, 'JavaScript': 3, 'Dart': 2, 'HTML/CSS': 6}
    }
    try:
        req = urllib.request.Request(
            f'https://api.github.com/users/{username}',
            headers={'User-Agent': 'Python-SVG-Gen'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            stats['total_repos'] = data.get('public_repos', stats['total_repos'])
            stats['followers'] = data.get('followers', stats['followers'])
            stats['following'] = data.get('following', stats['following'])
    except Exception as e:
        print(f"Using cached stats for profile: {e}")
        
    try:
        req = urllib.request.Request(
            f'https://api.github.com/users/{username}/repos?per_page=100',
            headers={'User-Agent': 'Python-SVG-Gen'}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            repos = json.loads(resp.read().decode())
            langs = {}
            for r in repos:
                l = r.get('language')
                if l:
                    langs[l] = langs.get(l, 0) + 1
            if langs:
                stats['languages'] = langs
    except Exception as e:
        print(f"Using cached repo languages: {e}")
        
    return stats

def iso_project(x, y, z, origin_x=440, origin_y=280):
    # Standard isometric: 30-degree angles
    cos30 = 0.866025
    sin30 = 0.5
    sx = origin_x + (x - y) * cos30
    sy = origin_y + (x + y) * sin30 - z
    return sx, sy

def make_iso_box(x, y, w, d, h, colors, origin_x=440, origin_y=280, id_prefix="box"):
    # 8 corners of a 3D box
    # Base: (x, y, 0), (x+w, y, 0), (x+w, y+d, 0), (x, y+d, 0)
    # Top: same + h
    p_back_base = iso_project(x, y, 0, origin_x, origin_y)
    p_right_base = iso_project(x + w, y, 0, origin_x, origin_y)
    p_front_base = iso_project(x + w, y + d, 0, origin_x, origin_y)
    p_left_base = iso_project(x, y + d, 0, origin_x, origin_y)
    
    p_back_top = iso_project(x, y, h, origin_x, origin_y)
    p_right_top = iso_project(x + w, y, h, origin_x, origin_y)
    p_front_top = iso_project(x + w, y + d, h, origin_x, origin_y)
    p_left_top = iso_project(x, y + d, h, origin_x, origin_y)
    
    svg = []
    
    # Shadow on the floor
    svg.append(f'  <!-- {id_prefix} floor shadow -->')
    pts_shadow = f"{p_back_base[0]:.1f},{p_back_base[1]:.1f} {p_right_base[0]:.1f},{p_right_base[1]:.1f} {p_front_base[0]:.1f},{p_front_base[1]:.1f} {p_left_base[0]:.1f},{p_left_base[1]:.1f}"
    svg.append(f'  <polygon points="{pts_shadow}" fill="rgba(0,0,0,0.5)" filter="url(#glow-soft)" />')
    
    # Left face (shaded dark)
    pts_left = f"{p_left_base[0]:.1f},{p_left_base[1]:.1f} {p_front_base[0]:.1f},{p_front_base[1]:.1f} {p_front_top[0]:.1f},{p_front_top[1]:.1f} {p_left_top[0]:.1f},{p_left_top[1]:.1f}"
    svg.append(f'  <polygon points="{pts_left}" fill="{colors["left"]}" stroke="{colors["stroke"]}" stroke-width="0.8" />')
    
    # Right face (medium shade)
    pts_right = f"{p_front_base[0]:.1f},{p_front_base[1]:.1f} {p_right_base[0]:.1f},{p_right_base[1]:.1f} {p_right_top[0]:.1f},{p_right_top[1]:.1f} {p_front_top[0]:.1f},{p_front_top[1]:.1f}"
    svg.append(f'  <polygon points="{pts_right}" fill="{colors["right"]}" stroke="{colors["stroke"]}" stroke-width="0.8" />')
    
    # Top face (illuminated)
    pts_top = f"{p_back_top[0]:.1f},{p_back_top[1]:.1f} {p_right_top[0]:.1f},{p_right_top[1]:.1f} {p_front_top[0]:.1f},{p_front_top[1]:.1f} {p_left_top[0]:.1f},{p_left_top[1]:.1f}"
    svg.append(f'  <polygon points="{pts_top}" fill="{colors["top"]}" stroke="{colors["top_stroke"]}" stroke-width="1.2" />')
    
    return "\n".join(svg), p_front_top, p_back_top

def generate_3d_analytics_svg(filename="analytics_3d.svg"):
    username = os.environ.get("GITHUB_ACTOR", "angkon101")
    stats = fetch_github_stats(username)
    
    width = 880
    height = 420
    
    svg = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <!-- Gradients -->',
        '    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#070a13" />',
        '      <stop offset="50%" stop-color="#0c1222" />',
        '      <stop offset="100%" stop-color="#060911" />',
        '    </linearGradient>',
        '    <linearGradient id="grid-fade" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.25" />',
        '      <stop offset="100%" stop-color="#00f0ff" stop-opacity="0.0" />',
        '    </linearGradient>',
        '    <linearGradient id="neon-cyan" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#00f0ff" />',
        '      <stop offset="100%" stop-color="#0072ff" />',
        '    </linearGradient>',
        '    <linearGradient id="neon-purple" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#e056fd" />',
        '      <stop offset="100%" stop-color="#6827b0" />',
        '    </linearGradient>',
        '    <linearGradient id="neon-gold" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#f9ca24" />',
        '      <stop offset="100%" stop-color="#f0932b" />',
        '    </linearGradient>',
        '    <linearGradient id="neon-green" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#2ed573" />',
        '      <stop offset="100%" stop-color="#10ac84" />',
        '    </linearGradient>',
        '    <linearGradient id="neon-coral" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#ff4757" />',
        '      <stop offset="100%" stop-color="#ff6b81" />',
        '    </linearGradient>',
        '    <!-- Glow Filters -->',
        '    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="3" result="blur" />',
        '      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>',
        '    <filter id="glow-soft" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="5" result="blur" />',
        '      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>',
        '  </defs>',
        '  <style>',
        '    .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 14px; font-weight: 700; fill: #00f0ff; letter-spacing: 2px; }',
        '    .subtitle { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; fill: #8b9bb4; }',
        '    .metric-val { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 15px; font-weight: 800; fill: #ffffff; }',
        '    .metric-lbl { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 9px; fill: #00f0ff; letter-spacing: 1px; font-weight: 600; text-transform: uppercase; }',
        '    .hud-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 10px; fill: #a5b4fc; }',
        '    .hud-bold { font-weight: 700; fill: #ffffff; }',
        '    .hud-accent { fill: #00f0ff; font-weight: 600; }',
        '    .grid-line { stroke: #1e293b; stroke-width: 1; stroke-opacity: 0.6; }',
        '    .iso-axis { stroke: #00f0ff; stroke-width: 1.2; stroke-dasharray: 4,4; stroke-opacity: 0.4; }',
        '    .hud-box { fill: rgba(15, 23, 42, 0.75); stroke: rgba(56, 189, 248, 0.25); stroke-width: 1; rx: 8; backdrop-filter: blur(8px); }',
        '    @keyframes pulseGlow { 0% { opacity: 0.4; } 50% { opacity: 0.9; } 100% { opacity: 0.4; } }',
        '    @keyframes floatUp { 0% { transform: translateY(0px); } 50% { transform: translateY(-7px); } 100% { transform: translateY(0px); } }',
        '    @keyframes spinRing { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }',
        '    @keyframes scanline { 0% { transform: translateY(0px); opacity: 0; } 50% { opacity: 0.8; } 100% { transform: translateY(400px); opacity: 0; } }',
        '    .floating-ring { animation: floatUp 3s ease-in-out infinite; }',
        '    .pulsing-node { animation: pulseGlow 2.5s ease-in-out infinite; }',
        '  </style>',
        '  <!-- Background -->',
        f'  <rect width="{width}" height="{height}" fill="url(#bg-grad)" rx="12" stroke="#1f293d" stroke-width="1.5" />',
        '  <!-- Cyberpunk Scanline -->',
        f'  <line x1="10" y1="20" x2="{width-10}" y2="20" stroke="#00f0ff" stroke-width="1" opacity="0.15">',
        '    <animate attributeName="y1" values="20;400;20" dur="8s" repeatCount="indefinite" />',
        '    <animate attributeName="y2" values="20;400;20" dur="8s" repeatCount="indefinite" />',
        '  </line>'
    ]
    
    # 3D Isometric Floor Grid
    origin_x = 450
    origin_y = 295
    grid_size = 5
    cell_w = 42
    
    svg.append('  <!-- 3D Isometric Grid Floor -->')
    svg.append('  <g class="grid-layer">')
    for i in range(-grid_size, grid_size + 1):
        x1, y1 = iso_project(i * cell_w, -grid_size * cell_w, 0, origin_x, origin_y)
        x2, y2 = iso_project(i * cell_w, grid_size * cell_w, 0, origin_x, origin_y)
        svg.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="grid-line" />')
        
        x3, y3 = iso_project(-grid_size * cell_w, i * cell_w, 0, origin_x, origin_y)
        x4, y4 = iso_project(grid_size * cell_w, i * cell_w, 0, origin_x, origin_y)
        svg.append(f'    <line x1="{x3:.1f}" y1="{y3:.1f}" x2="{x4:.1f}" y2="{y4:.1f}" class="grid-line" />')
    svg.append('  </g>')
    
    # 5 3D Isometric Pillars
    # Defined with coordinates (x, y), dimensions (w, d, h), and styling
    pillars = [
        {
            'name': 'Python & ML',
            'val': f"{stats['languages'].get('Python', 5)} Repos",
            'x': -130, 'y': -40, 'w': 38, 'd': 38, 'h': 135,
            'colors': {
                'left': '#3b1c6e', 'right': '#5c2d91', 'top': 'url(#neon-purple)',
                'stroke': '#9d4edd', 'top_stroke': '#e0aaff'
            },
            'glow': '#e056fd',
            'icon': '🐍'
        },
        {
            'name': 'Flutter & Dart',
            'val': f"{stats['languages'].get('Dart', 2)} Apps",
            'x': -65, 'y': -20, 'w': 38, 'd': 38, 'h': 115,
            'colors': {
                'left': '#0d3b66', 'right': '#1d5a91', 'top': 'url(#neon-cyan)',
                'stroke': '#00b4d8', 'top_stroke': '#90e0ef'
            },
            'glow': '#00f0ff',
            'icon': '📱'
        },
        {
            'name': 'TypeScript',
            'val': f"{stats['languages'].get('TypeScript', 4)} Repos",
            'x': 5, 'y': 0, 'w': 38, 'd': 38, 'h': 155,
            'colors': {
                'left': '#594406', 'right': '#856404', 'top': 'url(#neon-gold)',
                'stroke': '#ffc107', 'top_stroke': '#ffea79'
            },
            'glow': '#f9ca24',
            'icon': '⚡'
        },
        {
            'name': 'Total Repos',
            'val': f"{stats['total_repos']}",
            'x': 75, 'y': 20, 'w': 38, 'd': 38, 'h': 175,
            'colors': {
                'left': '#0f4c3a', 'right': '#167357', 'top': 'url(#neon-green)',
                'stroke': '#2ed573', 'top_stroke': '#7bed9f'
            },
            'glow': '#2ed573',
            'icon': '📦'
        },
        {
            'name': 'Bohuvuj Impact',
            'val': 'CEO / Founder',
            'x': 145, 'y': 40, 'w': 38, 'd': 38, 'h': 190,
            'colors': {
                'left': '#54121a', 'right': '#7d1e28', 'top': 'url(#neon-coral)',
                'stroke': '#ff4757', 'top_stroke': '#ff7a8a'
            },
            'glow': '#ff4757',
            'icon': '🚀'
        }
    ]
    
    # Render Pillars in correct back-to-front depth order
    # (x + y determines painter's order in isometric view)
    pillars_sorted = sorted(pillars, key=lambda p: (p['x'] + p['y']))
    
    svg.append('  <!-- 3D Pillars -->')
    for idx, p in enumerate(pillars_sorted):
        box_svg, p_front_top, p_back_top = make_iso_box(
            p['x'], p['y'], p['w'], p['d'], p['h'],
            p['colors'], origin_x, origin_y, p['name']
        )
        svg.append(box_svg)
        
        # Center of top face
        cx = (p_front_top[0] + p_back_top[0]) / 2
        cy = (p_front_top[1] + p_back_top[1]) / 2
        
        # Floating Holographic Data Halo above top
        anim_delay = idx * 0.4
        svg.append(f'  <!-- Halo for {p["name"]} -->')
        svg.append(f'  <g transform="translate(0, 0)">')
        # Hovering animation group
        svg.append(f'    <g>')
        svg.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="3s" begin="{anim_delay}s" repeatCount="indefinite" />')
        # Ellipse halo
        svg.append(f'      <ellipse cx="{cx:.1f}" cy="{cy-12:.1f}" rx="22" ry="10" fill="none" stroke="{p["glow"]}" stroke-width="1.4" opacity="0.8" stroke-dasharray="6,4">')
        svg.append(f'        <animate attributeName="stroke-dashoffset" from="0" to="20" dur="2s" repeatCount="indefinite" />')
        svg.append(f'      </ellipse>')
        # Glowing center energy core
        svg.append(f'      <circle cx="{cx:.1f}" cy="{cy-12:.1f}" r="3" fill="{p["glow"]}" filter="url(#glow-cyan)" />')
        # Pillar Label & Value
        svg.append(f'      <text x="{cx:.1f}" y="{cy-28:.1f}" text-anchor="middle" class="metric-val" fill="{p["glow"]}">{p["val"]}</text>')
        svg.append(f'      <text x="{cx:.1f}" y="{cy-42:.1f}" text-anchor="middle" class="metric-lbl">{p["name"]}</text>')
        svg.append(f'    </g>')
        svg.append(f'  </g>')
    
    # Top HUD Bar
    svg.append('  <!-- Top HUD Status -->')
    svg.append('  <g transform="translate(30, 32)">')
    # Glowing status dot
    svg.append('    <circle cx="6" cy="6" r="4" fill="#00f0ff" filter="url(#glow-cyan)">')
    svg.append('      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite" />')
    svg.append('    </circle>')
    svg.append('    <text x="18" y="10" class="title">3D LIVE ANALYTICS ENGINE // V2.6</text>')
    svg.append('    <text x="18" y="26" class="subtitle">ENGINEERING PORTFOLIO TELEMETRY &bull; ANGKON NATH (@angkon101)</text>')
    svg.append('  </g>')
    
    # Left HUD Box: Core Diagnostics
    svg.append('  <!-- Left HUD Glass Panel -->')
    svg.append('  <rect x="30" y="75" width="180" height="200" class="hud-box" />')
    svg.append('  <g transform="translate(45, 98)">')
    svg.append('    <text x="0" y="0" class="hud-accent" font-size="11">SYSTEM TELEMETRY</text>')
    svg.append('    <line x1="0" y1="8" x2="150" y2="8" stroke="rgba(56,189,248,0.2)" stroke-width="1" />')
    
    svg.append('    <text x="0" y="28" class="hud-text">STATUS: <tspan class="hud-accent">ACTIVE</tspan></text>')
    svg.append('    <text x="0" y="48" class="hud-text">PRIMARY: <tspan class="hud-bold">FULLSTACK &amp; ML</tspan></text>')
    svg.append('    <text x="0" y="68" class="hud-text">VENTURE: <tspan class="hud-bold">Bohuvuj.com</tspan></text>')
    svg.append('    <text x="0" y="88" class="hud-text">LOCATION: <tspan class="hud-bold">Dhaka, BD</tspan></text>')
    svg.append('    <text x="0" y="108" class="hud-text">TOTAL REPOS: <tspan class="hud-accent">24+</tspan></text>')
    
    # Soundwave / Activity Equalizer Bars
    svg.append('    <g transform="translate(0, 130)">')
    for bar_idx in range(12):
        bx = bar_idx * 12
        h_vals = f"{10 + (bar_idx * 2)};{28 - (bar_idx % 4)*4};{14 + (bar_idx % 3)*5};{10 + (bar_idx * 2)}"
        dur = f"{1.2 + (bar_idx % 4) * 0.3}s"
        svg.append(f'      <rect x="{bx}" y="0" width="6" height="20" fill="#00f0ff" rx="2" opacity="0.7">')
        svg.append(f'        <animate attributeName="height" values="{h_vals}" dur="{dur}" repeatCount="indefinite" />')
        svg.append(f'        <animate attributeName="y" values="0;{-6 + (bar_idx%3)*2};0" dur="{dur}" repeatCount="indefinite" />')
        svg.append(f'      </rect>')
    svg.append('    </g>')
    svg.append('  </g>')

    # Right HUD Box: Technology Radar & Mastery
    svg.append('  <!-- Right HUD Glass Panel -->')
    svg.append(f'  <rect x="{width-210}" y="75" width="180" height="200" class="hud-box" />')
    svg.append(f'  <g transform="translate({width-195}, 98)">')
    svg.append('    <text x="0" y="0" class="hud-accent" font-size="11">STACK PROFICIENCY</text>')
    svg.append('    <line x1="0" y1="8" x2="150" y2="8" stroke="rgba(56,189,248,0.2)" stroke-width="1" />')
    
    skills = [
        ('Flutter / Mobile', '95%', '#00f0ff'),
        ('Python / AI / ML', '92%', '#e056fd'),
        ('TypeScript / React', '88%', '#f9ca24'),
        ('Backend & Cloud', '85%', '#2ed573')
    ]
    for s_idx, (s_name, s_pct, s_col) in enumerate(skills):
        sy = 28 + s_idx * 34
        svg.append(f'    <text x="0" y="{sy}" class="hud-text">{s_name}</text>')
        svg.append(f'    <text x="150" y="{sy}" text-anchor="end" class="hud-bold" fill="{s_col}">{s_pct}</text>')
        # Progress Bar
        svg.append(f'    <rect x="0" y="{sy+6}" width="150" height="4" fill="rgba(255,255,255,0.1)" rx="2" />')
        svg.append(f'    <rect x="0" y="{sy+6}" width="{int(150 * int(s_pct.replace("%","")) / 100)}" height="4" fill="{s_col}" rx="2">')
        svg.append(f'      <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite" />')
        svg.append(f'    </rect>')
    svg.append('  </g>')

    # Bottom Ticker
    svg.append('  <!-- Bottom Cyber Ticker -->')
    svg.append(f'  <g transform="translate(30, {height-18})">')
    svg.append('    <text class="hud-text" font-size="10" fill="#475569">')
    svg.append('      [▲ DATA STREAM ONLINE] &bull; ARCHITECTURE: SCALABLE &bull; HIGH PERFORMANCE COMPUTING &bull; AUTO-SYNC')
    svg.append('    </text>')
    svg.append('  </g>')
    svg.append(f'  <g transform="translate({width-210}, {height-18})">')
    svg.append('    <text class="hud-accent" font-size="10" text-anchor="start">')
    svg.append('      INTERACTIVE 3D PROJECTION')
    svg.append('    </text>')
    svg.append('  </g>')

    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated 3D Analytics SVG -> {filename}")

if __name__ == "__main__":
    generate_3d_analytics_svg()
