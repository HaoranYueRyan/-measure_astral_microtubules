import os
import matplotlib
matplotlib.use('TkAgg')
from measure_area import load_image,threshold_image,measure_area
import natsort
import matplotlib.pyplot as plt
import pandas as pd


folder_path = './astral_microtubules/'

image_extensions = ('.tif', '.png', '.jpg', '.jpeg', '.bmp')

image_names = ['./astral_microtubules/'+filename for filename in os.listdir(folder_path) if filename.lower().endswith(image_extensions)]
image_names= natsort.natsorted(image_names)

def main(images_names:list,save_name)->pd.DataFrame:
    area_list=[]
    for img in images_names:
        image_gray = load_image(img)
        # cv2.imwrite('gray_image_{0}_{1}.png', image_gray.astype(np.uint8) * 255)
        binary_image = threshold_image(image_gray)
        centre_area, total_area = measure_area(binary_image)
        area_list.append(centre_area)
        print(f"The centre area of astral microtubules is: {centre_area} pixels")

    df=pd.DataFrame(area_list)
    df.columns=['area']
    df.to_csv(f"./{save_name}.csv")
    # Create a line plot
    plt.plot(area_list)
    # Add labels and title (optional)
    plt.xlabel('times')
    plt.ylabel('area')
    plt.title('area of astral microtubules ')
    # Display the plot
    plt.show()



if __name__=="__main__":
    main(image_names,save_name='test_01')
