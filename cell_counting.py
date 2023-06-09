# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:48:41 2023

@author: binghao chai
"""

# package import
import time
import argparse
import warnings
warnings.filterwarnings("ignore") # ignore warnings
since = time.time()
import cv2
import numpy as np
from scipy import ndimage

from skimage import color, segmentation, morphology
from skimage import io

# arguments definition
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
            "--input_img",
            type = str, 
            default = "./astral_microtubules/exp2022_H1299_EB3-mKate2_SiR-DNA_pi-EB1-GFP_set11_STLC_CilioDi_cell1_R3D_D3D_t001_c001.tif",
            help = "the input image for nucleus counting" 
            )

    opt = parser.parse_args()
    print(opt)

def rgb2gray(rgb): # convert rgb image to gray scale 1-channel image
    
    # r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    gray=rgb
    return gray

# Load and preprocess the image
# Load and preprocess the image
def load_image(image_url):
    image_gray = io.imread(image_url)
    # Normalize the image to the range [0, 1]
    normalized_image = cv2.normalize(image_gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return normalized_image

# Remove small noise using morphological operations
def denoise_image(binary_image):
    selem = morphology.disk(3) # Use disk-shaped structuring element
    denoised_image = morphology.opening(binary_image, selem)
    return denoised_image
    
# image loading
# img_rgb = io.imread(f"{opt.input_img}")
img_gray = load_image(f"{opt.input_img}")
# TODO
# if we need to count the cells by their colour, 
# we could convert the rgb image to hsv using:
# img_hsv = color.rgb2hsv(img_rgb)
# then threshold filtering the Hue-channel to select colours.

# if we only need to count all the cells in the image, then covert to gray scale
# img_gray = rgb2gray(img_gray)

# # gray channel normalisation
# gray_min = img_gray.min()
# gray_max = img_gray.max()
# img_gray_norm = (img_gray - gray_min) / (gray_max - gray_min)

# find the watershed markers of the background and the nuclei
markers = np.zeros_like(img_gray)
markers[img_gray < 0.2] = 1
markers[img_gray > 0.3] = 2




# watershed segmentation the cell nuclei
seg = segmentation.watershed(img_gray, markers)
seg = ndimage.binary_fill_holes(seg - 1)

# remove small objects with boolean input "seg"
seg = morphology.remove_small_objects(seg, 10)

import matplotlib.pyplot as plt

plt.imshow(seg)
plt.show()

# generate nuclei instance map based on watershed segmentation
nuclei_instance, _ = ndimage.label(seg)
nr_nuclei = len(np.unique(nuclei_instance)) - 1 # number of nuclei (minus 1 for background removal)
print(f"Number of nuclei: {nr_nuclei}")

# debug print    
time_elapsed = time.time() - since
print("Task complete in {:.0f}m {:.0f}s".format(time_elapsed // 60, time_elapsed % 60)) 


