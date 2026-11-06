import os
import math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "arial.ttf"

def create_architecture_diagram():
    scale = 2
    width, height = 750 * scale, 750 * scale
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_box = ImageFont.truetype(FONT_PATH, 15 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 13 * scale)
        font_tier = ImageFont.truetype(FONT_PATH, 16 * scale)
    except Exception:
        font_box = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_tier = ImageFont.load_default()

    black = (0, 0, 0)
    white = (255, 255, 255)

    def draw_rounded_rect(rect, r, fill, outline, width=2):
        x0, y0, x1, y1 = rect
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

    def draw_file_icon(rect, fold, fill, outline, width=2):
        x0, y0, x1, y1 = rect
        # Draw main polygon outline with folded corner
        points = [
            (x0, y0),
            (x1 - fold, y0),
            (x1, y0 + fold),
            (x1, y1),
            (x0, y1)
        ]
        draw.polygon(points, fill=fill, outline=outline, width=width)
        # Draw the inner fold lines
        draw.line([(x1 - fold, y0), (x1 - fold, y0 + fold), (x1, y0 + fold)], fill=outline, width=width)

    def draw_arrow(start, end, bidirectional=False):
        draw.line([start, end], fill=black, width=2 * scale)
        x1, y1 = start
        x2, y2 = end
        
        # Arrowhead helper
        def draw_head(ax1, ay1, ax2, ay2):
            angle = math.atan2(ay2 - ay1, ax2 - ax1)
            arrow_len = 10 * scale
            px1 = ax2 - arrow_len * math.cos(angle - math.pi/6)
            py1 = ay2 - arrow_len * math.sin(angle - math.pi/6)
            px2 = ax2 - arrow_len * math.cos(angle + math.pi/6)
            py2 = ay2 - arrow_len * math.sin(angle + math.pi/6)
            draw.polygon([(ax2, ay2), (px1, py1), (px2, py2)], fill=black)

        draw_head(x1, y1, x2, y2)
        if bidirectional:
            draw_head(x2, y2, x1, y1)

    def draw_dashed_line(start, end, dash_len=8*scale, gap_len=6*scale):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        cos = dx / dist
        sin = dy / dist
        curr_dist = 0
        while curr_dist < dist:
            next_dist = min(curr_dist + dash_len, dist)
            draw.line([(x1 + curr_dist * cos, y1 + curr_dist * sin), 
                       (x1 + next_dist * cos, y1 + next_dist * sin)], fill=black, width=2 * scale)
            curr_dist += dash_len + gap_len

    # --- 1. Client Tier (Top) ---
    web_browser_rect = [180 * scale, 40 * scale, 460 * scale, 160 * scale]
    draw_rounded_rect(web_browser_rect, 15 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((320 * scale, 100 * scale), "Web\nBrowser", fill=black, font=font_tier, anchor="mm", align="center")
    
    # Client Tier Label on right
    draw.text((610 * scale, 100 * scale), "Client Tier", fill=black, font=font_tier, anchor="lm")

    # --- Dashed Line 1 ---
    draw_dashed_line((30 * scale, 210 * scale), (720 * scale, 210 * scale))

    # --- 2. Application Tier (Middle) ---
    # Django Web Server Box (Left)
    django_rect = [160 * scale, 280 * scale, 340 * scale, 460 * scale]
    draw_rounded_rect(django_rect, 12 * scale, fill=white, outline=black, width=2 * scale)
    
    # Internal Document Lines Icon for Django Box
    draw_rounded_rect([205 * scale, 305 * scale, 295 * scale, 375 * scale], 4 * scale, fill=white, outline=black, width=2 * scale)
    draw.line([(220 * scale, 322 * scale), (280 * scale, 322 * scale)], fill=black, width=2 * scale)
    draw.line([(220 * scale, 340 * scale), (280 * scale, 340 * scale)], fill=black, width=2 * scale)
    draw.line([(220 * scale, 358 * scale), (280 * scale, 358 * scale)], fill=black, width=2 * scale)
    
    draw.text((250 * scale, 420 * scale), "Django server", fill=black, font=font_tier, anchor="mm")

    # ML Inference Engine Box (Right)
    ml_rect = [440 * scale, 280 * scale, 620 * scale, 460 * scale]
    draw_rounded_rect(ml_rect, 12 * scale, fill=white, outline=black, width=2 * scale)

    # Internal Document Lines Icon for ML Box
    draw_rounded_rect([485 * scale, 305 * scale, 575 * scale, 375 * scale], 4 * scale, fill=white, outline=black, width=2 * scale)
    draw.line([(500 * scale, 322 * scale), (560 * scale, 322 * scale)], fill=black, width=2 * scale)
    draw.line([(500 * scale, 340 * scale), (560 * scale, 340 * scale)], fill=black, width=2 * scale)
    draw.line([(500 * scale, 358 * scale), (560 * scale, 358 * scale)], fill=black, width=2 * scale)

    draw.text((530 * scale, 420 * scale), "ML server", fill=black, font=font_tier, anchor="mm")

    # Connectors
    # Upward Arrow from Django Server to Web Browser
    draw_arrow((250 * scale, 280 * scale), (250 * scale, 160 * scale))
    # Horizontal Bidirectional Arrow between Django Server and ML Server
    draw_arrow((340 * scale, 370 * scale), (440 * scale, 370 * scale), bidirectional=True)

    # --- Dashed Line 2 ---
    draw_dashed_line((30 * scale, 520 * scale), (720 * scale, 520 * scale))

    # --- 3. Database Tier (Bottom) ---
    # db.sqlite3 File Icon
    db_rect = [160 * scale, 560 * scale, 340 * scale, 710 * scale]
    draw_file_icon(db_rect, 25 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((250 * scale, 645 * scale), "db.sqlite3\nFile", fill=black, font=font_tier, anchor="mm", align="center")

    # CSV File Icon
    csv_rect = [440 * scale, 560 * scale, 620 * scale, 710 * scale]
    draw_file_icon(csv_rect, 25 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((530 * scale, 645 * scale), "CSV / H5\nFiles", fill=black, font=font_tier, anchor="mm", align="center")

    # Database Tier Labels
    draw.text((640 * scale, 615 * scale), "Database Tier", fill=black, font=font_tier, anchor="lm")
    draw.text((640 * scale, 675 * scale), "Database Tier", fill=black, font=font_tier, anchor="lm") # Replicate the double-label from the user's diagram

    # Database Connections (Bidirectional arrows between servers and databases)
    draw_arrow((250 * scale, 560 * scale), (250 * scale, 460 * scale), bidirectional=True)
    draw_arrow((530 * scale, 560 * scale), (530 * scale, 460 * scale), bidirectional=True)

    # Resize and save
    final_img = img.resize((750, 750), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_system_architecture.png", "PNG")
    print("Generated smart_farming_system_architecture.png successfully!")

if __name__ == "__main__":
    create_architecture_diagram()
