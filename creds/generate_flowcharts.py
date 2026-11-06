import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Set up standard paths
FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "arial.ttf"  # Fallback to local or system search

def create_crop_flowchart():
    # We will draw at 2x resolution and scale down to 1x for crisp anti-aliased rendering.
    scale = 2
    width, height = 800 * scale, 900 * scale
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype(FONT_PATH, 24 * scale)
        font_box = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 11 * scale)
    except Exception:
        font_title = ImageFont.load_default()
        font_box = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Brand Colors (Sleek professional theme based on project's green aesthetic)
    bg_box = (244, 250, 246, 255)  # Very soft green
    border_color = (58, 125, 68, 255)  # Primary Green #3a7d44
    text_color = (40, 50, 45, 255)  # Dark charcoal green
    line_color = (80, 90, 85, 255)  # Medium grey-green for flow lines

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

    def draw_arrow(start, end, label="", label_side="left"):
        # Draw the main line
        draw.line([start, end], fill=line_color, width=2 * scale)
        # Draw arrow head at end
        x1, y1 = start
        x2, y2 = end
        # Determine direction
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10 * scale
        px1 = x2 - arrow_len * math.cos(angle - math.pi/6)
        py1 = y2 - arrow_len * math.sin(angle - math.pi/6)
        px2 = x2 - arrow_len * math.cos(angle + math.pi/6)
        py2 = y2 - arrow_len * math.sin(angle + math.pi/6)
        draw.polygon([end, (px1, py1), (px2, py2)], fill=line_color)
        
        # Draw label
        if label:
            lx = (x1 + x2) // 2
            ly = (y1 + y2) // 2
            # Offset based on side
            if label_side == "left":
                lx -= 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="rm")
            elif label_side == "right":
                lx += 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="lm")
            elif label_side == "above":
                ly -= 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="mb")
            elif label_side == "below":
                ly += 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="mt")

    # 1. Title
    draw.text((400 * scale, 35 * scale), "Crop Suitability Recommendation Workflow", fill=border_color, font=font_title, anchor="mm")

    # 2. Start node
    start_cx, start_cy = 400 * scale, 90 * scale
    start_r = 16 * scale
    draw.ellipse([start_cx - start_r, start_cy - start_r, start_cx + start_r, start_cy + start_r], fill=(255, 255, 255, 255), outline=border_color, width=2 * scale)
    draw.text((start_cx, start_cy), "START", fill=border_color, font=font_label, anchor="mm")

    # Arrow from Start to Form
    draw_arrow((start_cx, start_cy + start_r), (400 * scale, 150 * scale))

    # 3. Crop Suitability Recommendation Form
    form_rect = [260 * scale, 150 * scale, 540 * scale, 220 * scale]
    draw_rounded_rect(form_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 185 * scale), "Crop Recommendation Form\n(N, P, K, pH, Temp, Humidity, Rainfall)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow from Form to Valid Decision
    draw_arrow((400 * scale, 220 * scale), (400 * scale, 270 * scale))

    # 4. Decision Diamond: Valid?
    diamond_center = (400 * scale, 310 * scale)
    draw_diamond(diamond_center, 140 * scale, 80 * scale, bg_box, border_color, width=2 * scale)
    draw.text(diamond_center, "Valid Data?", fill=text_color, font=font_box, anchor="mm")

    # No branch: redirects back to form
    # Draw line right, then up, then left with arrow
    draw.line([(470 * scale, 310 * scale), (600 * scale, 310 * scale), (600 * scale, 185 * scale)], fill=line_color, width=2 * scale)
    draw_arrow((600 * scale, 185 * scale), (540 * scale, 185 * scale), "No (Show Error)", "above")

    # Yes branch goes down to CropModel
    draw_arrow((400 * scale, 350 * scale), (400 * scale, 410 * scale), "Yes", "left")

    # 5. CropModel Singleton
    model_rect = [260 * scale, 410 * scale, 540 * scale, 480 * scale]
    draw_rounded_rect(model_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 445 * scale), "CropModel Singleton\n(Model Handler)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Bidirectional arrows to algorithms below
    # Arrow down: Gives inputs
    draw_arrow((360 * scale, 480 * scale), (360 * scale, 580 * scale), "Selects Algorithm & Inputs", "left")
    # Arrow up: Receives predictions
    draw_arrow((440 * scale, 580 * scale), (440 * scale, 480 * scale), "Returns Top 5 Predictions", "right")

    # 6. Ensemble Classifiers
    classifier_rect = [240 * scale, 580 * scale, 560 * scale, 650 * scale]
    draw_rounded_rect(classifier_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 615 * scale), "Machine Learning Ensemble Models\n(Random Forest & SVM Classifiers)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow from CropModel to Results View (goes right)
    draw_arrow((540 * scale, 445 * scale), (620 * scale, 445 * scale))

    # 7. Recommendations Results View
    results_rect = [620 * scale, 410 * scale, 770 * scale, 480 * scale]
    draw_rounded_rect(results_rect, 10 * scale, bg_box, outline=(60, 180, 90, 255), width=2 * scale)
    draw.text((695 * scale, 445 * scale), "Results View\n(Displays Top 5 Crops)", fill=text_color, font=font_box, anchor="mm", align="center")

    # End node
    end_cx, end_cy = 400 * scale, 770 * scale
    outer_r = 18 * scale
    inner_r = 12 * scale
    draw.ellipse([end_cx - outer_r, end_cy - outer_r, end_cx + outer_r, end_cy + outer_r], fill=(255, 255, 255, 255), outline=border_color, width=2 * scale)
    draw.ellipse([end_cx - inner_r, end_cy - inner_r, end_cx + inner_r, end_cy + inner_r], fill=border_color, outline=border_color, width=1 * scale)
    draw.text((end_cx, end_cy - 28 * scale), "END", fill=border_color, font=font_label, anchor="ms")

    # Arrow from Classifier to End
    draw_arrow((400 * scale, 650 * scale), (400 * scale, 752 * scale))

    # Arrow from Results View to End (goes down and left)
    draw.line([(695 * scale, 480 * scale), (695 * scale, 770 * scale)], fill=line_color, width=2 * scale)
    draw_arrow((695 * scale, 770 * scale), (400 * scale + outer_r, 770 * scale))

    # Scale down for super smooth antialiased edges
    final_img = img.resize((800, 900), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_crop_flowchart.png", "PNG")
    print("Generated smart_farming_crop_flowchart.png successfully!")

def create_disease_flowchart():
    scale = 2
    width, height = 800 * scale, 1000 * scale
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(FONT_PATH, 24 * scale)
        font_box = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 11 * scale)
    except Exception:
        font_title = ImageFont.load_default()
        font_box = ImageFont.load_default()
        font_label = ImageFont.load_default()

    bg_box = (244, 250, 246, 255)
    border_color = (58, 125, 68, 255)
    text_color = (40, 50, 45, 255)
    line_color = (80, 90, 85, 255)

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

    def draw_arrow(start, end, label="", label_side="left"):
        draw.line([start, end], fill=line_color, width=2 * scale)
        x1, y1 = start
        x2, y2 = end
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10 * scale
        px1 = x2 - arrow_len * math.cos(angle - math.pi/6)
        py1 = y2 - arrow_len * math.sin(angle - math.pi/6)
        px2 = x2 - arrow_len * math.cos(angle + math.pi/6)
        py2 = y2 - arrow_len * math.sin(angle + math.pi/6)
        draw.polygon([end, (px1, py1), (px2, py2)], fill=line_color)
        
        if label:
            lx = (x1 + x2) // 2
            ly = (y1 + y2) // 2
            if label_side == "left":
                lx -= 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="rm")
            elif label_side == "right":
                lx += 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="lm")
            elif label_side == "above":
                ly -= 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="mb")
            elif label_side == "below":
                ly += 10 * scale
                draw.text((lx, ly), label, fill=text_color, font=font_label, anchor="mt")

    # Title
    draw.text((400 * scale, 35 * scale), "Leaf Disease Diagnostics Workflow", fill=border_color, font=font_title, anchor="mm")

    # Start node
    start_cx, start_cy = 400 * scale, 90 * scale
    start_r = 16 * scale
    draw.ellipse([start_cx - start_r, start_cy - start_r, start_cx + start_r, start_cy + start_r], fill=(255, 255, 255, 255), outline=border_color, width=2 * scale)
    draw.text((start_cx, start_cy), "START", fill=border_color, font=font_label, anchor="mm")

    # Arrow from Start to Form
    draw_arrow((start_cx, start_cy + start_r), (400 * scale, 150 * scale))

    # Leaf Image Upload Form
    form_rect = [260 * scale, 150 * scale, 540 * scale, 220 * scale]
    draw_rounded_rect(form_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 185 * scale), "Leaf Image Upload Form\n(User selects crop leaf image file)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow to Decision: Allowed Extension?
    draw_arrow((400 * scale, 220 * scale), (400 * scale, 270 * scale))

    # Decision Diamond 1: Allowed Extension?
    diamond1_center = (400 * scale, 310 * scale)
    draw_diamond(diamond1_center, 150 * scale, 80 * scale, bg_box, border_color, width=2 * scale)
    draw.text(diamond1_center, "Allowed File Type?", fill=text_color, font=font_box, anchor="mm")

    # No branch 1: Redirects back
    draw.line([(475 * scale, 310 * scale), (620 * scale, 310 * scale), (620 * scale, 185 * scale)], fill=line_color, width=2 * scale)
    draw_arrow((620 * scale, 185 * scale), (540 * scale, 185 * scale), "No (Invalid Ext)", "above")

    # Yes branch goes down to MobileNetV2 Validation
    draw_arrow((400 * scale, 350 * scale), (400 * scale, 410 * scale), "Yes", "left")

    # MobileNetV2 Validation Layer (Phase 1)
    val_rect = [240 * scale, 410 * scale, 560 * scale, 480 * scale]
    draw_rounded_rect(val_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 445 * scale), "Phase 1: Verification Pipeline\n(MobileNetV2 Plant Material Classifier)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow down to Decision: Is Plant Leaf?
    draw_arrow((400 * scale, 480 * scale), (400 * scale, 530 * scale))

    # Decision Diamond 2: Is Plant Leaf?
    diamond2_center = (400 * scale, 570 * scale)
    draw_diamond(diamond2_center, 160 * scale, 80 * scale, bg_box, border_color, width=2 * scale)
    draw.text(diamond2_center, "Plant Verified?", fill=text_color, font=font_box, anchor="mm")

    # No branch 2: Redirects to Form (Rejects + displays warning + deletes file)
    draw.line([(480 * scale, 570 * scale), (660 * scale, 570 * scale), (660 * scale, 185 * scale)], fill=line_color, width=2 * scale)
    draw_arrow((660 * scale, 185 * scale), (540 * scale, 185 * scale), "No (Reject Image)", "above")

    # Yes branch goes down to Custom CNN
    draw_arrow((400 * scale, 610 * scale), (400 * scale, 680 * scale), "Yes (Plant Leaf)", "left")

    # Custom CNN Disease Diagnostic Model (Phase 2)
    cnn_rect = [240 * scale, 680 * scale, 560 * scale, 750 * scale]
    draw_rounded_rect(cnn_rect, 10 * scale, bg_box, border_color, width=2 * scale)
    draw.text((400 * scale, 715 * scale), "Phase 2: Diagnostics Classifier\n(Custom Deep Convolutional Neural Network)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow from CNN to Results View
    draw_arrow((400 * scale, 750 * scale), (400 * scale, 810 * scale))

    # Diagnostics Results View
    results_rect = [260 * scale, 810 * scale, 540 * scale, 880 * scale]
    draw_rounded_rect(results_rect, 10 * scale, bg_box, outline=(60, 180, 90, 255), width=2 * scale)
    draw.text((400 * scale, 845 * scale), "Diagnostics Results View\n(Displays Pathogen & Confidence %)", fill=text_color, font=font_box, anchor="mm", align="center")

    # Arrow down to End
    draw_arrow((400 * scale, 880 * scale), (400 * scale, 940 * scale))

    # End node
    end_cx, end_cy = 400 * scale, 955 * scale
    outer_r = 16 * scale
    inner_r = 10 * scale
    draw.ellipse([end_cx - outer_r, end_cy - outer_r, end_cx + outer_r, end_cy + outer_r], fill=(255, 255, 255, 255), outline=border_color, width=2 * scale)
    draw.ellipse([end_cx - inner_r, end_cy - inner_r, end_cx + inner_r, end_cy + inner_r], fill=border_color, outline=border_color, width=1 * scale)
    draw.text((end_cx, end_cy - 26 * scale), "END", fill=border_color, font=font_label, anchor="ms")

    final_img = img.resize((800, 1000), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_disease_flowchart.png", "PNG")
    print("Generated smart_farming_disease_flowchart.png successfully!")

if __name__ == "__main__":
    create_crop_flowchart()
    create_disease_flowchart()
