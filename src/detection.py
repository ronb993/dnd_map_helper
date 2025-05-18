import cv2
import os

def get_latest_screenshot(folder):
    files = os.listdir(folder)
    png_files = [f for f in files if f.endswith('.png')]
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return os.path.join(folder, png_files[0]) if png_files else None

def rotate_template(template, angle):
    center = tuple([s / 2 for s in template.shape[1::-1]])
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_template = cv2.warpAffine(template, rotation_matrix, template.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated_template

def match_rotated_templates(image, template, angles):
    best_match = None
    best_val = None
    best_angle = 0
    for angle in angles:
        rotated_template = rotate_template(template, angle)
        result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if best_val is None or max_val > best_val:
            best_val = max_val
            best_match = max_loc
            best_angle = angle
    return best_match, best_angle, best_val

def detect_matches(screenshot_path, template_paths, overlay_size=(1920,1080)):
    image = cv2.imread(screenshot_path)
    if image is None:
        return [], None
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_h, img_w = image.shape[:2]
    scale_x = overlay_size[0] / img_w
    scale_y = overlay_size[1] / img_h
    angles = [0, 90, 180, 270]
    rectangles = []
    for idx, template_path in enumerate(template_paths):
        template = cv2.imread(template_path)
        if template is None:
            continue
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        best_match, best_angle, best_val = match_rotated_templates(gray_image, gray_template, angles)
        if best_match:
            h, w = template.shape[:2]
            scaled_top_left = (int(best_match[0] * scale_x), int(best_match[1] * scale_y))
            scaled_size = (int(w * scale_x), int(h * scale_y))
            rect = (*scaled_top_left, *scaled_size)
            color = (0, 255, 0, 255)
            rectangles.append((rect, color))
    return rectangles, image
