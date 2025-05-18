import cv2
import numpy as np
import os


# Change this to the path where your screenshots are saved
# currently only works with goblin caves map. 
steam_folder = 'c:\\temp\\screenshots\\'
# Get the latest screenshot file
def get_latest_screenshot(folder):
    # Get all files in the folder
    files = os.listdir(folder)
    # Filter for .png files
    png_files = [f for f in files if f.endswith('.png')]
    # Sort by modification time
    png_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    # Return the latest file
    return os.path.join(folder, png_files[0]) if png_files else None

# Get the latest screenshot
latest_screenshot = get_latest_screenshot(steam_folder)
if latest_screenshot:
    print(f"Latest screenshot found: {latest_screenshot}")


    # Load the images
    image = cv2.imread(latest_screenshot)  # The image where you want to search the template
    template = cv2.imread('..\\maps\\cave_troll_test.png')  # The template (map section) you want to find
    
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

    # Save the result to a new file
    output_file = 'img\\output_image.png'  # Specify the output file path
    cv2.imwrite(output_file, image)

    width = int(image.shape[1] * 0.8)  # 50% of original width
    height = int(image.shape[0] * 0.8)  # 50% of original height
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    # Display the resized (zoomed-out) image
    cv2.imshow("Latest Screenshot - Zoomed Out", resized_image)

    #cv2.imshow(f'Match found at {best_angle} degrees with confidence {best_val:.2f}', image)
    cv2.waitKey(0)  # Wait for 100 ms
    cv2.destroyAllWindows()
else:
    print("No match found")
