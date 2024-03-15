# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 23:39:26 2024

@author: ADMIN
"""

import os
import warnings
warnings.filterwarnings("ignore")
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from promptsBase import *
import torch
from modelscope import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
#ckpt_path = "Shanghai_AI_Laboratory/internlm-xcomposer2-7b-4bit"

## 模型下载
download=False
quant=False
if quant==False:
    ckpt_path = "Shanghai_AI_Laboratory/internlm-xcomposer2-7b/"

else:
    ckpt_path = "Shanghai_AI_Laboratory/internlm-xcomposer2-7b-4bit/"

if not os.path.exists(ckpt_path) or download==True:
    from modelscope import snapshot_download
    model_dir = snapshot_download(ckpt_path)
else:
    print('has model')
tokenizer = AutoTokenizer.from_pretrained(ckpt_path, trust_remote_code=True)
# `torch_dtype=torch.float16` 可以令模型以 float16 精度加载，否则 transformers 会将模型加载为 float32，导致显存不足
model = AutoModelForCausalLM.from_pretrained(ckpt_path, torch_dtype=torch.float16,
                                             trust_remote_code=True, device_map='auto',
                                                use_safetensors=False,
                                             offload_folder="offloadFolder")
model = model.eval()
defaultImage = Image.open('gushi0.jpg').convert("RGB")
def predict(prompts,theme="早上起床要刷牙",imageList=[]): #image in imageList should be rgb
    if len(imageList)==0:

        imageList=[defaultImage]

    images = []
    for image in imageList:

        image = model.vis_processor(image)
        images.append(image)
    image = torch.stack(images)
    prompts=prompts.replace("{theme}.",theme)
    query="<ImageHere>"*len(imageList)+prompts

    print("query:=",query)
    with torch.cuda.amp.autocast():
        response, history = model.chat(tokenizer, query=query, image=image, history=[], do_sample=False)
    print(response)
    return response
#query = '<ImageHere>请根据图片写一篇作文：我最喜欢的动物。要求：选准角度，确定立意，明确文体，自拟标题。'
if __name__=="__main__":
    theme="早上起床要刷牙"

    res=predict(prompts1,theme,imageList=[])