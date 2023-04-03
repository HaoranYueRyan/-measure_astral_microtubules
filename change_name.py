import os
import re

folder_path = './overly_output/'

for filename in os.listdir(folder_path):
    if filename.endswith('.tif'):
        old_name = os.path.join(folder_path, filename)
        new_name = os.path.join(folder_path, re.sub(r'_c\d+', '', filename))
        os.rename(old_name, new_name)
