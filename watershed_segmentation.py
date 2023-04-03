import os
import numpy as np
import cv2
from measure_area import load_image,threshold_image,measure_area,denoise_image
from skimage import io, filters, morphology, segmentation, measure, feature
from scipy import ndimage as ndi
import natsort
import matplotlib.pyplot as plt
import cv2
import natsort
import numpy as np
import os
from skimage import filters, morphology, measure, feature, segmentation
from scipy import ndimage as ndi


def main(folder_path):
    image_extensions = ('.tif', '.png', '.jpg', '.jpeg', '.bmp')

    image_names = [folder_path+filename for filename in os.listdir(folder_path) if filename.lower().endswith(image_extensions)]
    image_names = natsort.natsorted(image_names)
    fixed_threshold = 0.20
    mean_increment = 0.8 / (151*2)
    std_dev = 0.005
    threshold_list = []

    for image_path in image_names:
        increment = np.random.normal(loc=mean_increment, scale=std_dev)
        fixed_threshold += increment
        fixed_threshold = min(fixed_threshold, 1)
        threshold_list.append(fixed_threshold)
        # print(fixed_threshold)
        image = load_image(image_path)
        binary_image = process_image(image,fixed_threshold)
        binary_image = binary_image != 0
        cv2.imwrite(f"./binary_output/{os.path.basename(image_path)}", (binary_image * 255).astype(np.uint8))
        adjusted_image = binary_image * image
        cv2.imwrite(f"./overly_output/{os.path.basename(image_path)}", (adjusted_image * 255).astype(np.uint8))


    plt.plot(threshold_list)
    # Add labels and title (optional)
    plt.xlabel('times')
    plt.ylabel('area')
    plt.title('area of astral microtubules ')
    # Display the plot
    plt.show()
def process_image(image,threshold):
    print(threshold)



    contrast_adjustment = 2
    brightness_adjustment = 0.45

    adjusted_image = image * contrast_adjustment - brightness_adjustment
    adjusted_image = np.clip(adjusted_image, 0, 1)
    adjusted_image = adjusted_image * (adjusted_image > threshold)
    


    binary_image = adjusted_image > threshold

    selem = morphology.disk(3)
    opened_image = morphology.opening(binary_image, selem)

    distance = ndi.distance_transform_edt(opened_image)
    local_maxi = feature.peak_local_max(distance, footprint=np.ones((3, 3)), labels=opened_image, exclude_border=False, indices=False)


    markers = measure.label(local_maxi)
    segmented_image = segmentation.watershed(-distance, markers, mask=opened_image)

    return segmented_image

if __name__=="__main__":
    folder_path = './astral_microtubules/'
    # folder_path = './astral_microtubules_2/'
    # folder_path = './images2/'

    main(folder_path)
