from PIL import Image
import numpy as np

image_file_name = "k_energy_v_time/image/k_energy_x4" # no png
# Open the image file
with Image.open(image_file_name+".png") as img:
    # Convert the image to RGBA if it's not already
    img = img.convert("RGBA")
    
    # Convert the image to a numpy array
    img_array = np.array(img)
    
    # Create a mask where non-white pixels are True
    # Define the "white" threshold: RGB values close to (255, 255, 255)
    white_threshold = 240
    mask = np.all(img_array[:, :, :3] >= white_threshold, axis=-1)  # check RGB channels
    
    # Find the bounding box of the non-white area
    non_white_pixels = np.where(mask == False)
    min_x, max_x = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])
    min_y, max_y = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
    
    # Crop the image to the bounding box
    cropped_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))  # crop to the bounds
    
    # Save the cropped image
    cropped_img.save(image_file_name+"-cropped.png", format="PNG")

print("Image cropped and saved as angle-figure-cropped.png")
