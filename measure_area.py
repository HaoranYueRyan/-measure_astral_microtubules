import cv2
import numpy as np
from skimage import io, filters, measure
import matplotlib.pyplot as plt

# Load and preprocess the image
def load_image(image_url):
    image_gray = io.imread(image_url)
    return image_gray

# Threshold the image to detect astral microtubules
def threshold_image(image_gray):
    threshold_value = filters.threshold_otsu(image_gray)
    binary_image = image_gray > threshold_value
    return binary_image

# Measure the total area of the microtubules
def measure_area(binary_image):
    label_image = measure.label(binary_image)
    regions = measure.regionprops(label_image)
    area_list=[region.area for region in regions]
    centre_area=max(area_list)
    total_area = sum(area_list)

    return centre_area,total_area

if __name__ == "__main__":
    image_url = "./images/exp2022_H1299_EB3-mKate2_SiR-DNA_pi-EB1-GFP_set11_STLC_CilioDi_cell1_R3D_D3D_t149_c002.tif"
    image_gray = load_image(image_url)
    # cv2.imwrite('gray_image_{0}_{1}.png', image_gray.astype(np.uint8) * 255)
    binary_image = threshold_image(image_gray)
    centre_area,total_area = measure_area(binary_image)
    print(f"The centre area of astral microtubules is: {centre_area} pixels\n "  
          f"The total area of astral microtubules is: {total_area} pixels")
