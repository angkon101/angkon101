import os
import json
import urllib.request

def fetch_contributions(username, token):
    query = """
    query($userName:String!) {
      user(login: $userName){
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': query, 'variables': {'userName': username}}).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    except Exception as e:
        print(f"Error fetching data from GitHub API: {e}")
        return []

def draw_pixel_sprite(name, pixels, colors, scale=1.0):
    svg = [f'    <g id="{name}">']
    for y_idx, row_str in enumerate(pixels):
        for x_idx, char in enumerate(row_str):
            if char in colors and colors[char]:
                px = x_idx * scale
                py = y_idx * scale
                svg.append(f'      <rect x="{px:.1f}" y="{py:.1f}" width="{scale:.1f}" height="{scale:.1f}" fill="{colors[char]}" />')
    svg.append('    </g>')
    return "\n".join(svg)

def generate_minecraft_github_svg(filename="minecraft_contribution.svg"):
    username = os.environ.get("GITHUB_ACTOR", "angkon101")
    token = os.environ.get("GITHUB_TOKEN")
    
    weeks_data = fetch_contributions(username, token) if token else []
    
    # If no data returned, generate standard 53 weeks
    if not weeks_data:
        weeks_data = [{'contributionDays': [{'contributionLevel': 'NONE'}] * 7} for _ in range(53)]
        # Add some mock activity so it looks alive when testing locally
        import random
        random.seed(101)
        levels = ['NONE', 'NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE']
        for w in weeks_data:
            w['contributionDays'] = [{'contributionLevel': random.choice(levels)} for _ in range(7)]

    # --- DIMENSIONS & GEOMETRY ---
    cell_w = 11
    cell_h = 10
    gap_x = 3
    gap_y = 3
    step_x = cell_w + gap_x
    step_y = cell_h + gap_y
    cols = len(weeks_data)
    rows = 7
    
    portal_x = 18
    grid_x_offset = 65
    top_padding = 68
    
    fortress_x = grid_x_offset + (cols * step_x) + 20
    width = fortress_x + 95
    ground_y = top_padding + (rows * step_y) + 8
    height = ground_y + 60
    
    svg = [
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <!-- Minecraft Sky Gradients -->',
        '    <linearGradient id="mc-sky" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#4a89f3" />',
        '      <stop offset="65%" stop-color="#73a7f8" />',
        '      <stop offset="100%" stop-color="#9dc2fc" />',
        '    </linearGradient>',
        '    <!-- Nether Portal Energy -->',
        '    <linearGradient id="portal-glow" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#4a0e4e" />',
        '      <stop offset="50%" stop-color="#8a2be2" />',
        '      <stop offset="100%" stop-color="#d946ef" />',
        '    </linearGradient>',
        '    <linearGradient id="beacon-beam" x1="0%" y1="100%" x2="0%" y2="0%">',
        '      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.9" />',
        '      <stop offset="70%" stop-color="#00f0ff" stop-opacity="0.4" />',
        '      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0" />',
        '    </linearGradient>',
        '    <!-- Glow Filters -->',
        '    <filter id="mc-glow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feGaussianBlur stdDeviation="2.5" result="blur" />',
        '      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>',
        '    <filter id="xp-glow" x="-40%" y="-40%" width="180%" height="180%">',
        '      <feGaussianBlur stdDeviation="3.5" result="blur" />',
        '      <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>',
        '    </filter>'
    ]
    
    # --- SPRITE ASSETS (STEVE, PICKAXE, CREEPER, ORES, ITEMS) ---
    # Steve's Body
    steve_body_pixels = [
        "  HHHHHH  ",
        " HHHHHHHH ",
        " HHSSESSH ",
        " HSSSESSH ",
        "  SSSSSS  ",
        "  SMMSMS  ",
        "   CCCC   ",
        " CCCCCCCC ",
        " CCCCCCCC ",
        " CCCCCCCC ",
        "  PP  PP  ",
        "  PP  PP  ",
        "  PP  PP  ",
        "  BB  BB  "
    ]
    steve_colors = {
        'H': '#3a2010', 'S': '#bd8b72', 'E': '#2b448e', 'M': '#593822',
        'C': '#009ea8', 'P': '#1c2866', 'B': '#3c3c3c'
    }
    
    # Diamond Pickaxe Sprite
    pickaxe_pixels = [
        "   DDDD ",
        "  DDDD  ",
        " DD W   ",
        "  D W   ",
        "   W    ",
        "  W     ",
        " W      "
    ]
    pickaxe_colors = {'D': '#2ce1d5', 'W': '#6c4422'}

    # Creeper Sprite
    creeper_pixels = [
        "  GGGGGG  ",
        " GGGGGGGG ",
        " GKKGGKKG ",
        " GKKGGKKG ",
        " GGGKKGGG ",
        " GGKKKKGG ",
        " GGKKKKGG ",
        " GGKGGKGG ",
        "  GGGGGG  ",
        " GGGGGGGG ",
        " GGGGGGGG ",
        " GGGGGGGG ",
        "  GG  GG  ",
        "  GG  GG  "
    ]
    creeper_colors = {'G': '#38a169', 'K': '#1a202c'}

    # Floating 3D Diamond Gem
    diamond_pixels = [
        "   DD   ",
        "  DCCD  ",
        " DCCCCD ",
        "DCCCCCCD",
        " DCCCCD ",
        "  DCCD  ",
        "   DD   "
    ]
    diamond_colors = {'D': '#00b4d8', 'C': '#90e0ef'}

    # Green XP Orb
    xp_pixels = [
        "  YY  ",
        " YGGY ",
        " YGGY ",
        "  YY  "
    ]
    xp_colors = {'Y': '#ccff00', 'G': '#39ff14'}

    svg.append(draw_pixel_sprite("steve_body", steve_body_pixels, steve_colors, scale=1.4))
    svg.append(draw_pixel_sprite("diamond_pickaxe", pickaxe_pixels, pickaxe_colors, scale=1.6))
    svg.append(draw_pixel_sprite("creeper", creeper_pixels, creeper_colors, scale=1.3))
    svg.append(draw_pixel_sprite("diamond_gem", diamond_pixels, diamond_colors, scale=1.4))
    svg.append(draw_pixel_sprite("xp_orb", xp_pixels, xp_colors, scale=1.5))
    
    # Combined Animated Steve (with swinging pickaxe arm)
    svg.append('    <g id="animated_steve">')
    svg.append('      <use href="#steve_body" x="0" y="0" />')
    # Swinging Right Arm with Pickaxe
    svg.append('      <g transform="translate(11, 10)">')
    svg.append('        <g>')
    # 0.4s rhythmic pickaxe swing
    svg.append('          <animateTransform attributeName="transform" type="rotate" values="0 0 0; -65 0 0; 15 0 0; 0 0 0" dur="0.45s" repeatCount="indefinite" />')
    svg.append('          <rect x="-1" y="0" width="3.5" height="10" fill="#009ea8" />')
    svg.append('          <use href="#diamond_pickaxe" x="-4" y="6" />')
    svg.append('        </g>')
    svg.append('      </g>')
    svg.append('    </g>')
    
    svg.append('  </defs>')
    
    # --- STYLES ---
    svg.append('  <style>')
    svg.append('    .mc-font { font-family: "Courier New", Courier, monospace, -apple-system; font-weight: bold; }')
    svg.append('    .title-banner { fill: #facc15; font-size: 11px; letter-spacing: 1.5px; filter: drop-shadow(1px 1px 0px #000); }')
    svg.append('    .advancement { fill: #ffffff; font-size: 9.5px; filter: drop-shadow(1px 1px 0px #000); }')
    svg.append('    .hud-text { font-family: monospace; font-size: 10px; fill: #ffffff; font-weight: bold; }')
    svg.append('    .ground-block { fill: #866043; }')
    svg.append('    .ground-top-grass { fill: #48bb78; }')
    svg.append('    .stone-bedrock { fill: #2d3748; }')
    svg.append('  </style>')
    
    # --- BACKGROUND (Minecraft Blue Sky & Ground) ---
    svg.append(f'  <rect width="{width}" height="{height}" fill="url(#mc-sky)" rx="8" />')
    
    # Minecraft Square Sun
    svg.append('  <!-- Minecraft Square Sun -->')
    svg.append('  <g transform="translate(240, 16)">')
    svg.append('    <rect x="0" y="0" width="34" height="34" fill="#ffffff" stroke="#fef08a" stroke-width="3" />')
    svg.append('    <rect x="3" y="3" width="28" height="28" fill="#fef9c3" />')
    svg.append('  </g>')
    
    # Minecraft Drifting Voxel Clouds
    svg.append('  <!-- Drifting Voxel Clouds -->')
    clouds = [(60, 22, 90, 16), (360, 30, 120, 18), (620, 18, 100, 16)]
    for idx, (cx, cy, cw, ch) in enumerate(clouds):
        svg.append(f'  <g>')
        svg.append(f'    <rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#ffffff" opacity="0.85" rx="2" />')
        svg.append(f'    <rect x="{cx+15}" y="{cy-6}" width="{cw-30}" height="6" fill="#ffffff" opacity="0.85" rx="1" />')
        svg.append(f'    <animateTransform attributeName="transform" type="translate" values="0,0; {width - cx},0; -{cx + cw},0; 0,0" dur="{35 + idx*10}s" repeatCount="indefinite" />')
        svg.append(f'  </g>')

    # Ground Layer (Dirt & Bedrock)
    svg.append(f'  <!-- Ground Surface -->')
    svg.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="{height - ground_y}" fill="#573d26" />')
    # Grass Top strip on ground
    svg.append(f'  <rect x="0" y="{ground_y}" width="{width}" height="4" fill="#48bb78" />')
    # Dirt pixel details
    for dx in range(0, width, 18):
        svg.append(f'  <rect x="{dx}" y="{ground_y + 8}" width="6" height="4" fill="#6e4c30" />')
        svg.append(f'  <rect x="{dx + 9}" y="{ground_y + 16}" width="5" height="4" fill="#422c1b" />')

    # --- LEFT STRUCTURE: 3D NETHER PORTAL ---
    portal_top = ground_y - 62
    svg.append('  <!-- Nether Portal -->')
    svg.append(f'  <g transform="translate({portal_x}, {portal_top})">')
    # Obsidian Frame (Outer 30x62, Inner 18x50)
    svg.append('    <rect x="0" y="0" width="32" height="62" fill="#1e102d" stroke="#10071a" stroke-width="1.5" />')
    # Swirling Purple Portal Fluid
    svg.append('    <rect x="6" y="6" width="20" height="50" fill="url(#portal-glow)" opacity="0.9" />')
    # Swirling animated portal lines
    for pl in range(3):
        svg.append(f'    <rect x="8" y="{12 + pl*14}" width="16" height="4" fill="#e9d5ff" opacity="0.6">')
        svg.append(f'      <animate attributeName="y" values="{12 + pl*14};{12 + pl*14 - 8};{12 + pl*14}" dur="{1.2 + pl*0.4}s" repeatCount="indefinite" />')
        svg.append(f'      <animate attributeName="opacity" values="0.3;0.9;0.3" dur="{1.2 + pl*0.4}s" repeatCount="indefinite" />')
        svg.append(f'    </rect>')
    svg.append('  </g>')

    # --- RIGHT STRUCTURE: 3D MINECRAFT BEACON FORTRESS ---
    fort_top = ground_y - 68
    svg.append('  <!-- Minecraft Beacon Tower -->')
    svg.append(f'  <g transform="translate({fortress_x}, {fort_top})">')
    # Sky Beacon Light Beam shooting straight up!
    svg.append('    <rect x="18" y="-70" width="14" height="70" fill="url(#beacon-beam)" filter="url(#mc-glow)">')
    svg.append('      <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite" />')
    svg.append('    </rect>')
    # Beacon Glass Block
    svg.append('    <rect x="16" y="0" width="18" height="18" fill="rgba(255,255,255,0.7)" stroke="#00f0ff" stroke-width="1.5" />')
    svg.append('    <rect x="20" y="4" width="10" height="10" fill="#00f0ff" filter="url(#mc-glow)" />')
    # Cobblestone Fortress Base
    svg.append('    <rect x="6" y="18" width="38" height="50" fill="#64748b" stroke="#334155" stroke-width="1.5" />')
    # Castle Battlement Teeth
    svg.append('    <rect x="4" y="14" width="8" height="6" fill="#475569" />')
    svg.append('    <rect x="21" y="14" width="8" height="6" fill="#475569" />')
    svg.append('    <rect x="38" y="14" width="8" height="6" fill="#475569" />')
    # Wooden Door
    svg.append('    <rect x="18" y="44" width="14" height="24" fill="#78350f" stroke="#451a03" stroke-width="1" />')
    svg.append('    <rect x="20" y="48" width="4" height="5" fill="#000000" opacity="0.4" />')
    svg.append('  </g>')

    # Standalone Pet Wolf / Dog or Creeper Guarding the Fortress
    svg.append(f'  <!-- Friendly Guard Creeper -->')
    svg.append(f'  <g transform="translate({fortress_x + 52}, {ground_y - 26})">')
    svg.append('    <use href="#creeper" x="0" y="0" />')
    svg.append('  </g>')

    # --- TOP TITLE & MINECRAFT ADVANCEMENT BANNER ---
    svg.append('  <!-- Top Minecraft Toast Advancement -->')
    svg.append('  <g transform="translate(18, 14)">')
    # Outer dark stone border
    svg.append('    <rect x="0" y="0" width="360" height="36" fill="#18181b" stroke="#3f3f46" stroke-width="1.8" rx="4" />')
    # Trophy Icon
    svg.append('    <text x="12" y="24" font-size="18">🏆</text>')
    svg.append('    <text x="38" y="16" class="mc-font title-banner">ADVANCEMENT MADE!</text>')
    svg.append('    <text x="38" y="28" class="mc-font advancement">Co-founder &amp; CEO // Bohuvuj.com</text>')
    svg.append('  </g>')

    # Right Seed Display
    svg.append(f'  <g transform="translate({width - 240}, 24)">')
    svg.append('    <rect x="0" y="0" width="220" height="26" fill="rgba(24,24,27,0.85)" stroke="#3f3f46" stroke-width="1" rx="4" />')
    svg.append('    <text x="12" y="17" class="mc-font" font-size="10" fill="#34d399">SEED: angkon101 [3D VOXEL]</text>')
    svg.append('  </g>')

    # --- 3D VOXEL CONTRIBUTION GRAPH RENDERING ---
    steve_h = 24
    total_travel_distance = fortress_x - portal_x
    
    path_d = f"M {portal_x + 12} {ground_y - steve_h} L {grid_x_offset} {ground_y - steve_h} "
    current_x, current_y = grid_x_offset, ground_y - steve_h
    
    diamonds_to_spawn = []
    xp_to_spawn = []
    
    # 3D Voxel Block Styling per Level
    # (Top face color, Side shadow color, Highlight color, Ore specks)
    block_styles = {
        'NONE': {
            'top': 'rgba(255,255,255,0.25)', 'side': 'rgba(0,0,0,0.2)',
            'highlight': 'rgba(255,255,255,0.4)', 'is_ore': False
        },
        'FIRST_QUARTILE': { # Light Grass Block
            'top': '#48bb78', 'side': '#2f855a',
            'highlight': '#68d391', 'dirt': '#866043', 'is_ore': False
        },
        'SECOND_QUARTILE': { # Emerald Ore Block
            'top': '#38a169', 'side': '#22543d',
            'highlight': '#48bb78', 'gem': '#10b981', 'is_ore': True
        },
        'THIRD_QUARTILE': { # Diamond Ore Block
            'top': '#0284c7', 'side': '#0369a1',
            'highlight': '#38bdf8', 'gem': '#00f0ff', 'is_ore': True
        },
        'FOURTH_QUARTILE': { # Enchanted Gold / Netherite Block
            'top': '#f59e0b', 'side': '#b45309',
            'highlight': '#fde047', 'gem': '#ec4899', 'is_ore': True
        }
    }

    svg.append('  <!-- 3D Voxel Contribution Blocks -->')
    svg.append('  <g class="voxel-grid">')
    
    empty_streak = 0
    
    for col, week in enumerate(weeks_data):
        col_x = grid_x_offset + col * step_x
        highest_active_row = rows
        is_empty_week = True
        
        for row, day in enumerate(week.get('contributionDays', [])):
            lvl = day.get('contributionLevel', 'NONE')
            block_y = top_padding + row * step_y
            bs = block_styles.get(lvl, block_styles['NONE'])
            
            # Draw 3D Voxel Block
            # 1. Main Top Face
            svg.append(f'    <rect x="{col_x}" y="{block_y}" width="{cell_w}" height="{cell_h - 2}" fill="{bs["top"]}" rx="1" />')
            # 2. 3D Bottom Edge / Dirt Underhang
            side_col = bs.get('dirt', bs['side'])
            svg.append(f'    <rect x="{col_x}" y="{block_y + cell_h - 2}" width="{cell_w}" height="2" fill="{side_col}" rx="0.5" />')
            # 3. 3D Top Highlight Lip
            svg.append(f'    <line x1="{col_x}" y1="{block_y}" x2="{col_x + cell_w}" y2="{block_y}" stroke="{bs["highlight"]}" stroke-width="0.8" opacity="0.7" />')
            
            # Ore Glitter for Levels 2, 3, 4
            if bs.get('is_ore') and bs.get('gem'):
                svg.append(f'    <rect x="{col_x + 3}" y="{block_y + 2}" width="2.5" height="2.5" fill="{bs["gem"]}" />')
                svg.append(f'    <rect x="{col_x + 6}" y="{block_y + 4}" width="2" height="2" fill="{bs["gem"]}" />')
            
            if lvl != 'NONE':
                is_empty_week = False
                if row < highest_active_row:
                    highest_active_row = row
            
            # Level 4 Diamond / XP Spawn Point!
            if lvl == 'FOURTH_QUARTILE':
                progress_t = (col_x - portal_x) / total_travel_distance
                diamonds_to_spawn.append({'x': col_x, 'y': block_y - 14, 't': progress_t})
                xp_to_spawn.append({'x': col_x + 4, 'y': block_y - 20, 't': progress_t})

        # --- CALCULATE STEVE'S PARKOUR PATH ---
        if is_empty_week:
            empty_streak += 1
        else:
            empty_streak = 0
            
        target_x = col_x
        target_y = (top_padding + highest_active_row * step_y) - steve_h
        
        # If running on ground or empty streak
        if is_empty_week:
            target_y = ground_y - steve_h
            
        if empty_streak == 3:
            # Jump up for a floating diamond!
            target_y -= 18
            progress_t = (col_x - portal_x) / total_travel_distance
            diamonds_to_spawn.append({'x': col_x, 'y': target_y - 6, 't': progress_t})
            empty_streak = 0
            
        # Path segment (hop or run)
        if target_y != current_y:
            mid_x = current_x + (target_x - current_x) / 2
            mid_y = min(current_y, target_y) - 14 # Jump arc
            path_d += f" Q {mid_x:.1f} {mid_y:.1f} {target_x:.1f} {target_y:.1f}"
        else:
            path_d += f" L {target_x:.1f} {target_y:.1f}"
            
        current_x, current_y = target_x, target_y

    # Path to Beacon Fortress
    path_d += f" L {fortress_x - 12} {ground_y - steve_h} L {fortress_x + 22} {ground_y - steve_h}"
    svg.append('  </g>')

    # --- DRAW FLOATING DIAMONDS & XP ORBS (Collected as Steve passes!) ---
    svg.append('  <!-- Mined Diamonds & XP Orbs -->')
    for d in diamonds_to_spawn:
        t, t_end = d['t'], min(1.0, d['t'] + 0.04)
        svg.append(f'  <g transform="translate({d["x"]}, {d["y"]})">')
        svg.append(f'    <g>')
        # Shoots up and fades out upon pickaxe strike
        svg.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; 0,0; 0,-18; 0,-18" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg.append(f'      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg.append(f'      <use href="#diamond_gem" x="0" y="0" />')
        svg.append(f'    </g>')
        svg.append(f'  </g>')
        
    for xp in xp_to_spawn:
        t, t_end = xp['t'], min(1.0, xp['t'] + 0.035)
        svg.append(f'  <g transform="translate({xp["x"]}, {xp["y"]})">')
        svg.append(f'    <g>')
        svg.append(f'      <animateTransform attributeName="transform" type="translate" values="0,0; 0,0; 4,-24; 4,-24" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg.append(f'      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{t:.3f};{t_end:.3f};1" dur="20s" repeatCount="indefinite" />')
        svg.append(f'      <use href="#xp_orb" x="0" y="0" />')
        svg.append(f'    </g>')
        svg.append(f'  </g>')

    # --- ATTACH ANIMATED STEVE ON THE PARKOUR PATH ---
    svg.append('  <!-- Steve Running on Path -->')
    svg.append(f'  <path id="steve-path" d="{path_d}" fill="none" stroke="none" />')
    svg.append('  <use href="#animated_steve">')
    svg.append('    <animateMotion dur="20s" repeatCount="indefinite">')
    svg.append('      <mpath href="#steve-path" />')
    svg.append('    </animateMotion>')
    svg.append('  </use>')

    # --- MINECRAFT IN-GAME HUD (Hearts, Hunger, XP Bar & 9-Slot Hotbar) ---
    hud_y = ground_y + 24
    svg.append('  <!-- Minecraft In-Game Bottom HUD -->')
    svg.append(f'  <g transform="translate({width/2 - 150}, {hud_y})">')
    
    # 10 Minecraft Pixel Hearts (Health: 100%)
    for h_idx in range(10):
        hx = h_idx * 13
        svg.append(f'    <path d="M {hx+2} 2 L {hx+5} 0 L {hx+8} 2 L {hx+10} 4 L {hx+6} 9 L {hx+2} 4 Z" fill="#e11d48" stroke="#881337" stroke-width="0.8">')
        svg.append(f'      <animate attributeName="opacity" values="1;0.8;1" dur="1s" repeatCount="indefinite" />')
        svg.append(f'    </path>')
        
    # 10 Minecraft Drumsticks (Hunger: 100%)
    for f_idx in range(10):
        fx = 175 + f_idx * 13
        svg.append(f'    <circle cx="{fx+4}" cy="4" r="3.5" fill="#c2410c" stroke="#7c2d12" stroke-width="0.8" />')
        svg.append(f'    <rect x="{fx+5}" y="5" width="4" height="2" fill="#fed7aa" />')
        
    # Minecraft Experience Bar
    svg.append('    <!-- Green Experience Bar -->')
    svg.append('    <rect x="0" y="14" width="300" height="4.5" fill="#18181b" rx="1.5" stroke="#27272a" stroke-width="0.8" />')
    svg.append('    <rect x="0" y="14" width="290" height="4.5" fill="#22c55e" rx="1.5" />')
    # Level 99 in authentic bright Minecraft green with drop shadow
    svg.append('    <text x="150" y="24" text-anchor="middle" class="mc-font" font-size="12" fill="#000000">99</text>')
    svg.append('    <text x="149" y="23" text-anchor="middle" class="mc-font" font-size="12" fill="#4ade80">99</text>')
    svg.append('  </g>')

    # 9-Slot Hotbar Centered at bottom
    hotbar_w = 9 * 22 + 4
    hotbar_x = (width - hotbar_w) / 2
    hotbar_y = height - 24
    svg.append(f'  <!-- 9-Slot Inventory Hotbar -->')
    svg.append(f'  <g transform="translate({hotbar_x}, {hotbar_y})">')
    # Background strip
    svg.append(f'    <rect x="0" y="0" width="{hotbar_w}" height="22" fill="#27272a" stroke="#52525b" stroke-width="1.5" rx="3" />')
    
    # 9 Slots with icons
    slot_items = [
        ('⛏️', True),   # 1. Diamond Pickaxe (Selected / Active)
        ('🗡️', False),  # 2. Diamond Sword
        ('🍏', False),  # 3. Golden Apple
        ('💎', False),  # 4. Diamonds (x64)
        ('🟩', False),  # 5. Emeralds
        ('🪵', False),  # 6. Oak Wood
        ('🧱', False),  # 7. Redstone
        ('🏹', False),  # 8. Bow
        ('🔮', False)   # 9. Ender Pearl
    ]
    for s_idx, (icon, is_active) in enumerate(slot_items):
        sx = 2 + s_idx * 22
        if is_active:
            # Active selected slot highlight box
            svg.append(f'    <rect x="{sx-1}" y="-2" width="22" height="24" fill="rgba(255,255,255,0.2)" stroke="#ffffff" stroke-width="1.8" rx="2" />')
        else:
            svg.append(f'    <rect x="{sx}" y="1" width="20" height="19" fill="#18181b" stroke="#3f3f46" stroke-width="0.8" rx="1.5" />')
        svg.append(f'    <text x="{sx+10}" y="15" font-size="11" text-anchor="middle">{icon}</text>')
    svg.append('  </g>')

    # Minecraft LEVEL CLEAR / WIN TEXT (When Steve reaches the Beacon!)
    t_win = (fortress_x - portal_x) / total_travel_distance
    svg.append(f'  <!-- Beacon Reached: Victory Banner -->')
    svg.append(f'  <text x="{fortress_x - 110}" y="{top_padding + 14}" fill="#00f0ff" font-family="monospace" font-weight="900" font-size="15" stroke="#000" stroke-width="1" opacity="0">')
    svg.append('    BEACON ACTIVATED!')
    svg.append(f'    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t_win:.3f};{t_win+0.01:.3f};0.98;1" dur="20s" repeatCount="indefinite" />')
    svg.append(f'    <animateTransform attributeName="transform" type="translate" values="0,10; 0,10; 0,0; 0,0" keyTimes="0;{t_win:.3f};{t_win+0.02:.3f};1" dur="20s" repeatCount="indefinite" />')
    svg.append('  </text>')

    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Successfully generated 3D Minecraft {filename}!")

if __name__ == "__main__":
    generate_minecraft_github_svg()
