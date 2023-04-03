import os
from PIL import Image

input_folder = "/Users/haoranyue/Desktop/input/"
output_folder = "/Users/haoranyue/Desktop/input_sample_png/"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".tif"):
        # Open the TIFF image
        input_image = Image.open(os.path.join(input_folder, filename))

        # Create the PNG filename
        png_filename = os.path.splitext(filename)[0] + ".png"

        # Save the image as PNG
        input_image.save(os.path.join(output_folder, png_filename), "PNG")
