import os
import shutil

source_folder = './images/'
destination_folder = './astral_microtubules/'

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for filename in os.listdir(source_folder):
    if filename.endswith("_c001.tif"):
        source_file_path = os.path.join(source_folder, filename)
        destination_file_path = os.path.join(destination_folder, filename)
        shutil.copy(source_file_path, destination_file_path)

print("Images copied successfully.")
