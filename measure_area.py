import cv2
import numpy as np
from skimage import io, filters, measure,morphology
import matplotlib.pyplot as plt

# Load and preprocess the image
def load_image(image_url):
    image_gray = io.imread(image_url)
    normalized_image = cv2.normalize(image_gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return normalized_image

# Threshold the image to detect astral microtubules
def threshold_image(image_gray):
    threshold_value = filters.threshold_otsu(image_gray)
    binary_image = image_gray > threshold_value*1.15
    return binary_image

def denoise_image(binary_image):
    selem = morphology.disk(3) # Use disk-shaped structuring element
    denoised_img = morphology.opening(binary_image, selem)
    return denoised_img



# Measure the total area of the microtubules
def measure_area(binary_image):
    label_image = measure.label(binary_image)
    regions = measure.regionprops(label_image)
    area_list=[region.area for region in regions]
    total_area = sum(area_list)

    return total_area

if __name__ == "__main__":
    image_url = "./images/exp2022_H1299_EB3-mKate2_SiR-DNA_pi-EB1-GFP_set11_STLC_CilioDi_cell1_R3D_D3D_t149_c001.tif"
    image_gray = load_image(image_url)
    cv2.imwrite('gray_image_{0}_{1}.png', image_gray.astype(np.uint8) * 255)
    binary_image = threshold_image(image_gray)
    cv2.imwrite('binary_image_{0}_{1}.png',binary_image.astype(np.uint8) * 255)
    centre_area = measure_area(binary_image)
    print(f"The centre area of astral microtubules is: {centre_area} pixels\n "  
          f"The total area of astral microtubules is: {total_area} pixels")
