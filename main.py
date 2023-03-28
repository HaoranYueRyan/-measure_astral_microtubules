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
# folder_path = './astral_microtubules/'
folder_path = './images2/'
image_extensions = ('.tif', '.png', '.jpg', '.jpeg', '.bmp')

image_names = [folder_path+filename for filename in os.listdir(folder_path) if filename.lower().endswith(image_extensions)]
image_names= natsort.natsorted(image_names)

def main(image_paths,save_name):
    area_list = []

    first_frame = True
    fixed_threshold = 0

    for image_path in image_paths:
        image_gray = load_image(image_path)

        if first_frame:
            fixed_threshold = filters.threshold_otsu(image_gray)*1.15
            first_frame = False
        else:
            current_threshold = filters.threshold_otsu(image_gray)
            if current_threshold > fixed_threshold:
                fixed_threshold = current_threshold

        binary_image = image_gray > fixed_threshold
        denoised_image = denoise_image(binary_image)
        cv2.imwrite(f"./output/{os.path.basename(image_path)}", (denoised_image.astype(np.uint8) * 255))
        centre_area, total_area = measure_area(binary_image)
        area_list.append(centre_area)

    df = pd.DataFrame(area_list)
    df.columns = ['area']
    df.to_csv(f"./{save_name}.csv")
    # Create a line plot
    plt.plot(area_list)
    # Add labels and title (optional)
    plt.xlabel('times')
    plt.ylabel('area')
    plt.title('area of astral microtubules ')
    # Display the plot
    plt.show()

    return area_list





if __name__=="__main__":
    main(image_names,save_name='test_01')
