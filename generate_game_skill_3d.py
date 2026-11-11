import math

def generate_shooting_game_svg(filename="game_skill_3d.svg"):
    width = 880
    height = 440
    
    svg = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <!-- Background Gradients -->',
        '    <linearGradient id="space-bg" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#030611" />',
        '      <stop offset="60%" stop-color="#080e22" />',
        '      <stop offset="100%" stop-color="#02040a" />',
        '    </linearGradient>',
        '    <linearGradient id="laser-cyan" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#ffffff" />',
        '      <stop offset="30%" stop-color="#00f0ff" />',
        '      <stop offset="100%" stop-color="rgba(0,240,255,0)" />',
        '    </linearGradient>',
        '    <linearGradient id="laser-magenta" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#ffffff" />',
        '      <stop offset="30%" stop-color="#ff007f" />',
        '      <stop offset="100%" stop-color="rgba(255,0,127,0)" />',
        '    </linearGradient>',
        '    <linearGradient id="hull-grad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="50%" stop-color="#1e293b" />',
        '      <stop offset="100%" stop-color="#0f172a" />',
        '    </linearGradient>',
        '    <linearGradient id="shield-grad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.3" />',
        '      <stop offset="100%" stop-color="#7000ff" stop-opacity="0.05" />',
        '    </linearGradient>',
        '    <linearGradient id="hp-grad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#00ff88" />',
        '      <stop offset="100%" stop-color="#00f0ff" />',
        '    </linearGradient>',
        '    <linearGradient id="crit-grad" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#ff0055" />',
        '      <stop offset="100%" stop-color="#ffb703" />',
        '    </linearGradient>',
        '    <!-- Glow Filters -->',
        '    <filter id="neon-glow" x="-30%" y="-30%" width="160%" height="160%">',
        '      <feGaussianBlur stdDeviation="4" result="blur" />',
        '      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>',
        '    <filter id="hyper-glow" x="-50%" y="-50%" width="200%" height="200%">',
        '      <feGaussianBlur stdDeviation="8" result="blur1" />',
        '      <feGaussianBlur stdDeviation="3" result="blur2" />',
        '      <feMerge><feMergeNode in="blur1" /><feMergeNode in="blur2" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>',
        '  </defs>',
        '  <style>',
        '    .hud-header { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 11px; font-weight: 800; fill: #00f0ff; letter-spacing: 2px; }',
        '    .hud-stat { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 10px; fill: #94a3b8; }',
        '    .hud-val { font-weight: 800; fill: #ffffff; }',
        '    .score-title { font-family: monospace; font-size: 9px; fill: #ffb703; letter-spacing: 1.5px; }',
        '    .score-num { font-family: monospace; font-size: 18px; font-weight: 900; fill: #ff0055; filter: drop-shadow(0 0 4px #ff0055); }',
        '    .skill-title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", monospace; font-size: 10px; font-weight: 800; fill: #ffffff; letter-spacing: 1px; text-anchor: middle; }',
        '    .skill-sub { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-size: 8px; font-weight: 700; fill: #00f0ff; text-anchor: middle; letter-spacing: 0.5px; }',
        '    .crit-text { font-family: monospace; font-size: 11px; font-weight: 900; fill: #ff0055; text-anchor: middle; }',
        '    .hud-panel { fill: rgba(10, 15, 30, 0.7); stroke: rgba(0, 240, 255, 0.3); stroke-width: 1; rx: 6; }',
        '  </style>',
        '  <!-- Background Canvas -->',
        f'  <rect width="{width}" height="{height}" fill="url(#space-bg)" rx="12" stroke="#1e293b" stroke-width="1.5" />',
        '  <!-- 3D Warp Perspective Floor Grid -->',
        '  <g opacity="0.35">'
    ]
    
    # 3D Perspective Grid Vanishing to center horizon
    vx, vy = 440, 160
    for i in range(-12, 13):
        x_bottom = 440 + i * 55
        svg.append(f'    <line x1="{vx}" y1="{vy}" x2="{x_bottom}" y2="{height}" stroke="#00f0ff" stroke-width="0.8" opacity="0.5" />')
        
    for d in [10, 25, 45, 75, 115, 165, 230]:
        y_pos = vy + d
        svg.append(f'    <line x1="0" y1="{y_pos}" x2="{width}" y2="{y_pos}" stroke="#7000ff" stroke-width="0.8" opacity="0.4">')
        svg.append(f'      <animate attributeName="opacity" values="0.2;0.6;0.2" dur="3s" repeatCount="indefinite" />')
        svg.append(f'    </line>')
    svg.append('  </g>')
    
    # Floating Stars / Hyperdrive Warp Particles
    svg.append('  <!-- Warp Dust Particles -->')
    stars = [(120, 80), (280, 50), (620, 70), (760, 110), (200, 220), (680, 240), (350, 90), (510, 95)]
    for sx, sy in stars:
        svg.append(f'  <circle cx="{sx}" cy="{sy}" r="1.5" fill="#00f0ff" opacity="0.8">')
        svg.append(f'    <animate attributeName="r" values="1;2.5;1" dur="{2 + (sx%3)}s" repeatCount="indefinite" />')
        svg.append(f'    <animate attributeName="opacity" values="0.3;1;0.3" dur="{1.5 + (sy%2)}s" repeatCount="indefinite" />')
        svg.append(f'  </circle>')
        
    # 5 3D Hexagonal / Holographic Skill Target Bosses
    targets = [
        {
            'id': 'flutter', 'name': 'FLUTTER & DART', 'lvl': 'LVL 96 - S-TIER',
            'sub': 'MOBILE ARCHITECTURE', 'x': 170, 'y': 150, 'hp': 96,
            'color': '#00f0ff', 'glow': 'rgba(0,240,255,0.4)', 'crit': '+960 XP', 'icon': '📱'
        },
        {
            'id': 'python', 'name': 'PYTHON & AI / ML', 'lvl': 'LVL 95 - S-TIER',
            'sub': 'NEURAL COMPUTING', 'x': 310, 'y': 105, 'hp': 95,
            'color': '#a855f7', 'glow': 'rgba(168,85,247,0.4)', 'crit': '+1250 CRIT!', 'icon': '🧠'
        },
        {
            'id': 'founder', 'name': 'BOHUVUJ.COM', 'lvl': 'LVL 99 - SUPREME BOSS',
            'sub': 'CO-FOUNDER & CEO', 'x': 440, 'y': 70, 'hp': 100,
            'color': '#ff0055', 'glow': 'rgba(255,0,85,0.6)', 'crit': 'MAX OVERDRIVE!', 'icon': '👑'
        },
        {
            'id': 'typescript', 'name': 'TYPESCRIPT & REACT', 'lvl': 'LVL 92 - A-TIER',
            'sub': 'FULLSTACK PLATFORM', 'x': 570, 'y': 105, 'hp': 92,
            'color': '#ffb703', 'glow': 'rgba(255,183,3,0.4)', 'crit': '+880 XP', 'icon': '⚡'
        },
        {
            'id': 'cloud', 'name': 'SYSTEMS & SQL', 'lvl': 'LVL 88 - A-TIER',
            'sub': 'CLOUD & DATABASE', 'x': 710, 'y': 150, 'hp': 88,
            'color': '#00ff88', 'glow': 'rgba(0,255,136,0.4)', 'crit': '+720 XP', 'icon': '🛡️'
        }
    ]
    
    svg.append('  <!-- 3D Target Nodes -->')
    for idx, t in enumerate(targets):
        tx, ty = t['x'], t['y']
        c = t['color']
        
        svg.append(f'  <!-- Target: {t["name"]} -->')
        svg.append(f'  <g transform="translate({tx}, {ty})">')
        # Floating Bobbing Animation
        svg.append(f'    <g>')
        svg.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="{3 + (idx%3)*0.5}s" repeatCount="indefinite" />')
        
        # Outer Rotating Tech Ring
        svg.append(f'      <circle cx="0" cy="0" r="42" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="14,8" opacity="0.8">')
        svg.append(f'        <animateTransform attributeName="transform" type="rotate" from="0" to="{360 if idx%2==0 else -360}" dur="12s" repeatCount="indefinite" />')
        svg.append(f'      </circle>')
        
        # Inner Shield Hexagon
        svg.append(f'      <polygon points="0,-32 28,-16 28,16 0,32 -28,16 -28,-16" fill="rgba(15,23,42,0.85)" stroke="{c}" stroke-width="1.8" filter="url(#neon-glow)" />')
        
        # Floating Icon
        svg.append(f'      <text x="0" y="7" font-size="20" text-anchor="middle">{t["icon"]}</text>')
        
        # Skill Badge & Health Bar above target
        svg.append(f'      <rect x="-55" y="-58" width="110" height="18" fill="rgba(6,10,22,0.9)" stroke="{c}" stroke-width="1" rx="4" />')
        svg.append(f'      <text x="0" y="-45" class="skill-title" fill="#ffffff" font-size="8.5">{t["name"]}</text>')
        
        # Mini HP Gauge
        svg.append(f'      <rect x="-45" y="-37" width="90" height="3" fill="rgba(255,255,255,0.1)" rx="1.5" />')
        svg.append(f'      <rect x="-45" y="-37" width="{int(90 * t["hp"]/100)}" height="3" fill="{c}" rx="1.5">')
        svg.append(f'        <animate attributeName="opacity" values="0.7;1;0.7" dur="1.5s" repeatCount="indefinite" />')
        svg.append(f'      </rect>')
        
        # Skill Class Tag below target
        svg.append(f'      <text x="0" y="48" class="skill-sub" fill="{c}">{t["lvl"]}</text>')
        svg.append(f'      <text x="0" y="58" class="skill-sub" fill="#94a3b8" font-size="7.5">{t["sub"]}</text>')
        
        # Floating Floating Damage Number (+XP)
        svg.append(f'      <text x="0" y="-66" class="crit-text" fill="{c}">')
        svg.append(f'        {t["crit"]}')
        svg.append(f'        <animate attributeName="y" values="-60;-85;-60" dur="2.4s" begin="{idx*0.5}s" repeatCount="indefinite" />')
        svg.append(f'        <animate attributeName="opacity" values="0;1;0;0" dur="2.4s" begin="{idx*0.5}s" repeatCount="indefinite" />')
        svg.append(f'      </text>')
        
        # Laser Strike Impact Flare at target center
        svg.append(f'      <circle cx="0" cy="0" r="8" fill="#ffffff" opacity="0">')
        svg.append(f'        <animate attributeName="r" values="3;18;3" dur="1.8s" begin="{idx*0.4}s" repeatCount="indefinite" />')
        svg.append(f'        <animate attributeName="opacity" values="0;0.9;0" dur="1.8s" begin="{idx*0.4}s" repeatCount="indefinite" />')
        svg.append(f'      </circle>')
        
        svg.append(f'    </g>')
        svg.append(f'  </g>')

    # 3D PLAYER FIGHTER SHIP / PLASMA CANNON (Bottom Center)
    # Ship is positioned at x=440, y=360
    svg.append('  <!-- 3D Player Combat Ship -->')
    svg.append('  <g transform="translate(440, 365)">')
    # Engine Thruster Flame
    svg.append('    <!-- Thruster Exhaust -->')
    svg.append('    <polygon points="-12,42 0,68 12,42" fill="#00f0ff" filter="url(#hyper-glow)">')
    svg.append('      <animate attributeName="points" values="-12,42 0,68 12,42; -10,42 0,55 10,42; -14,42 0,78 14,42; -12,42 0,68 12,42" dur="0.25s" repeatCount="indefinite" />')
    svg.append('    </polygon>')
    svg.append('    <polygon points="-6,42 0,55 6,42" fill="#ffffff" />')
    
    # Ship Hull Polygons (Futuristic 3D Starfighter)
    svg.append('    <!-- Left Wing -->')
    svg.append('    <polygon points="-75,32 -30,10 -15,22 -55,42" fill="#091426" stroke="#00f0ff" stroke-width="1.2" />')
    svg.append('    <!-- Right Wing -->')
    svg.append('    <polygon points="75,32 30,10 15,22 55,42" fill="#091426" stroke="#00f0ff" stroke-width="1.2" />')
    
    # Main Fuselage
    svg.append('    <!-- Fuselage Body -->')
    svg.append('    <polygon points="0,-35 24,25 15,40 -15,40 -24,25" fill="url(#hull-grad)" stroke="#38bdf8" stroke-width="1.4" />')
    svg.append('    <!-- Cockpit Canopy Glass -->')
    svg.append('    <polygon points="0,-22 9,10 0,18 -9,10" fill="#00f0ff" opacity="0.75" filter="url(#neon-glow)">')
    svg.append('      <animate attributeName="opacity" values="0.6;0.95;0.6" dur="2s" repeatCount="indefinite" />')
    svg.append('    </polygon>')
    
    # Dual Plasma Gun Barrels
    svg.append('    <!-- Dual Plasma Cannons -->')
    svg.append('    <rect x="-32" y="-12" width="5" height="28" fill="#1e293b" stroke="#00f0ff" stroke-width="1" rx="1" />')
    svg.append('    <rect x="27" y="-12" width="5" height="28" fill="#1e293b" stroke="#00f0ff" stroke-width="1" rx="1" />')
    
    # Muzzle Flashes
    svg.append('    <circle cx="-29.5" cy="-14" r="5" fill="#00f0ff" filter="url(#hyper-glow)">')
    svg.append('      <animate attributeName="r" values="2;7;2" dur="0.25s" repeatCount="indefinite" />')
    svg.append('      <animate attributeName="opacity" values="0.4;1;0.4" dur="0.25s" repeatCount="indefinite" />')
    svg.append('    </circle>')
    svg.append('    <circle cx="29.5" cy="-14" r="5" fill="#ff007f" filter="url(#hyper-glow)">')
    svg.append('      <animate attributeName="r" values="7;2;7" dur="0.25s" repeatCount="indefinite" />')
    svg.append('      <animate attributeName="opacity" values="1;0.4;1" dur="0.25s" repeatCount="indefinite" />')
    svg.append('    </circle>')
    svg.append('  </g>')

    # CONTINUOUS FIRING LASER BEAMS SHOOTING AT TARGETS
    svg.append('  <!-- Animated Plasma Laser Beams -->')
    # Left cannon fires at Python & Flutter
    svg.append('  <line x1="410.5" y1="350" x2="310" y2="105" stroke="url(#laser-cyan)" stroke-width="3.5" filter="url(#neon-glow)" stroke-linecap="round">')
    svg.append('    <animate attributeName="stroke-dasharray" values="0,200; 120,40; 0,200" dur="0.6s" repeatCount="indefinite" />')
    svg.append('    <animate attributeName="opacity" values="0.3;1;0.3" dur="0.6s" repeatCount="indefinite" />')
    svg.append('  </line>')
    
    # Right cannon fires at TypeScript & Founder Boss
    svg.append('  <line x1="469.5" y1="350" x2="440" y2="70" stroke="url(#laser-magenta)" stroke-width="4" filter="url(#hyper-glow)" stroke-linecap="round">')
    svg.append('    <animate attributeName="stroke-dasharray" values="120,40; 0,200; 120,40" dur="0.75s" repeatCount="indefinite" />')
    svg.append('    <animate attributeName="opacity" values="1;0.4;1" dur="0.75s" repeatCount="indefinite" />')
    svg.append('  </line>')

    # Moving Crosshair Locking On Targets
    svg.append('  <!-- Autonomous Aim-Lock Crosshair -->')
    svg.append('  <g>')
    svg.append('    <!-- Tracking Path between target positions -->')
    svg.append('    <animateMotion path="M 310,105 L 440,70 L 570,105 L 170,150 L 710,150 Z" dur="8s" repeatCount="indefinite" />')
    # Crosshair Reticle SVG
    svg.append('    <circle cx="0" cy="0" r="16" fill="none" stroke="#ff0055" stroke-width="1.8" filter="url(#neon-glow)" stroke-dasharray="8,5" />')
    svg.append('    <line x1="-24" y1="0" x2="-18" y2="0" stroke="#ff0055" stroke-width="2" />')
    svg.append('    <line x1="18" y1="0" x2="24" y2="0" stroke="#ff0055" stroke-width="2" />')
    svg.append('    <line x1="0" y1="-24" x2="0" y2="-18" stroke="#ff0055" stroke-width="2" />')
    svg.append('    <line x1="0" y1="18" x2="0" y2="24" stroke="#ff0055" stroke-width="2" />')
    svg.append('    <text x="0" y="-22" font-family="monospace" font-size="8" font-weight="900" fill="#ff0055" text-anchor="middle">[LOCK-ON]</text>')
    svg.append('  </g>')

    # TOP LEFT HUD: PLAYER STATUS & HEALTH
    svg.append('  <!-- Top Left HUD Deck -->')
    svg.append('  <rect x="25" y="20" width="220" height="75" class="hud-panel" />')
    svg.append('  <g transform="translate(38, 38)">')
    svg.append('    <text x="0" y="0" class="hud-header">COMMANDER: ANGKON NATH</text>')
    svg.append('    <text x="0" y="14" class="hud-stat">CLASS: <tspan class="hud-val">FULLSTACK &amp; AI CEO</tspan></text>')
    
    # HP Bar
    svg.append('    <text x="0" y="32" class="hud-stat" font-size="9">HP 100%</text>')
    svg.append('    <rect x="45" y="24" width="140" height="8" fill="rgba(255,255,255,0.1)" rx="3" />')
    svg.append('    <rect x="45" y="24" width="140" height="8" fill="url(#hp-grad)" rx="3" filter="url(#neon-glow)" />')
    
    # Shield / Energy Bar
    svg.append('    <text x="0" y="47" class="hud-stat" font-size="9">ENERGY</text>')
    svg.append('    <rect x="45" y="39" width="140" height="6" fill="rgba(255,255,255,0.1)" rx="2" />')
    svg.append('    <rect x="45" y="39" width="125" height="6" fill="#a855f7" rx="2">')
    svg.append('      <animate attributeName="width" values="110;140;110" dur="2s" repeatCount="indefinite" />')
    svg.append('    </rect>')
    svg.append('  </g>')

    # TOP RIGHT HUD: SCORE, COMBO & STATS
    svg.append('  <!-- Top Right Score Deck -->')
    svg.append(f'  <rect x="{width-245}" y="20" width="220" height="75" class="hud-panel" />')
    svg.append(f'  <g transform="translate({width-230}, 38)">')
    svg.append('    <text x="0" y="0" class="score-title">TOTAL REPO SCORE</text>')
    svg.append('    <text x="0" y="20" class="score-num">2,410,101 PTS</text>')
    svg.append('    <text x="0" y="36" class="hud-stat">STREAK MULTIPLIER: <tspan class="hud-val" fill="#ffb703">x99 COMBO</tspan></text>')
    svg.append('    <text x="0" y="48" class="hud-stat">BUGS ANNIHILATED: <tspan class="hud-val">100% CLEAN</tspan></text>')
    svg.append('  </g>')

    # BOTTOM COCKPIT WEAPONS SELECTOR
    svg.append('  <!-- Bottom Arsenal Bar -->')
    weapons = [
        ('1', 'DART BLASTER', '#00f0ff'),
        ('2', 'PYTHON CANNON', '#a855f7'),
        ('3', 'TS GATLING', '#ffb703'),
        ('4', 'BOHUVAJ OVERDRIVE', '#ff0055')
    ]
    for w_idx, (w_key, w_name, w_col) in enumerate(weapons):
        wx = 25 + w_idx * 105
        svg.append(f'  <g transform="translate({wx}, {height-38})">')
        svg.append(f'    <rect x="0" y="0" width="98" height="22" rx="4" fill="rgba(10,15,30,0.85)" stroke="{w_col}" stroke-width="1" />')
        svg.append(f'    <text x="10" y="15" font-family="monospace" font-size="10" font-weight="900" fill="{w_col}">[{w_key}]</text>')
        svg.append(f'    <text x="28" y="14" font-family="-apple-system, BlinkMacSystemFont, monospace" font-size="7.5" font-weight="800" fill="#ffffff">{w_name}</text>')
        svg.append(f'  </g>')

    # Bottom Right Telemetry Indicator
    svg.append(f'  <g transform="translate({width-180}, {height-24})">')
    svg.append('    <circle cx="0" cy="-4" r="3.5" fill="#00ff88" filter="url(#neon-glow)">')
    svg.append('      <animate attributeName="opacity" values="1;0.2;1" dur="1s" repeatCount="indefinite" />')
    svg.append('    </circle>')
    svg.append('    <text x="10" y="0" font-family="monospace" font-size="9" font-weight="700" fill="#00ff88">ARCADE SHOOTER ACTIVE</text>')
    svg.append('  </g>')

    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated 3D Shooting Game Skill SVG -> {filename}")

if __name__ == "__main__":
    generate_shooting_game_svg()
