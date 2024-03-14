import gradio as gr
from promptsBase import *
import time
import os

import os
os.system("mkdir Shanghai_AI_Laboratory")
os.system("wget -O internlm-xcomposer2-7b.zip https://bj.bcebos.com/v1/ai-studio-online/a555f79d63e34a4b85c6c5edb23305a2843ff32171554c90af8048301f8d1eb7?responseContentDisposition=attachment%3B%20filename%3Dinternlm-xcomposer2-7b.zip&authorization=bce-auth-v1%2F5cfe9a5e1454405eb2a975c43eace6ec%2F2024-03-14T14%3A50%3A42Z%2F-1%2F%2F377d77f7224b1cb96a69aa8de8df0867a08654d90acf04e862cbe4b628d236f2")
os.system("ls")
os.system("unzip internlm-xcomposer2-7b.zip -d Shanghai_AI_Laboratory/")
os.system("pip install modelscope")
os.system("pip install modelscope[multi-modal]")
os.system("pip install torch==2.1.2 torchvision")

from internlmXcomposer import predict, model,defaultImage

def clear_fn(value):
    return "",None, "请上传儿童插画的照片，并输入故事主题"

def recognize(theme, webcam):  # webcam is rgb
    if webcam is not None:
        print('theme', theme)
        print(webcam.size)
        result = predict(prompts1, theme, imageList=[webcam])
    else:
        result = "【请先上传图片或选默认照片后，再按生成按钮】"
    return result

with gr.Blocks() as demo:
    with gr.Column():
        theme = gr.Textbox(label='故事主题', lines=3)
        gr.Examples(["早上起床要刷牙"],theme,label="",)
        webcam = gr.Image(label="",source="upload", type="pil")
        # 使用设置好的图像组件创建Examples组件
        gr.Examples([defaultImage], webcam, label="")
        show=gr.Button("请上传儿童插画的照片，并输入故事主题")
        with gr.Row():
            submit = gr.Button("生成🚀")
            clear = gr.Button("清除🧹")
        # output_string = gr.Textbox()
    submit.click(fn=recognize, inputs=[theme, webcam], outputs=show)
    clear.click(fn=clear_fn, inputs=clear, outputs=[theme,webcam, show])
demo.queue(status_update_rate=1).launch(server_name="0.0.0.0", share=False)
