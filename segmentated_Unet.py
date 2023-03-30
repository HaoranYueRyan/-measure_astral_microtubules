import cv2
import torch
import numpy as np
import segmentation_models_pytorch as smp

# Load the grayscale image (replace 'image_path' with the path to your image)
image = cv2.imread( "./images/exp2022_H1299_EB3-mKate2_SiR-DNA_pi-EB1-GFP_set11_STLC_CilioDi_cell1_R3D_D3D_t001_c001.tif", cv2.IMREAD_GRAYSCALE)

# Preprocess the image for the model
preprocessed_image = np.expand_dims(image, axis=0).astype(np.float32)
preprocessed_image = torch.tensor(preprocessed_image, dtype=torch.float32).unsqueeze(0)

# Load the pre-trained U-Net model with 1 input channel
model = smp.Unet('resnet34', encoder_weights=None, in_channels=1, classes=1)
model.eval()

# Apply the model to the image
with torch.no_grad():
    mask = model(preprocessed_image)

# Postprocess the mask
mask = mask.squeeze().cpu().numpy()
mask = (mask > 0.5).astype(np.uint8) * 255

# Save the mask image
cv2.imwrite('mask.png', mask)
