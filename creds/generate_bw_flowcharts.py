import os
from PIL import Image, ImageDraw, ImageFont

# Set up standard paths
FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "arial.ttf"

def create_crop_flowchart_bw():
    # Draw at 2x resolution and scale down to 1x for crisp anti-aliasing
    scale = 2
    width, height = 900 * scale, 800 * scale
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_box = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 11 * scale)
    except Exception:
        font_box = ImageFont.load_default()
        font_label = ImageFont.load_default()

    black = (0, 0, 0)
    white = (255, 255, 255)

    def draw_rounded_rect(rect, r, fill, outline, width=2):
        x0, y0, x1, y1 = rect
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

    def draw_diamond(center, w, h, fill, outline, width=2):
        cx, cy = center
        w_half, h_half = w // 2, h // 2
        coords = [
            (cx, cy - h_half),  # Top
            (cx + w_half, cy),  # Right
            (cx, cy + h_half),  # Bottom
            (cx - w_half, cy)   # Left
        ]
        draw.polygon(coords, fill=fill, outline=outline, width=width)

    def draw_arrow(start, end, label="", label_pos="left"):
        # Draw line
        draw.line([start, end], fill=black, width=2 * scale)
        x1, y1 = start
        x2, y2 = end
        # Draw arrow head
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10 * scale
        px1 = x2 - arrow_len * math.cos(angle - math.pi/6)
        py1 = y2 - arrow_len * math.sin(angle - math.pi/6)
        px2 = x2 - arrow_len * math.cos(angle + math.pi/6)
        py2 = y2 - arrow_len * math.sin(angle + math.pi/6)
        draw.polygon([end, (px1, py1), (px2, py2)], fill=black)
        
        if label:
            lx = (x1 + x2) // 2
            ly = (y1 + y2) // 2
            if label_pos == "left":
                draw.text((lx - 8 * scale, ly), label, fill=black, font=font_label, anchor="rm")
            elif label_pos == "right":
                draw.text((lx + 8 * scale, ly), label, fill=black, font=font_label, anchor="lm")
            elif label_pos == "above":
                draw.text((lx, ly - 8 * scale), label, fill=black, font=font_label, anchor="mb")
            elif label_pos == "below":
                draw.text((lx, ly + 8 * scale), label, fill=black, font=font_label, anchor="mt")

    # 1. Start circle
    start_cx, start_cy = 80 * scale, 130 * scale
    start_r = 25 * scale
    draw.ellipse([start_cx - start_r, start_cy - start_r, start_cx + start_r, start_cy + start_r], fill=white, outline=black, width=2 * scale)

    # Arrow from Start to Form
    draw_arrow((start_cx + start_r, start_cy), (160 * scale, 130 * scale))

    # 2. Crop Recommendation Form (Left)
    draw_rounded_rect([160 * scale, 80 * scale, 340 * scale, 180 * scale], 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((250 * scale, 130 * scale), "Crop Recommendation\nForm", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Form to Valid?
    draw_arrow((340 * scale, 130 * scale), (420 * scale, 130 * scale))

    # 3. Decision Diamond: Valid?
    diamond_center = (470 * scale, 130 * scale)
    draw_diamond(diamond_center, 100 * scale, 100 * scale, fill=white, outline=black, width=2 * scale)
    draw.text(diamond_center, "Valid?", fill=black, font=font_box, anchor="mm")

    # No branch
    # Line goes right from right vertex (520, 130) to (730, 130), then down to (730, 250)
    draw.line([(520 * scale, 130 * scale), (730 * scale, 130 * scale)], fill=black, width=2 * scale)
    draw.text((580 * scale, 130 * scale - 8 * scale), "No", fill=black, font=font_label, anchor="mb")
    draw_arrow((730 * scale, 130 * scale), (730 * scale, 250 * scale))

    # Yes branch
    # Line goes down from bottom vertex (470, 180) to (470, 250)
    draw_arrow((470 * scale, 180 * scale), (470 * scale, 250 * scale), "Yes", "right")

    # 4. Random Forest & SVM Models (Linear Regression Model equivalent)
    model_rect = [380 * scale, 250 * scale, 560 * scale, 350 * scale]
    draw_rounded_rect(model_rect, 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((470 * scale, 300 * scale), "Random Forest &\nSVM Models", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Model to Form (Right)
    draw_arrow((560 * scale, 300 * scale), (640 * scale, 300 * scale))

    # 5. Crop Recommendation Form (Right)
    draw_rounded_rect([640 * scale, 250 * scale, 820 * scale, 350 * scale], 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((730 * scale, 300 * scale), "Crop Recommendation\nForm", fill=black, font=font_box, anchor="mm", align="center")

    # Bidirectional arrows to algorithms
    # Arrow down: Gives Input
    draw_arrow((430 * scale, 350 * scale), (430 * scale, 470 * scale), "Gives Input", "left")
    # Arrow up: Receives Prediction
    draw_arrow((510 * scale, 470 * scale), (510 * scale, 350 * scale), "Receives Prediction", "right")

    # 6. Random Forest & SVM Algorithms (Linear Regression Algorithm equivalent)
    algo_rect = [380 * scale, 470 * scale, 560 * scale, 570 * scale]
    draw_rounded_rect(algo_rect, 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((470 * scale, 520 * scale), "Random Forest &\nSVM Algorithms", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Algorithms down to End
    draw_arrow((470 * scale, 570 * scale), (470 * scale, 650 * scale))

    # 7. End double circle
    end_cx, end_cy = 470 * scale, 685 * scale
    outer_r = 30 * scale
    inner_r = 22 * scale
    draw.ellipse([end_cx - outer_r, end_cy - outer_r, end_cx + outer_r, end_cy + outer_r], fill=white, outline=black, width=2 * scale)
    draw.ellipse([end_cx - inner_r, end_cy - inner_r, end_cx + inner_r, end_cy + inner_r], fill=white, outline=black, width=2 * scale)

    # Resize and save
    final_img = img.resize((900, 800), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_crop_flowchart_bw.png", "PNG")
    print("Generated smart_farming_crop_flowchart_bw.png successfully!")

def create_disease_flowchart_bw():
    scale = 2
    width, height = 900 * scale, 800 * scale
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_box = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 11 * scale)
    except Exception:
        font_box = ImageFont.load_default()
        font_label = ImageFont.load_default()

    black = (0, 0, 0)
    white = (255, 255, 255)

    def draw_rounded_rect(rect, r, fill, outline, width=2):
        x0, y0, x1, y1 = rect
        draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=outline, width=width)

    def draw_diamond(center, w, h, fill, outline, width=2):
        cx, cy = center
        w_half, h_half = w // 2, h // 2
        coords = [
            (cx, cy - h_half),
            (cx + w_half, cy),
            (cx, cy + h_half),
            (cx - w_half, cy)
        ]
        draw.polygon(coords, fill=fill, outline=outline, width=width)

    def draw_arrow(start, end, label="", label_pos="left"):
        draw.line([start, end], fill=black, width=2 * scale)
        x1, y1 = start
        x2, y2 = end
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10 * scale
        px1 = x2 - arrow_len * math.cos(angle - math.pi/6)
        py1 = y2 - arrow_len * math.sin(angle - math.pi/6)
        px2 = x2 - arrow_len * math.cos(angle + math.pi/6)
        py2 = y2 - arrow_len * math.sin(angle + math.pi/6)
        draw.polygon([end, (px1, py1), (px2, py2)], fill=black)
        
        if label:
            lx = (x1 + x2) // 2
            ly = (y1 + y2) // 2
            if label_pos == "left":
                draw.text((lx - 8 * scale, ly), label, fill=black, font=font_label, anchor="rm")
            elif label_pos == "right":
                draw.text((lx + 8 * scale, ly), label, fill=black, font=font_label, anchor="lm")
            elif label_pos == "above":
                draw.text((lx, ly - 8 * scale), label, fill=black, font=font_label, anchor="mb")
            elif label_pos == "below":
                draw.text((lx, ly + 8 * scale), label, fill=black, font=font_label, anchor="mt")

    # 1. Start circle
    start_cx, start_cy = 80 * scale, 130 * scale
    start_r = 25 * scale
    draw.ellipse([start_cx - start_r, start_cy - start_r, start_cx + start_r, start_cy + start_r], fill=white, outline=black, width=2 * scale)

    # Arrow from Start to Form
    draw_arrow((start_cx + start_r, start_cy), (160 * scale, 130 * scale))

    # 2. Leaf Disease Diagnostics Form (Left)
    draw_rounded_rect([160 * scale, 80 * scale, 340 * scale, 180 * scale], 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((250 * scale, 130 * scale), "Leaf Diagnostics\nForm", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Form to Valid?
    draw_arrow((340 * scale, 130 * scale), (420 * scale, 130 * scale))

    # 3. Decision Diamond: Valid? (Allowed File Extension?)
    diamond_center = (470 * scale, 130 * scale)
    draw_diamond(diamond_center, 100 * scale, 100 * scale, fill=white, outline=black, width=2 * scale)
    draw.text(diamond_center, "Valid?", fill=black, font=font_box, anchor="mm")

    # No branch
    # Line goes right from right vertex to (730, 130), then down to top of right form box
    draw.line([(520 * scale, 130 * scale), (730 * scale, 130 * scale)], fill=black, width=2 * scale)
    draw.text((580 * scale, 130 * scale - 8 * scale), "No", fill=black, font=font_label, anchor="mb")
    draw_arrow((730 * scale, 130 * scale), (730 * scale, 250 * scale))

    # Yes branch
    # Line goes down to MobileNetV2 & Custom CNN Model Layer
    draw_arrow((470 * scale, 180 * scale), (470 * scale, 250 * scale), "Yes", "right")

    # 4. MobileNetV2 & Custom CNN Models (Model Layer)
    model_rect = [380 * scale, 250 * scale, 560 * scale, 350 * scale]
    draw_rounded_rect(model_rect, 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((470 * scale, 300 * scale), "MobileNetV2 &\nCustom CNN Models", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Model to Form (Right)
    draw_arrow((560 * scale, 300 * scale), (640 * scale, 300 * scale))

    # 5. Leaf Disease Diagnostics Form (Right)
    draw_rounded_rect([640 * scale, 250 * scale, 820 * scale, 350 * scale], 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((730 * scale, 300 * scale), "Leaf Diagnostics\nForm", fill=black, font=font_box, anchor="mm", align="center")

    # Bidirectional arrows to algorithms
    # Arrow down: Gives Input
    draw_arrow((430 * scale, 350 * scale), (430 * scale, 470 * scale), "Gives Input", "left")
    # Arrow up: Receives Prediction
    draw_arrow((510 * scale, 470 * scale), (510 * scale, 350 * scale), "Receives Prediction", "right")

    # 6. MobileNetV2 & Custom CNN Algorithms
    algo_rect = [380 * scale, 470 * scale, 560 * scale, 570 * scale]
    draw_rounded_rect(algo_rect, 12 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((470 * scale, 520 * scale), "MobileNetV2 &\nCustom CNN Algos", fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Algorithms down to End
    draw_arrow((470 * scale, 570 * scale), (470 * scale, 650 * scale))

    # 7. End double circle
    end_cx, end_cy = 470 * scale, 685 * scale
    outer_r = 30 * scale
    inner_r = 22 * scale
    draw.ellipse([end_cx - outer_r, end_cy - outer_r, end_cx + outer_r, end_cy + outer_r], fill=white, outline=black, width=2 * scale)
    draw.ellipse([end_cx - inner_r, end_cy - inner_r, end_cx + inner_r, end_cy + inner_r], fill=white, outline=black, width=2 * scale)

    # Resize and save
    final_img = img.resize((900, 800), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_disease_flowchart_bw.png", "PNG")
    print("Generated smart_farming_disease_flowchart_bw.png successfully!")

if __name__ == "__main__":
    create_crop_flowchart_bw()
    create_disease_flowchart_bw()
