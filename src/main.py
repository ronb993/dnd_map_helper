import cv2
import numpy as np

# Load the images
image = cv2.imread('img\\screenshot.png')  # The image where you want to search the template
template = cv2.imread('img\\template.png')  # The template (map section) you want to find

# Convert the image and template to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# Function to rotate the template by a given angle
def rotate_template(template, angle):
    # Get the image center
    center = tuple(np.array(template.shape[1::-1]) / 2)
    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Perform the rotation
    rotated_template = cv2.warpAffine(template, rotation_matrix, template.shape[1::-1], flags=cv2.INTER_LINEAR)
    return rotated_template

# Function to perform template matching for a list of rotated templates
def match_rotated_templates(image, template, angles, threshold=0.8):
    best_match = None
    best_val = None
    best_angle = 0
    
    # Loop over the angles (0°, 90°, 180°, 270°)
    for angle in angles:
        # Rotate the template
        rotated_template = rotate_template(template, angle)
        
        # Perform template matching
        result = cv2.matchTemplate(image, rotated_template, cv2.TM_CCOEFF_NORMED)
        
        # Check for best match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if best_val is None or max_val > best_val:
            best_val = max_val
            best_match = max_loc
            best_angle = angle
    
    return best_match, best_angle, best_val

# Define angles for rotation (0, 90, 180, 270 degrees)
angles = [0, 90, 180, 270]

# Perform matching for all rotations
best_match, best_angle, best_val = match_rotated_templates(gray_image, gray_template, angles)

# If a match was found
if best_match:
    top_left = best_match
    h, w = template.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # Draw rectangle around the matched area
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    # Show the result
    cv2.imshow(f'Match found at {best_angle} degrees with confidence {best_val:.2f}', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No match found")
