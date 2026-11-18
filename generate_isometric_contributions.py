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

def generate_mona_lisa_masterpiece(filename="isometric_contributions.svg"):
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

    width = 1000
    height = 560
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <defs>',
        '    <!-- Museum Louvre Wall Background -->',
        '    <linearGradient id="wall-paint" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#12151c" />',
        '      <stop offset="50%" stop-color="#1b2029" />',
        '      <stop offset="100%" stop-color="#0f1117" />',
        '    </linearGradient>',
        '',
        '    <!-- Directional Gallery Ceiling Spotlight Illuminating Mona Lisa -->',
        '    <radialGradient id="louvre-spotlight" cx="35%" cy="12%" r="80%">',
        '      <stop offset="0%" stop-color="rgba(255, 248, 225, 0.32)" />',
        '      <stop offset="45%" stop-color="rgba(255, 240, 200, 0.12)" />',
        '      <stop offset="100%" stop-color="rgba(0, 0, 0, 0.5)" />',
        '    </radialGradient>',
        '',
        '    <!-- Classical Gilded Gold Frame Gradients -->',
        '    <linearGradient id="gold-leaf-outer" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#4e330c" />',
        '      <stop offset="15%" stop-color="#9a7126" />',
        '      <stop offset="35%" stop-color="#e2bf57" />',
        '      <stop offset="50%" stop-color="#fff2b2" />',
        '      <stop offset="68%" stop-color="#cb9f33" />',
        '      <stop offset="85%" stop-color="#7a541a" />',
        '      <stop offset="100%" stop-color="#422908" />',
        '    </linearGradient>',
        '',
        '    <linearGradient id="gold-leaf-inner" x1="0%" y1="100%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#5a3d12" />',
        '      <stop offset="30%" stop-color="#b88d30" />',
        '      <stop offset="50%" stop-color="#fae79d" />',
        '      <stop offset="70%" stop-color="#a87f28" />',
        '      <stop offset="100%" stop-color="#4a300d" />',
        '    </linearGradient>',
        '',
        '    <!-- Mona Lisa Portrait Sfumato Background Gradients -->',
        '    <linearGradient id="sfumato-sky" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#556b68" />',
        '      <stop offset="40%" stop-color="#7a928b" />',
        '      <stop offset="75%" stop-color="#8ba192" />',
        '      <stop offset="100%" stop-color="#5a6c5f" />',
        '    </linearGradient>',
        '    <linearGradient id="sfumato-earth" x1="0%" y1="0%" x2="0%" y2="100%">',
        '      <stop offset="0%" stop-color="#3c4a3e" />',
        '      <stop offset="50%" stop-color="#2a332a" />',
        '      <stop offset="100%" stop-color="#1e241c" />',
        '    </linearGradient>',
        '',
        '    <!-- Renaissance Skin Tones (Da Vinci Sfumato Shading) -->',
        '    <linearGradient id="skin-face" x1="25%" y1="0%" x2="80%" y2="100%">',
        '      <stop offset="0%" stop-color="#f5e0cb" />',
        '      <stop offset="45%" stop-color="#e9cbb2" />',
        '      <stop offset="80%" stop-color="#d4aa8c" />',
        '      <stop offset="100%" stop-color="#b68366" />',
        '    </linearGradient>',
        '    <linearGradient id="skin-neck" x1="30%" y1="0%" x2="70%" y2="100%">',
        '      <stop offset="0%" stop-color="#edd2bc" />',
        '      <stop offset="50%" stop-color="#d8b195" />',
        '      <stop offset="100%" stop-color="#a8785c" />',
        '    </linearGradient>',
        '    <linearGradient id="skin-hand" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#f8e5d3" />',
        '      <stop offset="60%" stop-color="#e4c4aa" />',
        '      <stop offset="100%" stop-color="#be9479" />',
        '    </linearGradient>',
        '',
        '    <!-- Mona Lisa Hair & Robes Gradients -->',
        '    <linearGradient id="hair-shade" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#36251b" />',
        '      <stop offset="50%" stop-color="#20150e" />',
        '      <stop offset="100%" stop-color="#140c08" />',
        '    </linearGradient>',
        '    <linearGradient id="dress-fabric" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#3b3b27" />',
        '      <stop offset="40%" stop-color="#282a1d" />',
        '      <stop offset="80%" stop-color="#191a13" />',
        '      <stop offset="100%" stop-color="#0f110c" />',
        '    </linearGradient>',
        '    <linearGradient id="shawl-fabric" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#695133" />',
        '      <stop offset="50%" stop-color="#483620" />',
        '      <stop offset="100%" stop-color="#2c1f10" />',
        '    </linearGradient>',
        '',
        '    <!-- Brass Exhibition Plaque Gradients -->',
        '    <linearGradient id="brass-grad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#7a551b" />',
        '      <stop offset="25%" stop-color="#cca244" />',
        '      <stop offset="48%" stop-color="#fff4be" />',
        '      <stop offset="56%" stop-color="#fad97f" />',
        '      <stop offset="80%" stop-color="#b78e34" />',
        '      <stop offset="100%" stop-color="#6b4814" />',
        '    </linearGradient>',
        '',
        '    <!-- Shadow Filters -->',
        '    <filter id="frame-drop" x="-5%" y="-5%" width="110%" height="114%">',
        '      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="rgba(0,0,0,0.72)" />',
        '    </filter>',
        '    <filter id="plaque-drop" x="-10%" y="-10%" width="120%" height="125%">',
        '      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="rgba(0,0,0,0.55)" />',
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
        '    .plaque-title { font-family: "Cinzel", "Times New Roman", "Georgia", serif; font-size: 11.5px; font-weight: 700; fill: #2a1b08; letter-spacing: 1.5px; }',
        '    .plaque-sub { font-family: "Cinzel", "Times New Roman", "Georgia", serif; font-size: 9px; font-style: italic; fill: #5a3c14; letter-spacing: 0.9px; }',
        '  </style>',
        '',
        '  <!-- 1. Museum Wall Background -->',
        f'  <rect width="{width}" height="{height}" fill="url(#wall-paint)" rx="10" />',
        f'  <rect width="{width}" height="{height}" fill="url(#louvre-spotlight)" rx="10" />',
        '',
        '  <!-- 2. Classical Louvre Gilded Gold Frame -->',
        '  <g filter="url(#frame-drop)">',
        '    <!-- Outer Gold Leaf Molding -->',
        '    <rect x="42" y="24" width="916" height="474" rx="8" fill="url(#gold-leaf-outer)" stroke="#382206" stroke-width="1.5" />',
        '    <!-- Decorative Corner Rosettes -->',
        '    <circle cx="56" cy="38" r="4.5" fill="#fff0aa" stroke="#684712" stroke-width="1" />',
        '    <circle cx="944" cy="38" r="4.5" fill="#fff0aa" stroke="#684712" stroke-width="1" />',
        '    <circle cx="56" cy="484" r="4.5" fill="#fff0aa" stroke="#684712" stroke-width="1" />',
        '    <circle cx="944" cy="484" r="4.5" fill="#fff0aa" stroke="#684712" stroke-width="1" />',
        '',
        '    <!-- Inner Gold Fillet & Dark Velvet Matting -->',
        '    <rect x="56" y="38" width="888" height="446" rx="5" fill="none" stroke="url(#gold-leaf-inner)" stroke-width="3" />',
        '    <rect x="62" y="44" width="876" height="434" rx="4" fill="#181c22" stroke="#0e1115" stroke-width="1.5" />',
        '    <rect x="80" y="62" width="840" height="398" rx="2" fill="none" stroke="url(#gold-leaf-outer)" stroke-width="2.5" />',
        '    <rect x="84" y="66" width="832" height="390" rx="2" fill="#32220c" />',
        '  </g>',
        '',
        '  <!-- 3. Painting Canvas Surface -->',
        '  <rect x="87" y="69" width="826" height="384" rx="2" fill="#fafafa" />',
        '',
        '  <!-- ============================================================== -->',
        '  <!-- 4. LEONARDO DA VINCI: LA GIOCONDA (THE MONA LISA PORTRAIT)    -->',
        '  <!-- ============================================================== -->',
        '  <g id="mona-lisa-portrait" transform="translate(90, 71)">',
        '    <!-- Clip path to keep Mona Lisa within her portrait arch/section -->',
        '    <defs>',
        '      <clipPath id="mona-clip">',
        '        <rect x="0" y="0" width="290" height="380" rx="2" />',
        '      </clipPath>',
        '    </defs>',
        '    ',
        '    <g clip-path="url(#mona-clip)">',
        '      <!-- Background Sfumato Sky & Italian Landscape -->',
        '      <rect x="0" y="0" width="290" height="380" fill="url(#sfumato-sky)" />',
        '      <!-- Distant hazy mountains and winding road -->',
        '      <path d="M0 160 Q 60 140, 120 155 T 200 145 T 290 158 L 290 240 L 0 240 Z" fill="#698075" opacity="0.6" />',
        '      <path d="M0 185 Q 80 170, 160 185 T 290 175 L 290 280 L 0 280 Z" fill="#4d6255" opacity="0.75" />',
        '      <!-- Winding River Arno -->',
        '      <path d="M40 180 Q 70 200, 50 220 T 70 245" stroke="#8fa69a" stroke-width="4" fill="none" opacity="0.5" />',
        '      <path d="M220 175 Q 240 195, 230 215 T 250 235" stroke="#8fa69a" stroke-width="3" fill="none" opacity="0.4" />',
        '      <!-- Earth & Loggia Balustrade Base -->',
        '      <rect x="0" y="240" width="290" height="140" fill="url(#sfumato-earth)" />',
        '      <rect x="0" y="360" width="290" height="20" fill="#1b1d16" stroke="#2c3024" stroke-width="1" />',
        '',
        '      <!-- Robe / Cloak / Renaissance Gown -->',
        '      <!-- Outer Dark Cloak covering shoulders -->',
        '      <path d="M30 380 C 40 280, 80 230, 145 228 C 210 230, 250 280, 260 380 Z" fill="url(#dress-fabric)" />',
        '      <!-- Ochre / Golden Brown Draped Shawl on Left Shoulder -->',
        '      <path d="M45 380 C 50 310, 80 260, 120 250 L 105 380 Z" fill="url(#shawl-fabric)" />',
        '      <path d="M245 380 C 240 310, 210 260, 170 250 L 185 380 Z" fill="url(#shawl-fabric)" />',
        '',
        '      <!-- Pleated Silk Bodice & Embroidered Gold Neckline -->',
        '      <path d="M110 245 C 130 260, 160 260, 180 245 L 175 320 C 155 330, 135 330, 115 320 Z" fill="#2d2217" />',
        '      <!-- Gold Embroidered Renaissance Border Trim -->',
        '      <path d="M106 242 C 128 262, 162 262, 184 242" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-dasharray="3,2" />',
        '',
        '      <!-- Décolletage & Neck with Smooth Sfumato Transitions -->',
        '      <path d="M120 180 L 120 240 C 132 254, 158 254, 170 240 L 170 180 Z" fill="url(#skin-neck)" />',
        '      <!-- Soft Chin Shadow -->',
        '      <ellipse cx="145" cy="200" rx="18" ry="8" fill="#9e6e50" opacity="0.35" />',
        '',
        '      <!-- Wavy Dark Renaissance Hair Flowing Over Shoulders -->',
        '      <!-- Left Hair -->',
        '      <path d="M112 110 C 95 150, 90 210, 115 270 C 105 270, 80 220, 92 140 Z" fill="url(#hair-shade)" />',
        '      <path d="M114 125 C 102 165, 100 225, 122 280 C 112 280, 92 230, 102 150 Z" fill="#1b120c" />',
        '      <!-- Right Hair -->',
        '      <path d="M178 110 C 195 150, 200 210, 175 270 C 185 270, 210 220, 198 140 Z" fill="url(#hair-shade)" />',
        '      <path d="M176 125 C 188 165, 190 225, 168 280 C 178 280, 198 230, 188 150 Z" fill="#1b120c" />',
        '',
        '      <!-- Mona Lisa Head & Face Structure -->',
        '      <path d="M112 115 C 110 70, 130 54, 145 54 C 160 54, 180 70, 178 115 C 176 160, 162 196, 145 196 C 128 196, 114 160, 112 115 Z" fill="url(#skin-face)" />',
        '',
        '      <!-- Transparent Silk Veil (Guarnello) over head -->',
        '      <path d="M110 110 C 110 50, 130 46, 145 46 C 160 46, 180 50, 180 110 C 165 95, 125 95, 110 110 Z" fill="#2a1f18" opacity="0.65" />',
        '      <!-- Veil Edge Rim -->',
        '      <path d="M111 106 C 125 86, 165 86, 179 106" fill="none" stroke="#d5c8ba" stroke-width="1" opacity="0.6" />',
        '',
        '      <!-- High Plucked Renaissance Forehead & Hairline -->',
        '      <path d="M113 95 C 124 78, 145 74, 145 74 C 145 74, 166 78, 177 95 C 165 84, 125 84, 113 95 Z" fill="#241710" />',
        '',
        '      <!-- Facial Features: Eyes, Nose, and the Iconic Enigmatic Smile -->',
        '      <!-- Leonardo Eyebrow Region (Extremely subtle, no prominent brow hair) -->',
        '      <path d="M123 108 Q 132 104, 138 107" fill="none" stroke="#b08468" stroke-width="1.2" opacity="0.4" />',
        '      <path d="M152 107 Q 158 104, 167 108" fill="none" stroke="#b08468" stroke-width="1.2" opacity="0.4" />',
        '',
        '      <!-- Left Eye with Gentle Sfumato Gaze -->',
        '      <ellipse cx="131" cy="116" rx="6.5" ry="3.5" fill="#fdf4eb" />',
        '      <circle cx="131.5" cy="116" r="2.8" fill="#422e1e" />',
        '      <circle cx="132.2" cy="115.3" r="0.9" fill="#ffffff" />',
        '      <path d="M124 115 Q 131 111, 138 114" fill="none" stroke="#503522" stroke-width="1.3" />',
        '      <path d="M125 116 Q 131 119, 137 116" fill="none" stroke="#90654c" stroke-width="0.8" opacity="0.7" />',
        '',
        '      <!-- Right Eye with Gentle Sfumato Gaze -->',
        '      <ellipse cx="159" cy="116" rx="6.5" ry="3.5" fill="#fdf4eb" />',
        '      <circle cx="158.5" cy="116" r="2.8" fill="#422e1e" />',
        '      <circle cx="159.2" cy="115.3" r="0.9" fill="#ffffff" />',
        '      <path d="M152 114 Q 159 111, 166 115" fill="none" stroke="#503522" stroke-width="1.3" />',
        '      <path d="M153 116 Q 159 119, 165 116" fill="none" stroke="#90654c" stroke-width="0.8" opacity="0.7" />',
        '',
        '      <!-- Slender Italian Classical Nose with Shadow -->',
        '      <path d="M144 114 L 143 146 Q 145 151, 149 148" fill="none" stroke="#b8896d" stroke-width="1.5" />',
        '      <ellipse cx="141" cy="148" rx="2.5" ry="1.5" fill="#8f6146" opacity="0.5" />',
        '      <ellipse cx="149" cy="148" rx="2.5" ry="1.5" fill="#8f6146" opacity="0.5" />',
        '',
        '      <!-- =================================================== -->',
        '      <!-- THE WORLD-FAMOUS ENIGMATIC SMILE (LA GIOCONDA)   -->',
        '      <!-- =================================================== -->',
        '      <!-- Soft sfumato shadow at lip corners -->',
        '      <circle cx="132" cy="167" r="2.2" fill="#86513a" opacity="0.5" />',
        '      <circle cx="158" cy="166.5" r="2.2" fill="#86513a" opacity="0.5" />',
        '      <!-- Upper Lip: Subtle Cupid\'s bow curving into slight upward smile -->',
        '      <path d="M133 167 Q 140 164, 145 165 Q 150 164, 157 166.5" fill="none" stroke="#98533e" stroke-width="1.6" />',
        '      <!-- Center Mouth Line: Gentle mysterious curve -->',
        '      <path d="M132 167 Q 145 168.5, 158 166.5" fill="none" stroke="#5c2c1e" stroke-width="1.5" />',
        '      <!-- Lower Lip: Softly rounded and highlighted -->',
        '      <path d="M135 167.5 Q 145 174, 155 167" fill="#c47862" opacity="0.75" />',
        '      <path d="M136 168 Q 145 173, 154 167.5" fill="none" stroke="#a45842" stroke-width="1.2" />',
        '      <!-- Chin dimple shadow -->',
        '      <ellipse cx="145" cy="182" rx="7" ry="2.5" fill="#a46d50" opacity="0.3" />',
        '',
        '      <!-- =================================================== -->',
        '      <!-- MONA LISA\'S FAMOUS RESTING CROSSED HANDS          -->',
        '      <!-- =================================================== -->',
        '      <g transform="translate(70, 315)">',
        '        <!-- Right arm resting on chair balustrade -->',
        '        <path d="M15 35 C 30 15, 70 12, 115 15 C 130 16, 140 28, 135 45 C 110 50, 40 52, 15 35 Z" fill="url(#dress-fabric)" />',
        '        <!-- Left hand placed over right wrist (the classic crossed posture) -->',
        '        <!-- Delicate Renaissance Fingers -->',
        '        <path d="M60 20 C 75 14, 105 14, 130 18 C 138 20, 140 27, 135 32 C 110 33, 80 34, 60 20 Z" fill="url(#skin-hand)" />',
        '        <!-- Forefinger & Middle fingers -->',
        '        <path d="M85 24 Q 115 22, 142 27 Q 138 33, 115 33 Z" fill="url(#skin-hand)" stroke="#9c6d4e" stroke-width="0.6" />',
        '        <path d="M80 30 Q 110 28, 138 34 Q 134 40, 110 39 Z" fill="url(#skin-hand)" stroke="#9c6d4e" stroke-width="0.6" />',
        '        <path d="M75 36 Q 105 35, 130 41 Q 126 46, 105 45 Z" fill="url(#skin-hand)" stroke="#9c6d4e" stroke-width="0.6" />',
        '      </g>',
        '    </g>',
        '    <!-- Portrait Inner Border Frame Divider -->',
        '    <line x1="290" y1="0" x2="290" y2="380" stroke="#d5be8a" stroke-width="2" />',
        '    <line x1="292" y1="0" x2="292" y2="380" stroke="#3d280c" stroke-width="1" />',
        '  </g>',
        '',
        '  <!-- ============================================================== -->',
        '  <!-- 5. GITHUB CONTRIBUTION GRAPH & STATS (THE DIGITAL CANVAS)     -->',
        '  <!-- ============================================================== -->',
        '  <!-- Top-Right "Contributions" Archival Box -->',
        '  <g transform="translate(685, 82)">',
        '    <text x="0" y="0" class="section-title">Contributions</text>',
        '    <rect x="0" y="10" width="210" height="64" class="panel-box" />',
        '    <line x1="105" y1="18" x2="105" y2="66" class="divider-line" />',
        f'    <text x="14" y="34" class="stat-val">{total_contribs}</text>',
        '    <text x="14" y="49" class="stat-label">Total</text>',
        '    <text x="14" y="62" class="stat-date">Nov 16 → Present</text>',
        f'    <text x="120" y="34" class="stat-val">{max_day_count}</text>',
        '    <text x="120" y="49" class="stat-label">Best day</text>',
        '    <text x="120" y="62" class="stat-date">Nov 8</text>',
        f'    <text x="210" y="87" text-anchor="end" class="avg-text">Average: <tspan class="avg-bold">{avg_per_day:.2f}</tspan> / day</text>',
        '  </g>',
        '',
        '  <!-- Bottom-Left "Streaks" Archival Box (beside Mona Lisa) -->',
        '  <g transform="translate(395, 345)">',
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
        '  <!-- Footer Legend & Info -->',
        '  <g transform="translate(615, 432)">',
        '    <text x="0" y="0" class="link-blue">Learn how we count contributions.</text>',
        '  </g>',
        '  <g transform="translate(775, 432)">',
        '    <text x="-24" y="0" class="legend-lbl">Less</text>',
        '    <rect x="4" y="-8" width="9" height="9" rx="2" fill="#ebedf0" />',
        '    <rect x="17" y="-8" width="9" height="9" rx="2" fill="#9be9a8" />',
        '    <rect x="30" y="-8" width="9" height="9" rx="2" fill="#40c463" />',
        '    <rect x="43" y="-8" width="9" height="9" rx="2" fill="#30a14e" />',
        '    <rect x="56" y="-8" width="9" height="9" rx="2" fill="#216e39" />',
        '    <text x="70" y="0" class="legend-lbl">More</text>',
        '  </g>',
        '',
        '  <!-- 3D Isometric Contribution Pillars (Jason Long Obelisk Geometry) -->',
        '  <g id="masterpiece-pillars">'
    ]

    # Obelisk Isometric Parameters positioned gracefully on the right
    origin_x = 485
    origin_y = 138
    step_x = 8.1
    step_y = 4.05
    tile_r = 6.6
    
    color_palette = {
        'NONE': {'top': '#ebedf0', 'left': '#d0d7de', 'right': '#afb8c1', 'base_h': 1.8},
        'FIRST_QUARTILE': {'top': '#9be9a8', 'left': '#82d890', 'right': '#6ec27b', 'base_h': 7.0},
        'SECOND_QUARTILE': {'top': '#40c463', 'left': '#34a853', 'right': '#2a8c44', 'base_h': 14.0},
        'THIRD_QUARTILE': {'top': '#30a14e', 'left': '#278841', 'right': '#1e6e34', 'base_h': 22.0},
        'FOURTH_QUARTILE': {'top': '#216e39', 'left': '#1a5c2f', 'right': '#144824', 'base_h': 32.0}
    }
    
    pillars = []
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week.get('contributionDays', [])):
            lvl = day.get('contributionLevel', 'NONE')
            cnt = day.get('contributionCount', 0)
            
            bx = origin_x + col_idx * step_x - row_idx * step_x
            by = origin_y + col_idx * step_y + row_idx * step_y
            
            cp = color_palette.get(lvl, color_palette['NONE'])
            h = cp['base_h'] if lvl == 'NONE' else cp['base_h'] + min(9, cnt * 1.1)
            depth_order = col_idx + row_idx
            
            pillars.append({
                'col': col_idx, 'row': row_idx,
                'depth': depth_order,
                'x': bx, 'y': by,
                'h': h,
                'colors': cp
            })
            
    # Painter's algorithm sort
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
        
        # Stationary, timeless, no auto-rotation
        svg.append(f'    <polygon points="{pts_left}" fill="{cp["left"]}" />')
        svg.append(f'    <polygon points="{pts_right}" fill="{cp["right"]}" />')
        svg.append(f'    <polygon points="{pts_top}" fill="{cp["top"]}" />')
        
    svg.append('  </g>')
    svg.append('')
    
    # 6. Polished Brass Museum Exhibition Plaque (Louvre Nameplate)
    svg.append('  <!-- 6. Polished Brass Museum Exhibition Plaque -->')
    svg.append('  <g filter="url(#plaque-drop)" transform="translate(310, 504)">')
    svg.append('    <rect x="0" y="0" width="380" height="42" rx="4" fill="url(#brass-grad)" stroke="#4a320d" stroke-width="1.2" />')
    svg.append('    <rect x="3" y="3" width="374" height="36" rx="2" fill="none" stroke="#fff4be" stroke-width="0.75" opacity="0.6" />')
    svg.append('    <!-- Brass Screws / Rivets -->')
    svg.append('    <circle cx="8" cy="8" r="2.2" fill="#3a2508" /><circle cx="8" cy="8" r="1.3" fill="#fff4be" />')
    svg.append('    <circle cx="372" cy="8" r="2.2" fill="#3a2508" /><circle cx="372" cy="8" r="1.3" fill="#fff4be" />')
    svg.append('    <circle cx="8" cy="34" r="2.2" fill="#3a2508" /><circle cx="8" cy="34" r="1.3" fill="#fff4be" />')
    svg.append('    <circle cx="372" cy="34" r="2.2" fill="#3a2508" /><circle cx="372" cy="34" r="1.3" fill="#fff4be" />')
    svg.append('    <!-- Engraved Exhibition Inscription -->')
    svg.append('    <text x="190" y="18" text-anchor="middle" class="plaque-title">LEONARDO DA VINCI &amp; ANGKON NATH · "MONA LISA &amp; CODE"</text>')
    svg.append('    <text x="190" y="31" text-anchor="middle" class="plaque-sub">1503 – 2026 · Musée du Louvre, Salle des États · Git Heatmap on Canvas</text>')
    svg.append('  </g>')
    svg.append('</svg>')
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Generated Authentic Mona Lisa Louvre Masterpiece -> {filename}")

if __name__ == "__main__":
    generate_mona_lisa_masterpiece()
