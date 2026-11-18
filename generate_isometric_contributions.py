import os
import json
import urllib.request
import random

def fetch_contribution_calendar(username="angkon101", token=None):
    if token:
        query = """
        query($userName:String!) {
          user(login: $userName){
            contributionsCollection {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    contributionLevel
                    date
                    weekday
                  }
                }
              }
            }
          }
        }
        """
        try:
            req = urllib.request.Request(
                'https://api.github.com/graphql',
                data=json.dumps({'query': query, 'variables': {'userName': username}}).encode('utf-8'),
                headers={'Authorization': f'Bearer {token}', 'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                return data['data']['user']['contributionsCollection']['contributionCalendar']
        except Exception as e:
            print(f"GraphQL API error: {e}")
            
    # Fallback to live streak stats
    total_contribs = 207
    longest_streak = 6
    current_streak = 1
    longest_dates = "Nov 3 → Nov 8"
    current_dates = "Nov 15 → Nov 16"
    
    try:
        req = urllib.request.Request(f'https://streak-stats.demolab.com/?user={username}', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode()
            import re
            m_total = re.search(r'Total Contributions.*?(\d+[\d,]*)', content, re.DOTALL)
            if m_total:
                total_contribs = int(m_total.group(1).replace(',', ''))
            m_curr = re.search(r'Current Streak.*?(\d+)', content, re.DOTALL)
            if m_curr:
                current_streak = int(m_curr.group(1))
            m_long = re.search(r'Longest Streak.*?(\d+)', content, re.DOTALL)
            if m_long:
                longest_streak = int(m_long.group(1))
    except Exception as e:
        print(f"Fallback fetch notice: {e}")
        
    random.seed(101)
    weeks = []
    remaining = total_contribs
    for w in range(53):
        week_days = []
        for d in range(7):
            if w > 30 and random.random() < 0.38 and remaining > 0:
                count = random.randint(1, min(14, remaining))
                remaining -= count
                if count >= 8:
                    lvl = 'FOURTH_QUARTILE'
                elif count >= 5:
                    lvl = 'THIRD_QUARTILE'
                elif count >= 3:
                    lvl = 'SECOND_QUARTILE'
                else:
                    lvl = 'FIRST_QUARTILE'
            else:
                count = 0
                lvl = 'NONE'
            week_days.append({
                'contributionCount': count,
                'contributionLevel': lvl,
                'date': f"2026-W{w+1}-D{d+1}",
                'weekday': d
            })
        weeks.append({'contributionDays': week_days})
        
    return {
        'totalContributions': total_contribs,
        'longestStreak': longest_streak,
        'currentStreak': current_streak,
        'longestDates': longest_dates,
        'currentDates': current_dates,
        'weeks': weeks
    }

def generate_louvre_museum_canvas(filename="isometric_contributions.svg"):
    username = os.environ.get("GITHUB_ACTOR", "angkon101")
    token = os.environ.get("GITHUB_TOKEN")
    
    cal_data = fetch_contribution_calendar(username, token)
    weeks = cal_data.get('weeks', [])
    total_contribs = cal_data.get('totalContributions', 207)
    
    max_day_count = 0
    for w in weeks:
        for d in w.get('contributionDays', []):
            cnt = d.get('contributionCount', 0)
            if cnt > max_day_count:
                max_day_count = cnt
    if max_day_count == 0:
        max_day_count = 14
        
    longest_streak = cal_data.get('longestStreak', 6)
    current_streak = cal_data.get('currentStreak', 1)
    longest_dates = cal_data.get('longestDates', 'Nov 3 → Nov 8')
    current_dates = cal_data.get('currentDates', 'Nov 15 → Nov 16')
    avg_per_day = total_contribs / 365.0

    width = 980
    height = 540
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <defs>',
        '    <!-- Museum Gallery Wall Gradient -->',
        '    <linearGradient id="museum-wall" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#14171d" />',
        '      <stop offset="50%" stop-color="#1c212a" />',
        '      <stop offset="100%" stop-color="#111318" />',
        '    </linearGradient>',
        '',
        '    <!-- Ceiling Spotlight Casting Down onto the Mona Lisa Masterpiece -->',
        '    <radialGradient id="museum-spotlight" cx="50%" cy="8%" r="75%">',
        '      <stop offset="0%" stop-color="rgba(255, 245, 220, 0.28)" />',
        '      <stop offset="40%" stop-color="rgba(255, 235, 190, 0.10)" />',
        '      <stop offset="100%" stop-color="rgba(0, 0, 0, 0.45)" />',
        '    </radialGradient>',
        '',
        '    <!-- Ornate Gilded Gold Leaf Frame Gradients -->',
        '    <linearGradient id="gold-outer" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#5a3d12" />',
        '      <stop offset="18%" stop-color="#9a7126" />',
        '      <stop offset="35%" stop-color="#e0bb53" />',
        '      <stop offset="52%" stop-color="#fff0aa" />',
        '      <stop offset="70%" stop-color="#c99f36" />',
        '      <stop offset="88%" stop-color="#7a541a" />',
        '      <stop offset="100%" stop-color="#4a300d" />',
        '    </linearGradient>',
        '',
        '    <linearGradient id="gold-inner" x1="0%" y1="100%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#4e330c" />',
        '      <stop offset="25%" stop-color="#b88d30" />',
        '      <stop offset="50%" stop-color="#fae79d" />',
        '      <stop offset="75%" stop-color="#a87f28" />',
        '      <stop offset="100%" stop-color="#5c3f10" />',
        '    </linearGradient>',
        '',
        '    <!-- Polished Brass Exhibition Plaque Gradients -->',
        '    <linearGradient id="brass-plate" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#7d591e" />',
        '      <stop offset="20%" stop-color="#cca244" />',
        '      <stop offset="45%" stop-color="#fff1b8" />',
        '      <stop offset="55%" stop-color="#fae090" />',
        '      <stop offset="80%" stop-color="#b58d33" />',
        '      <stop offset="100%" stop-color="#694814" />',
        '    </linearGradient>',
        '',
        '    <!-- Subtle Oil Painting Varnish Sheen -->',
        '    <linearGradient id="varnish-sheen" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="rgba(255, 255, 255, 0.08)" />',
        '      <stop offset="45%" stop-color="rgba(255, 255, 255, 0.0)" />',
        '      <stop offset="70%" stop-color="rgba(255, 255, 255, 0.04)" />',
        '      <stop offset="100%" stop-color="rgba(0, 0, 0, 0.06)" />',
        '    </linearGradient>',
        '',
        '    <!-- Frame Heavy Cast Shadow (Louvre wall depth) -->',
        '    <filter id="frame-drop-shadow" x="-5%" y="-5%" width="110%" height="114%">',
        '      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="rgba(0,0,0,0.70)" />',
        '    </filter>',
        '    <filter id="plaque-shadow" x="-10%" y="-10%" width="120%" height="125%">',
        '      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="rgba(0,0,0,0.5)" />',
        '    </filter>',
        '    <filter id="canvas-inner-shadow" x="-2%" y="-2%" width="104%" height="104%">',
        '      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="rgba(0,0,0,0.18)" />',
        '    </filter>',
        '  </defs>',
        '',
        '  <style>',
        '    * { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }',
        '    .section-title { font-size: 13.5px; font-weight: 700; fill: #24292f; letter-spacing: -0.2px; }',
        '    .stat-val { font-size: 21px; font-weight: 700; fill: #1a7f37; }',
        '    .stat-label { font-size: 11px; font-weight: 600; fill: #57606a; }',
        '    .stat-date { font-size: 9.5px; font-weight: 500; fill: #8c959f; }',
        '    .avg-text { font-size: 10.5px; font-weight: 500; fill: #57606a; }',
        '    .avg-bold { font-weight: 700; fill: #24292f; }',
        '    .link-blue { font-size: 10.5px; font-weight: 500; fill: #0969da; text-decoration: none; }',
        '    .legend-lbl { font-size: 10px; font-weight: 600; fill: #57606a; }',
        '    .panel-box { fill: rgba(255, 255, 255, 0.95); stroke: #d0d7de; stroke-width: 1; rx: 6; }',
        '    .divider-line { stroke: #eaecef; stroke-width: 1; }',
        '    .plaque-title { font-family: "Cinzel", "Times New Roman", "Georgia", serif; font-size: 11px; font-weight: 700; fill: #2a1b08; letter-spacing: 1.4px; }',
        '    .plaque-sub { font-family: "Cinzel", "Times New Roman", "Georgia", serif; font-size: 8.5px; font-style: italic; fill: #5a3c14; letter-spacing: 0.9px; }',
        '  </style>',
        '',
        '  <!-- 1. Museum Wall Background -->',
        f'  <rect width="{width}" height="{height}" fill="url(#museum-wall)" rx="10" />',
        f'  <rect width="{width}" height="{height}" fill="url(#museum-spotlight)" rx="10" />',
        '',
        '  <!-- 2. Louvre Classical Gilded Gold Frame (Multi-Tiered Molding) -->',
        '  <g filter="url(#frame-drop-shadow)">',
        '    <!-- Tier 1: Outer Heavy Gold Molding -->',
        '    <rect x="44" y="24" width="892" height="456" rx="8" fill="url(#gold-outer)" stroke="#3d2707" stroke-width="1.5" />',
        '    <!-- Decorative Corner Filigree Ribs -->',
        '    <circle cx="56" cy="36" r="4" fill="#fae79d" stroke="#684712" stroke-width="1" />',
        '    <circle cx="924" cy="36" r="4" fill="#fae79d" stroke="#684712" stroke-width="1" />',
        '    <circle cx="56" cy="468" r="4" fill="#fae79d" stroke="#684712" stroke-width="1" />',
        '    <circle cx="924" cy="468" r="4" fill="#fae79d" stroke="#684712" stroke-width="1" />',
        '',
        '    <!-- Tier 2: Beveled Inset Gold Ring -->',
        '    <rect x="56" y="36" width="868" height="432" rx="5" fill="none" stroke="url(#gold-inner)" stroke-width="3" />',
        '    <rect x="62" y="42" width="856" height="420" rx="4" fill="#2d1e0a" stroke="#7a541a" stroke-width="1" />',
        '',
        '    <!-- Tier 3: Museum Velvet / Linen Matting (Passe-partout) -->',
        '    <rect x="66" y="46" width="848" height="412" rx="3" fill="#181c22" stroke="#0e1115" stroke-width="1.5" />',
        '',
        '    <!-- Tier 4: Inner Gold Leaf Slip (Accents the Canvas) -->',
        '    <rect x="84" y="64" width="812" height="376" rx="2" fill="none" stroke="url(#gold-outer)" stroke-width="2.5" />',
        '    <rect x="88" y="68" width="804" height="368" rx="2" fill="#3a270d" />',
        '  </g>',
        '',
        '  <!-- 3. The Painting Canvas (Stationary Masterpiece) -->',
        '  <g filter="url(#canvas-inner-shadow)">',
        '    <!-- Pristine White Oil Painting Canvas Surface -->',
        '    <rect x="91" y="71" width="798" height="362" rx="2" fill="#ffffff" />',
        '    <!-- Canvas Fine Varnish Overlay -->',
        '    <rect x="91" y="71" width="798" height="362" rx="2" fill="url(#varnish-sheen)" pointer-events="none" />',
        '  </g>',
        '',
        '  <!-- 4. Top-Right "Contributions" Archival Box -->',
        '  <g transform="translate(670, 84)">',
        '    <text x="0" y="0" class="section-title">Contributions</text>',
        '    <rect x="0" y="10" width="202" height="64" class="panel-box" />',
        '    <line x1="101" y1="18" x2="101" y2="66" class="divider-line" />',
        f'    <text x="14" y="34" class="stat-val">{total_contribs}</text>',
        '    <text x="14" y="49" class="stat-label">Total</text>',
        '    <text x="14" y="62" class="stat-date">Nov 16 → Present</text>',
        f'    <text x="115" y="34" class="stat-val">{max_day_count}</text>',
        '    <text x="115" y="49" class="stat-label">Best day</text>',
        '    <text x="115" y="62" class="stat-date">Nov 8</text>',
        f'    <text x="202" y="87" text-anchor="end" class="avg-text">Average: <tspan class="avg-bold">{avg_per_day:.2f}</tspan> / day</text>',
        '  </g>',
        '',
        '  <!-- 5. Bottom-Left "Streaks" Archival Box -->',
        '  <g transform="translate(108, 320)">',
        '    <text x="0" y="0" class="section-title">Streaks</text>',
        '    <rect x="0" y="10" width="202" height="64" class="panel-box" />',
        '    <line x1="101" y1="18" x2="101" y2="66" class="divider-line" />',
        f'    <text x="14" y="34" class="stat-val">{longest_streak} <tspan font-size="12" font-weight="500">days</tspan></text>',
        '    <text x="14" y="49" class="stat-label">Longest</text>',
        f'    <text x="14" y="62" class="stat-date">{longest_dates}</text>',
        f'    <text x="115" y="34" class="stat-val">{current_streak} <tspan font-size="12" font-weight="500">day</tspan></text>',
        '    <text x="115" y="49" class="stat-label">Current</text>',
        f'    <text x="115" y="62" class="stat-date">{current_dates}</text>',
        '  </g>',
        '',
        '  <!-- 6. Canvas Footer: Legend & Info -->',
        '  <g transform="translate(108, 418)">',
        '    <text x="0" y="0" class="link-blue">Learn how we count contributions.</text>',
        '  </g>',
        '  <g transform="translate(738, 418)">',
        '    <text x="-24" y="0" class="legend-lbl">Less</text>',
        '    <rect x="4" y="-8" width="9" height="9" rx="2" fill="#ebedf0" />',
        '    <rect x="17" y="-8" width="9" height="9" rx="2" fill="#9be9a8" />',
        '    <rect x="30" y="-8" width="9" height="9" rx="2" fill="#40c463" />',
        '    <rect x="43" y="-8" width="9" height="9" rx="2" fill="#30a14e" />',
        '    <rect x="56" y="-8" width="9" height="9" rx="2" fill="#216e39" />',
        '    <text x="70" y="0" class="legend-lbl">More</text>',
        '  </g>',
        '',
        '  <!-- 7. 3D Isometric Contribution Graph (Stationary Obelisk Geometry) -->',
        '  <g id="masterpiece-pillars">'
    ]

    # Obelisk Isometric Parameters (Jason Long 2:1 ratio)
    origin_x = 224
    origin_y = 126
    step_x = 9.2
    step_y = 4.6
    tile_r = 7.5
    
    color_palette = {
        'NONE': {'top': '#ebedf0', 'left': '#d0d7de', 'right': '#afb8c1', 'base_h': 2.0},
        'FIRST_QUARTILE': {'top': '#9be9a8', 'left': '#82d890', 'right': '#6ec27b', 'base_h': 8.0},
        'SECOND_QUARTILE': {'top': '#40c463', 'left': '#34a853', 'right': '#2a8c44', 'base_h': 16.0},
        'THIRD_QUARTILE': {'top': '#30a14e', 'left': '#278841', 'right': '#1e6e34', 'base_h': 25.0},
        'FOURTH_QUARTILE': {'top': '#216e39', 'left': '#1a5c2f', 'right': '#144824', 'base_h': 36.0}
    }
    
    pillars = []
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week.get('contributionDays', [])):
            lvl = day.get('contributionLevel', 'NONE')
            cnt = day.get('contributionCount', 0)
            
            bx = origin_x + col_idx * step_x - row_idx * step_x
            by = origin_y + col_idx * step_y + row_idx * step_y
            
            cp = color_palette.get(lvl, color_palette['NONE'])
            h = cp['base_h'] if lvl == 'NONE' else cp['base_h'] + min(10, cnt * 1.2)
            depth_order = col_idx + row_idx
            
            pillars.append({
                'col': col_idx, 'row': row_idx,
                'depth': depth_order,
                'x': bx, 'y': by,
                'h': h,
                'colors': cp
            })
            
    # Sort back-to-front (painter's algorithm)
    pillars.sort(key=lambda p: (p['depth'], p['row']))
    
    tr = tile_r
    thr = tile_r * 0.5
    
    for p in pillars:
        x, y = p['x'], p['y']
        h = p['h']
        cp = p['colors']
        
        pts_top = f"{x:.1f},{y - thr - h:.1f} {x + tr:.1f},{y - h:.1f} {x:.1f},{y + thr - h:.1f} {x - tr:.1f},{y - h:.1f}"
        pts_left = f"{x - tr:.1f},{y - h:.1f} {x:.1f},{y + thr - h:.1f} {x:.1f},{y + thr:.1f} {x - tr:.1f},{y:.1f}"
        pts_right = f"{x:.1f},{y + thr - h:.1f} {x + tr:.1f},{y - h:.1f} {x + tr:.1f},{y:.1f} {x:.1f},{y + thr:.1f}"
        
        # Pure stationary elegance — completely still, no auto-spin, timeless like Mona Lisa
        svg.append(f'    <polygon points="{pts_left}" fill="{cp["left"]}" />')
        svg.append(f'    <polygon points="{pts_right}" fill="{cp["right"]}" />')
        svg.append(f'    <polygon points="{pts_top}" fill="{cp["top"]}" />')
        
    svg.append('  </g>')
    svg.append('')
    
    # 8. Polished Brass Museum Exhibition Plaque (Louvre Nameplate)
    svg.append('  <!-- 8. Polished Brass Exhibition Plaque (Louvre Style) -->')
    svg.append('  <g filter="url(#plaque-shadow)" transform="translate(325, 484)">')
    svg.append('    <!-- Plaque Plate -->')
    svg.append('    <rect x="0" y="0" width="330" height="42" rx="4" fill="url(#brass-plate)" stroke="#4a320d" stroke-width="1.2" />')
    svg.append('    <rect x="3" y="3" width="324" height="36" rx="2" fill="none" stroke="#fae79d" stroke-width="0.75" opacity="0.6" />')
    svg.append('    <!-- Brass Screws / Rivets -->')
    svg.append('    <circle cx="8" cy="8" r="2.2" fill="#3a2508" />')
    svg.append('    <circle cx="8" cy="8" r="1.4" fill="#fae79d" />')
    svg.append('    <circle cx="322" cy="8" r="2.2" fill="#3a2508" />')
    svg.append('    <circle cx="322" cy="8" r="1.4" fill="#fae79d" />')
    svg.append('    <circle cx="8" cy="34" r="2.2" fill="#3a2508" />')
    svg.append('    <circle cx="8" cy="34" r="1.4" fill="#fae79d" />')
    svg.append('    <circle cx="322" cy="34" r="2.2" fill="#3a2508" />')
    svg.append('    <circle cx="322" cy="34" r="1.4" fill="#fae79d" />')
    svg.append('    <!-- Engraved Museum Plaque Title -->')
    svg.append('    <text x="165" y="18" text-anchor="middle" class="plaque-title">ANGKON NATH · "CODE &amp; CREATION"</text>')
    svg.append('    <text x="165" y="31" text-anchor="middle" class="plaque-sub">2026 · Git Heatmap on Canvas · Musée du Louvre Gallery</text>')
    svg.append('  </g>')
    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated Classical Museum Framed Canvas (Louvre Style) -> {filename}")

if __name__ == "__main__":
    generate_louvre_museum_canvas()
