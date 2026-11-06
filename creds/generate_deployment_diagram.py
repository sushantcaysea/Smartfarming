import os
import math
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "arial.ttf"

def create_deployment_diagram():
    scale = 2
    width, height = 1000 * scale, 620 * scale
    img = Image.new("RGB", (width, height), (255, 255, 255))
    img_draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_box = ImageFont.truetype(FONT_PATH, 12 * scale)
        font_header = ImageFont.truetype(FONT_PATH, 14 * scale)
        font_label = ImageFont.truetype(FONT_PATH, 11 * scale)
    except Exception:
        font_box = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_label = ImageFont.load_default()

    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (230, 230, 230)

    def draw_custom_rounded_rect(draw_obj, rect, r, fill, outline, width=2, tl=True, tr=True, br=True, bl=True):
        x0, y0, x1, y1 = rect
        points = []
        
        # Top-Left corner
        if tl and r > 0:
            for i in range(16):
                angle = math.pi + (i / 15.0) * (math.pi / 2.0)
                x = x0 + r + r * math.cos(angle)
                y = y0 + r + r * math.sin(angle)
                points.append((x, y))
        else:
            points.append((x0, y0))
            
        # Top-Right corner
        if tr and r > 0:
            for i in range(16):
                angle = 1.5 * math.pi + (i / 15.0) * (math.pi / 2.0)
                x = x1 - r + r * math.cos(angle)
                y = y0 + r + r * math.sin(angle)
                points.append((x, y))
        else:
            points.append((x1, y0))
            
        # Bottom-Right corner
        if br and r > 0:
            for i in range(16):
                angle = 0.0 + (i / 15.0) * (math.pi / 2.0)
                x = x1 - r + r * math.cos(angle)
                y = y1 - r + r * math.sin(angle)
                points.append((x, y))
        else:
            points.append((x1, y1))
            
        # Bottom-Left corner
        if bl and r > 0:
            for i in range(16):
                angle = 0.5 * math.pi + (i / 15.0) * (math.pi / 2.0)
                x = x0 + r + r * math.cos(angle)
                y = y1 - r + r * math.sin(angle)
                points.append((x, y))
        else:
            points.append((x0, y1))
            
        # Draw filled polygon
        draw_obj.polygon(points, fill=fill, outline=outline, width=width)

    def draw_package(rect, tab_w, tab_h, fill, outline, width=2):
        x0, y0, x1, y1 = rect
        r = 10 * scale
        
        # 1. Draw Tab: rounded top-left and top-right, sharp bottom-left and bottom-right
        tab_rect = [x0, y0 - tab_h, x0 + tab_w, y0]
        draw_custom_rounded_rect(img_draw, tab_rect, r, fill, outline, width, tl=True, tr=True, br=False, bl=False)
        
        # 2. Draw Main Box: rounded top-right, bottom-right, bottom-left, sharp top-left
        draw_custom_rounded_rect(img_draw, [x0, y0, x1, y1], r, fill, outline, width, tl=False, tr=True, br=True, bl=True)
        
        # 3. Cover boundary line between tab and main box
        img_draw.line([(x0 + width // 2, y0), (x0 + tab_w - width // 2, y0)], fill=fill, width=width)

    def draw_component(rect, fill, outline, width=2, squares_left=True):
        x0, y0, x1, y1 = rect
        # Draw main box
        img_draw.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
        
        # Draw the two small squares sticking out of the border
        sq_w = 20 * scale
        sq_h = 16 * scale
        h_quarter = (y1 - y0) // 4
        
        if squares_left:
            # Squares sticking out on the left side completely (no overlapping inside)
            sq_x0 = x0 - sq_w
            sq_x1 = x0
            
            # Square 1
            y_c1 = y0 + h_quarter
            img_draw.rectangle([sq_x0, y_c1 - sq_h // 2, sq_x1, y_c1 + sq_h // 2], fill=fill, outline=outline, width=width)
            # Square 2
            y_c2 = y0 + 3 * h_quarter
            img_draw.rectangle([sq_x0, y_c2 - sq_h // 2, sq_x1, y_c2 + sq_h // 2], fill=fill, outline=outline, width=width)
        else:
            # Squares sticking out on the right side completely (no overlapping inside)
            sq_x0 = x1
            sq_x1 = x1 + sq_w
            
            # Square 1
            y_c1 = y0 + h_quarter
            img_draw.rectangle([sq_x0, y_c1 - sq_h // 2, sq_x1, y_c1 + sq_h // 2], fill=fill, outline=outline, width=width)
            # Square 2
            y_c2 = y0 + 3 * h_quarter
            img_draw.rectangle([sq_x0, y_c2 - sq_h // 2, sq_x1, y_c2 + sq_h // 2], fill=fill, outline=outline, width=width)

    def draw_3d_node(rect, dx, dy, fill_front, fill_depth, outline, width=2):
        x0, y0, x1, y1 = rect
        
        # Coordinates of vertices
        # Front face
        f_tl = (x0, y0)
        f_tr = (x1, y0)
        f_br = (x1, y1)
        f_bl = (x0, y1)
        
        # Back face
        b_tl = (x0 - dx, y0 - dy)
        b_tr = (x1 - dx, y0 - dy)
        b_br = (x1 - dx, y1 - dy)
        b_bl = (x0 - dx, y1 - dy)
        
        # Draw top depth panel
        img_draw.polygon([f_tl, b_tl, b_tr, f_tr], fill=fill_depth, outline=outline, width=width)
        # Draw left depth panel
        img_draw.polygon([f_tl, b_tl, b_bl, f_bl], fill=fill_depth, outline=outline, width=width)
        # Draw front face
        img_draw.polygon([f_tl, f_tr, f_br, f_bl], fill=fill_front, outline=outline, width=width)

    def draw_arrow(start, end):
        img_draw.line([start, end], fill=black, width=2 * scale)
        x1, y1 = start
        x2, y2 = end
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10 * scale
        px1 = x2 - arrow_len * math.cos(angle - math.pi/6)
        py1 = y2 - arrow_len * math.sin(angle - math.pi/6)
        px2 = x2 - arrow_len * math.cos(angle + math.pi/6)
        py2 = y2 - arrow_len * math.sin(angle + math.pi/6)
        img_draw.polygon([end, (px1, py1), (px2, py2)], fill=black)

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
            img_draw.line([(x1 + curr_dist * cos, y1 + curr_dist * sin), 
                           (x1 + next_dist * cos, y1 + next_dist * sin)], fill=black, width=1 * scale)
            curr_dist += dash_len + gap_len

    # --- 1. Draw 3D Device Node (Bottom-Left) ---
    device_rect = [50 * scale, 340 * scale, 240 * scale, 520 * scale]
    # Shaded top and left panels, white front panel
    draw_3d_node(device_rect, 20 * scale, 20 * scale, white, grey, black, width=2 * scale)
    img_draw.text((60 * scale, 345 * scale), "Device", fill=black, font=font_header)

    # Draw inner component: <<webapps>> DPS equivalent
    # We position it inside the front face of the 3D box
    inner_comp_rect = [80 * scale, 390 * scale, 210 * scale, 490 * scale]
    draw_component(inner_comp_rect, fill=white, outline=black, width=2 * scale, squares_left=False)
    img_draw.text((145 * scale, 420 * scale), "<<webapps>>\nSmartFarming", fill=black, font=font_box, anchor="mm", align="center")

    # --- 2. Draw Input Interfaces (Middle-Left Packages) ---
    # Crop Details Input Interface Package (Top-Middle-Left)
    crop_input_rect = [360 * scale, 120 * scale, 540 * scale, 210 * scale]
    draw_package(crop_input_rect, 40 * scale, 15 * scale, fill=white, outline=black, width=2 * scale)
    img_draw.text((450 * scale, 165 * scale), "Crop Details\nInput Interface", fill=black, font=font_box, anchor="mm", align="center")

    # Leaf Image Upload Interface Package (Bottom-Middle-Left)
    leaf_input_rect = [360 * scale, 230 * scale, 540 * scale, 320 * scale]
    draw_package(leaf_input_rect, 40 * scale, 15 * scale, fill=white, outline=black, width=2 * scale)
    img_draw.text((450 * scale, 275 * scale), "Leaf Image\nUpload Interface", fill=black, font=font_box, anchor="mm", align="center")

    # --- 3. Draw ML Components (Middle-Bottom Components) ---
    # Crop Recommendation Model (Scikit-Learn Random Forest & SVM)
    crop_model_rect = [360 * scale, 370 * scale, 540 * scale, 460 * scale]
    draw_component(crop_model_rect, fill=white, outline=black, width=2 * scale, squares_left=True)
    img_draw.text((455 * scale, 415 * scale), "Crop Recommendation\nModel", fill=black, font=font_box, anchor="mm", align="center")

    # Disease Detection Model (MobileNetV2 & Custom CNN)
    disease_model_rect = [360 * scale, 490 * scale, 540 * scale, 580 * scale]
    draw_component(disease_model_rect, fill=white, outline=black, width=2 * scale, squares_left=True)
    img_draw.text((455 * scale, 535 * scale), "Disease Detection\nModel", fill=black, font=font_box, anchor="mm", align="center")

    # --- 4. Draw Dashed Connections from Device ---
    # Connections go from front-right edge of 3D node (X = 240, Y = 430)
    draw_dashed_line((240 * scale, 430 * scale), (360 * scale, 165 * scale))
    draw_dashed_line((240 * scale, 430 * scale), (360 * scale, 275 * scale))
    draw_dashed_line((240 * scale, 430 * scale), (340 * scale, 415 * scale))
    draw_dashed_line((240 * scale, 430 * scale), (340 * scale, 535 * scale))

    # --- 5. Draw Session Package (Top-Right) ---
    session_rect = [670 * scale, 90 * scale, 950 * scale, 290 * scale]
    draw_package(session_rect, 60 * scale, 20 * scale, fill=white, outline=black, width=2 * scale)
    img_draw.text((810 * scale, 115 * scale), "Session", fill=black, font=font_header, anchor="mm")

    # Inside Session: Crop Suitability Data Component
    crop_data_rect = [700 * scale, 140 * scale, 920 * scale, 200 * scale]
    draw_component(crop_data_rect, fill=white, outline=black, width=2 * scale, squares_left=True)
    img_draw.text((815 * scale, 170 * scale), "Crop Suitability Data", fill=black, font=font_box, anchor="mm")

    # Inside Session: Leaf Diagnostics Data Component
    leaf_data_rect = [700 * scale, 215 * scale, 920 * scale, 275 * scale]
    draw_component(leaf_data_rect, fill=white, outline=black, width=2 * scale, squares_left=True)
    img_draw.text((815 * scale, 245 * scale), "Leaf Diagnostics Data", fill=black, font=font_box, anchor="mm")

    # --- 6. Draw Connectors and Stereo Dependency Labels ---
    # From Crop Model to Crop Suitability Data
    # Path: from X = 540, Y = 415 right to X = 810, Y = 415, then up to bottom of Crop Data X = 810, Y = 200
    img_draw.line([(540 * scale, 415 * scale), (810 * scale, 415 * scale)], fill=black, width=2 * scale)
    draw_arrow((810 * scale, 415 * scale), (810 * scale, 200 * scale))
    img_draw.text((810 * scale - 6 * scale, 320 * scale), "<<show crop suitability prediction data>>", fill=black, font=font_label, anchor="rm")

    # From Disease Model to Leaf Diagnostics Data
    # Path: from X = 540, Y = 535 right to X = 880, Y = 535, then up to bottom of Leaf Data X = 880, Y = 275
    img_draw.line([(540 * scale, 535 * scale), (880 * scale, 535 * scale)], fill=black, width=2 * scale)
    draw_arrow((880 * scale, 535 * scale), (880 * scale, 275 * scale))
    img_draw.text((880 * scale - 6 * scale, 380 * scale), "<<show leaf diagnostics data>>", fill=black, font=font_label, anchor="rm")

    # Resize and save
    final_img = img.resize((1000, 620), Image.Resampling.LANCZOS)
    final_img.save("smart_farming_deployment_diagram.png", "PNG")
    print("Generated smart_farming_deployment_diagram.png successfully!")

if __name__ == "__main__":
    create_deployment_diagram()
