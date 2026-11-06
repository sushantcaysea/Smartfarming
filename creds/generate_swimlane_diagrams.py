import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "arial.ttf"

def create_swimlane_diagram(title_text, system_name_slug):
    scale = 2
    width, height = 750 * scale, 950 * scale
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_box = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_header = ImageFont.truetype(FONT_PATH, 16 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 12 * scale)
        font_title = ImageFont.truetype(FONT_PATH, 20 * scale)
    except Exception:
        font_box = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_title = ImageFont.load_default()

    black = (0, 0, 0)
    white = (255, 255, 255)

    # 1. Draw Grid Frame
    # Vertical Boundaries:
    # X = 0 (left edge)
    # X = 60 * scale (Title lane end)
    # X = 290 * scale (User lane end)
    # X = 520 * scale (Algorithm lane end)
    # X = 750 * scale (System lane end)
    
    draw.rectangle([0, 0, width - 1, height - 1], outline=black, width=2 * scale)
    draw.line([(60 * scale, 0), (60 * scale, height)], fill=black, width=2 * scale)
    draw.line([(290 * scale, 0), (290 * scale, height)], fill=black, width=2 * scale)
    draw.line([(520 * scale, 0), (520 * scale, height)], fill=black, width=2 * scale)
    
    # Horizontal line for headers Y = 50 * scale
    draw.line([(60 * scale, 50 * scale), (width, 50 * scale)], fill=black, width=2 * scale)

    # 2. Draw Swimlane Headers
    draw.text((175 * scale, 25 * scale), "User", fill=black, font=font_header, anchor="mm")
    draw.text((405 * scale, 25 * scale), "Algorithm", fill=black, font=font_header, anchor="mm")
    draw.text((635 * scale, 25 * scale), "System", fill=black, font=font_header, anchor="mm")

    # 3. Draw Rotated Far-Left Title
    # We draw on a transparent canvas and rotate 90 degrees CCW
    title_w, title_h = 700 * scale, 50 * scale
    title_img = Image.new("RGBA", (title_w, title_h), (255, 255, 255, 0))
    title_draw = ImageDraw.Draw(title_img)
    title_draw.text((title_w // 2, title_h // 2), title_text, fill=black, font=font_title, anchor="mm")
    rotated_title = title_img.rotate(90, expand=True)
    
    # Paste rotated title to the far left lane Y centered
    img.paste(rotated_title, (5 * scale, (height - title_w) // 2), rotated_title)

    # Drawing helper functions
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

    # Layout Coordinates
    # Y levels:
    # Y = 100 : Start Circle
    # Y = 200 : Access Form Box
    # Y = 330 : Input details / Valid? Diamond
    # Y = 460 : Error Message Box
    # Y = 590 : Ask predictions / Predict results
    # Y = 680 : End double circle
    # Y = 800 : View Result Box (Algorithm & User)

    # 4. User Lane Elements
    # Start Circle
    start_cx, start_cy = 175 * scale, 100 * scale
    start_r = 25 * scale
    draw.ellipse([start_cx - start_r, start_cy - start_r, start_cx + start_r, start_cy + start_r], fill=white, outline=black, width=2 * scale)

    # Arrow from Start to Access Form
    draw_arrow((start_cx, start_cy + start_r), (175 * scale, 170 * scale))

    # Access Form Box
    form_text = "Access Crop\nDetails Form" if "Crop" in title_text else "Access Leaf\nUpload Form"
    draw_rounded_rect([95 * scale, 170 * scale, 255 * scale, 230 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((175 * scale, 200 * scale), form_text, fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Access Form to Input Details
    draw_arrow((175 * scale, 230 * scale), (175 * scale, 300 * scale))

    # Input Details Box
    input_text = "Input Crop\nDetails" if "Crop" in title_text else "Upload Leaf\nImage"
    draw_rounded_rect([95 * scale, 300 * scale, 255 * scale, 360 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((175 * scale, 330 * scale), input_text, fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Input Details to Valid? in System Lane
    draw_arrow((255 * scale, 330 * scale), (575 * scale, 330 * scale))

    # Error Message Box
    draw_rounded_rect([95 * scale, 430 * scale, 255 * scale, 490 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((175 * scale, 460 * scale), "Error Message", fill=black, font=font_box, anchor="mm")

    # End double circle
    end_cx, end_cy = 175 * scale, 680 * scale
    outer_r = 30 * scale
    inner_r = 22 * scale
    draw.ellipse([end_cx - outer_r, end_cy - outer_r, end_cx + outer_r, end_cy + outer_r], fill=white, outline=black, width=2 * scale)
    draw.ellipse([end_cx - inner_r, end_cy - inner_r, end_cx + inner_r, end_cy + inner_r], fill=white, outline=black, width=2 * scale)

    # View Result Box (User)
    draw_rounded_rect([95 * scale, 800 * scale, 255 * scale, 860 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((175 * scale, 830 * scale), "View Result", fill=black, font=font_box, anchor="mm")

    # Arrow going up from View Result to End
    draw_arrow((175 * scale, 800 * scale), (175 * scale, 710 * scale))


    # 5. System Lane Elements
    # Decision Diamond Valid?
    diamond_center = (635 * scale, 330 * scale)
    draw_diamond(diamond_center, 120 * scale, 120 * scale, fill=white, outline=black, width=2 * scale)
    draw.text(diamond_center, "Valid?", fill=black, font=font_box, anchor="mm")

    # No branch to Error Message (Y = 460)
    # Horizontal line from bottom of diamond (or side)
    # Let's go from bottom (635, 390) down to (635, 460), then left to (255, 460)
    draw.line([(635 * scale, 390 * scale), (635 * scale, 460 * scale)], fill=black, width=2 * scale)
    draw_arrow((635 * scale, 460 * scale), (255 * scale, 460 * scale), "No", "above")

    # Yes branch goes to Y = 560
    # From right of diamond (695, 330) or bottom? Wait, in user's image, "Yes" arrow goes from right vertex (695, 330)
    # to the right, then down, then left into "Ask Predictions from Algorithm"
    draw.line([(695 * scale, 330 * scale), (715 * scale, 330 * scale), (715 * scale, 590 * scale)], fill=black, width=2 * scale)
    draw.text((715 * scale + 6 * scale, 460 * scale), "Yes", fill=black, font=font_label, anchor="lm")
    draw_arrow((715 * scale, 590 * scale), (715 * scale - 1, 590 * scale)) # Helper to trigger arrow head
    draw_arrow((715 * scale, 590 * scale), (715 * scale - 1, 590 * scale))
    draw_arrow((715 * scale, 590 * scale), (715 * scale - 2, 590 * scale))
    # Correct horizontal arrow into box:
    draw_arrow((715 * scale, 590 * scale), (635 * scale + 80 * scale, 590 * scale))

    # Ask Predictions Box
    ask_text = "Ask Predictions\nfrom Algorithm" if "Crop" in title_text else "Ask Diagnosis\nfrom Algorithm"
    draw_rounded_rect([555 * scale, 560 * scale, 715 * scale, 620 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((635 * scale, 590 * scale), ask_text, fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Ask Predictions (System) to Predict (Algorithm)
    draw_arrow((555 * scale, 590 * scale), (485 * scale, 590 * scale))


    # 6. Algorithm Lane Elements
    # Predict the results Box
    predict_text = "Predict the\nresults" if "Crop" in title_text else "Diagnose\nplant disease"
    draw_rounded_rect([325 * scale, 560 * scale, 485 * scale, 620 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((405 * scale, 590 * scale), predict_text, fill=black, font=font_box, anchor="mm", align="center")

    # Arrow from Predict (Y = 620) down to View Result (Y = 800)
    draw_arrow((405 * scale, 620 * scale), (405 * scale, 800 * scale))

    # View Result Box (Algorithm)
    draw_rounded_rect([325 * scale, 800 * scale, 485 * scale, 860 * scale], 5 * scale, fill=white, outline=black, width=2 * scale)
    draw.text((405 * scale, 830 * scale), "View Result", fill=black, font=font_box, anchor="mm")

    # Arrow from Algorithm View Result to User View Result
    draw_arrow((325 * scale, 830 * scale), (255 * scale, 830 * scale))

    # Resize and save
    final_img = img.resize((750, 950), Image.Resampling.LANCZOS)
    final_img.save(f"{system_name_slug}_swimlane.png", "PNG")
    print(f"Generated {system_name_slug}_swimlane.png successfully!")

if __name__ == "__main__":
    create_swimlane_diagram("Crop Suitability Recommendation System", "crop_recommendation")
    create_swimlane_diagram("Leaf Disease Diagnostics System", "leaf_disease")
