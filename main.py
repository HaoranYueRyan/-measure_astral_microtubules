import os
import matplotlib
matplotlib.use('TkAgg')
from measure_area import load_image,threshold_image,measure_area,denoise_image
import natsort
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import numpy as np
from skimage import  filters
folder_path = './astral_microtubules/'
# folder_path = './astral_microtubules_2/'
# folder_path = './images2/'
image_extensions = ('.tif', '.png', '.jpg', '.jpeg', '.bmp')

image_names = [folder_path+filename for filename in os.listdir(folder_path) if filename.lower().endswith(image_extensions)]
image_names= natsort.natsorted(image_names)

def main(image_paths,):
    area_list = []
    threshold_list = []
    fixed_threshold = 0
    mean_increment = (0.8) / (len(image_paths)*2) # Set the mean increment so that the threshold reaches about 0.5 after 150 images
    std_dev = 0.01  # Adjust this value to control the spread of the normal distribution

    for image_path in image_paths:
        image_gray = load_image(image_path)

        current_threshold = filters.threshold_otsu(image_gray)
        print(current_threshold)

        # Update threshold using a normal distribution
        increment = np.random.normal(loc=mean_increment, scale=std_dev)
        fixed_threshold += increment
        fixed_threshold = min(fixed_threshold, 1)  # Limit the maximum threshold to 1


        # Define the contrast adjustment value (values greater than 1 increase contrast, values between 0 and 1 decrease contrast)
        contrast_adjustment =2
        # Define the brightness adjustment value (positive value to increase brightness, negative value to decrease)
        brightness_adjustment = 0.45

        # Adjust the contrast and brightness of the image
        adjusted_image = image_gray* contrast_adjustment - brightness_adjustment
        threshold_list.append(fixed_threshold)

        adjusted_image = adjusted_image * (adjusted_image > fixed_threshold)
        # Clip the pixel values to the valid range (0-1)
        adjusted_image = np.clip(adjusted_image, 0, 1)
        binary_image = np.ones_like(adjusted_image) * (adjusted_image != 0)
        cv2.imwrite(f"./binary_output/{os.path.basename(image_path)}", (binary_image * 255).astype(np.uint8))
        # binary_image = adjusted_image > fixed_threshold
        # denoised_image = denoise_image(binary_image)

        cv2.imwrite(f"./overly_output/{os.path.basename(image_path)}", (adjusted_image * 255).astype(np.uint8))
        # total_area = measure_area(binary_image)
        # area_list.append(total_area)

    plt.plot(threshold_list)
    # Add labels and title (optional)
    plt.xlabel('times')
    plt.ylabel('area')
    plt.title('area of astral microtubules ')
    # Display the plot
    plt.show()

    return area_list





if __name__=="__main__":
    main(image_names)
