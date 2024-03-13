import gradio as gr
from promptsBase import *
from internlmXcomposer import predict, model,defaultImage
import time
import os


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