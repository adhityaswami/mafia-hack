from transformers import DPTImageProcessor, DPTForDepthEstimation
import torch
import numpy as np
from PIL import Image
from tqdm.notebook import tqdm
import os
import cv2
import json


# In[3]:


processor = DPTImageProcessor.from_pretrained("Intel/dpt-large")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large").to('cuda')


# In[4]:


image_files = [os.path.join('MiDaS/input', element) for element in os.listdir('MiDaS/input')]


# In[5]:


def process(image_path):
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt").to('cuda')

    with torch.no_grad():
        outputs = model(**inputs)
        predicted_depth = outputs.predicted_depth

    # interpolate to original size
    prediction = torch.nn.functional.interpolate(
        predicted_depth.unsqueeze(1),
        size=image.size[::-1],
        mode="bicubic",
        align_corners=False,
    )

    return prediction


# In[6]:


outputs = []
for image in tqdm(image_files):
    outputs.append(process(image))


# In[12]:


for idx, op in enumerate(outputs):
    output = op.squeeze().cpu().numpy()
    formatted = (output / np.max(output))
    resized = cv2.resize(formatted, (128, 128))
    with open('MiDaS/output/' + str(idx) + '.json', 'w') as jsonfile:
        json.dump(resized.tolist(), jsonfile)
