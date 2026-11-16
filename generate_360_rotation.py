import math
import random
from PIL import Image, ImageDraw, ImageFont

def generate_360_rotating_gif(filename="contributions_3d_360.gif", num_frames=36):
    width, height = 900, 480
    
    # 53 weeks x 7 days
    cols = 53
    rows = 7
    total_contribs = 207
    max_day_count = 14
    
    # Seed contribution data matching angkon101
    random.seed(101)
    grid_data = []
    remaining = total_contribs
    for c in range(cols):
        for r in range(rows):
            cnt = 0
            lvl = 0
            if c > 32 and random.random() < 0.38 and remaining > 0:
                cnt = random.randint(1, min(14, remaining))
                remaining -= cnt
                if cnt >= 8: lvl = 4
                elif cnt >= 5: lvl = 3
                elif cnt >= 3: lvl = 2
                else: lvl = 1
            grid_data.append({'col': c, 'row': r, 'count': cnt, 'lvl': lvl})

    # 3D Grid Parameters
    step_x = 7.0
    step_y = 7.0
    box_size = 5.2
    
    center_col = (cols - 1) / 2.0
    center_row = (rows - 1) / 2.0
    
    # Color palette
    colors = {
        0: {'top': (235, 237, 240), 'side1': (208, 215, 222), 'side2': (175, 184, 193), 'h': 2.0},
        1: {'top': (155, 233, 168), 'side1': (130, 216, 144), 'side2': (110, 194, 123), 'h': 8.0},
        2: {'top': (64, 196, 99),   'side1': (52, 168, 83),   'side2': (42, 140, 68),   'h': 16.0},
        3: {'top': (48, 161, 78),   'side1': (39, 136, 65),   'side2': (30, 110, 52),   'h': 26.0},
        4: {'top': (33, 110, 57),   'side1': (26, 92, 47),    'side2': (20, 72, 36),    'h': 38.0}
    }
    
    phi = math.radians(34) # Camera tilt
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)
    
    screen_cx = width / 2.0
    screen_cy = height / 2.0 + 35
    
    frames = []
    
    for f in range(num_frames):
        theta = (2.0 * math.pi * f) / num_frames
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        
        # New frame image
        frame = Image.new('RGB', (width, height), '#ffffff')
        draw = ImageDraw.Draw(frame)
        
        # Background card frame
        draw.rounded_rectangle([(2, 2), (width - 4, height - 4)], radius=12, fill='#ffffff', outline='#d0d7de', width=1)
        
        # HUD: Top-Right Contributions
        tr_x, tr_y = width - 265, 26
        draw.text((tr_x, tr_y), "Contributions", fill='#24292f')
        draw.rounded_rectangle([(tr_x, tr_y + 20), (tr_x + 230, tr_y + 92)], radius=6, fill='#ffffff', outline='#d0d7de', width=1)
        draw.line([(tr_x + 115, tr_y + 28), (tr_x + 115, tr_y + 84)], fill='#eaecef', width=1)
        
        draw.text((tr_x + 16, tr_y + 28), f"{total_contribs}", fill='#1a7f37')
        draw.text((tr_x + 16, tr_y + 54), "Total", fill='#57606a')
        draw.text((tr_x + 16, tr_y + 70), "Nov 16 → Present", fill='#8c959f')
        
        draw.text((tr_x + 130, tr_y + 28), f"{max_day_count}", fill='#1a7f37')
        draw.text((tr_x + 130, tr_y + 54), "Best day", fill='#57606a')
        draw.text((tr_x + 130, tr_y + 70), "Nov 8", fill='#8c959f')
        draw.text((tr_x + 230 - 110, tr_y + 98), f"Average: {total_contribs/365.0:.2f} / day", fill='#57606a')
        
        # HUD: Bottom-Left Streaks
        bl_x, bl_y = 35, height - 145
        draw.text((bl_x, bl_y), "Streaks", fill='#24292f')
        draw.rounded_rectangle([(bl_x, bl_y + 20), (bl_x + 230, bl_y + 92)], radius=6, fill='#ffffff', outline='#d0d7de', width=1)
        draw.line([(bl_x + 115, bl_y + 28), (bl_x + 115, bl_y + 84)], fill='#eaecef', width=1)
        
        draw.text((bl_x + 16, bl_y + 28), "6 days", fill='#1a7f37')
        draw.text((bl_x + 16, bl_y + 54), "Longest", fill='#57606a')
        draw.text((bl_x + 16, bl_y + 70), "Nov 3 → Nov 8", fill='#8c959f')
        
        draw.text((bl_x + 130, bl_y + 28), "1 day", fill='#1a7f37')
        draw.text((bl_x + 130, bl_y + 54), "Current", fill='#57606a')
        draw.text((bl_x + 130, bl_y + 70), "Nov 15 → Nov 16", fill='#8c959f')
        
        # Footer
        draw.text((bl_x, height - 25), "Learn how we count contributions.", fill='#0969da')
        draw.text((width - 150 - 30, height - 25), "Less", fill='#57606a')
        leg_cols = [(235, 237, 240), (155, 233, 168), (64, 196, 99), (48, 161, 78), (33, 110, 57)]
        for i, lc in enumerate(leg_cols):
            draw.rounded_rectangle([(width - 150 + i * 13, height - 25), (width - 150 + i * 13 + 10, height - 15)], radius=2, fill=lc)
        draw.text((width - 150 + 5 * 13 + 6, height - 25), "More", fill='#57606a')
        
        # 3D 360° Rotating Model
        # Rotate all pillars and sort by depth (painter's algorithm)
        projected_pillars = []
        
        for p in grid_data:
            c, r = p['col'], p['row']
            lvl = p['lvl']
            cnt = p['count']
            
            # Position relative to center
            X = (c - center_col) * step_x
            Y = (r - center_row) * step_y
            
            # Rotate around vertical Z axis by theta
            rx = X * cos_t - Y * sin_t
            ry = X * sin_t + Y * cos_t
            
            h = colors[lvl]['h']
            if lvl > 0:
                h += min(10, cnt * 1.2)
                
            depth = ry * cos_phi
            projected_pillars.append({
                'rx': rx, 'ry': ry, 'h': h,
                'depth': depth, 'lvl': lvl
            })
            
        # Sort back to front (lowest depth first)
        projected_pillars.sort(key=lambda item: item['depth'])
        
        half_b = box_size / 2.0
        
        # Draw each 3D box
        for item in projected_pillars:
            rx, ry, h = item['rx'], item['ry'], item['h']
            col_info = colors[item['lvl']]
            
            # 4 base corners rotated by theta
            # Corners in local box coords: (+- half_b, +- half_b)
            corners = [
                (-half_b, -half_b),
                (half_b, -half_b),
                (half_b, half_b),
                (-half_b, half_b)
            ]
            
            # Rotate corners and project to screen
            base_pts = []
            top_pts = []
            
            for cx_l, cy_l in corners:
                # Local rotated
                cx_r = rx + (cx_l * cos_t - cy_l * sin_t)
                cy_r = ry + (cx_l * sin_t + cy_l * cos_t)
                
                # Base projection
                bx_s = screen_cx + cx_r
                by_s = screen_cy + cy_r * sin_phi
                base_pts.append((bx_s, by_s))
                
                # Top projection (elevated by h)
                tx_s = screen_cx + cx_r
                ty_s = screen_cy + (cy_r * sin_phi - h)
                top_pts.append((tx_s, ty_s))
                
            # Draw side walls (4 faces around the perimeter)
            for side_idx in range(4):
                next_idx = (side_idx + 1) % 4
                
                # Backface culling: calculate 2D cross product of screen edge
                v1x = base_pts[next_idx][0] - base_pts[side_idx][0]
                v1y = base_pts[next_idx][1] - base_pts[side_idx][1]
                v2x = top_pts[side_idx][0] - base_pts[side_idx][0]
                v2y = top_pts[side_idx][1] - base_pts[side_idx][1]
                cross = v1x * v2y - v1y * v2x
                
                if cross > 0: # Facing camera!
                    wall_poly = [
                        base_pts[side_idx],
                        base_pts[next_idx],
                        top_pts[next_idx],
                        top_pts[side_idx]
                    ]
                    # Shade according to angle
                    wall_col = col_info['side1'] if (side_idx % 2 == 0) else col_info['side2']
                    draw.polygon(wall_poly, fill=wall_col)
                    
            # Draw top face
            draw.polygon(top_pts, fill=col_info['top'])
            
        frames.append(frame)
        print(f"Rendered frame {f+1}/{num_frames}")
        
    # Save as optimized animated GIF
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=70,  # ~14 FPS smooth rotation
        loop=0,
        optimize=True
    )
    print(f"Generated 360° Rotating 3D GIF -> {filename}")

if __name__ == "__main__":
    generate_360_rotating_gif()
