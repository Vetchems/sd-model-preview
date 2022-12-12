import json
import requests
from random import randint
import os.path
from pathlib import Path

import pathlib
import os
import modules.scripts as scripts
import gradio as gr

from modules.processing import Processed, process_images
from modules.shared import opts
from modules import script_callbacks, sd_models, shared

refresh_symbol = '\U0001f504'  # 🔄

def list_all_models():
    model_list = sd_models.checkpoint_tiles()
    #model_list = [token.split(' [',1)[0].split('\\')[-1] for token in model_list]
    #print(f"Model List:\n{model_list}")
#    if os.path.exists('models/Stable-diffusion'):
#        model_dict = {}
#        count = 1
#        for path in Path('models/Stable-diffusion').rglob('*.ckpt'):
#            value = path.name
#            model_dict[int(count)] = value
#            count += 1
#        return model_dict
    return model_list

def refresh_models():
    model_list = sd_models.checkpoint_tiles()
    refresh_ckpt = gr.Dropdown.update(label="Model", choices=list_all_models(), interactive=True, elem_id="quicksettings")
    return refresh_ckpt

def show_model_preview(modelname=None):
    modelname = modelname.split(' [',1)[0].split('\\')[-1]
    model_text_file = None
    model_jpg_file = None
    txt_update = None
    jpg_html_update = None
    search_name = modelname.replace(".ckpt",".txt")
    search_model = modelname.replace(".ckpt",".jpg")
    for txt_file in Path('extensions').rglob('*.txt'):
        if txt_file.name == modelname.replace(".ckpt",".txt"):
            if model_text_file is None:
                model_text_file = txt_file.name
                model_text_path = Path(txt_file)

    for txt_file in Path('models/Stable-diffusion').rglob('*.txt'):
        if txt_file.name == modelname.replace(".ckpt",".txt"):
            if model_text_file is None:
                model_text_file = txt_file.name
                model_text_path = Path(txt_file)

    if model_text_file is not None:
        with open(model_text_path, "r", encoding="utf8") as file:
            count = 1
            for line in file:
                output_text = f'{line.strip()}\n'
        txt_update = gr.Textbox.update(value=output_text)

    for jpg_file in Path('extensions').rglob('*.jpg'):
        if jpg_file.name == modelname.replace(".ckpt",".jpg"):
            if model_jpg_file is None:
                model_jpg_file = jpg_file.name
                model_jpg_path = Path(jpg_file)
    for jpg_file in Path('models/Stable-diffusion').rglob('*.jpg'):
        if jpg_file.name == modelname.replace(".ckpt",".jpg"):
            if model_jpg_file is None:
                model_jpg_file = jpg_file.name
                model_jpg_path = Path(jpg_file)

    if model_jpg_file is not None:
        model_jpg_nospace = str(model_jpg_path).replace(" ","%20")
        jpg_html_update = gr.HTML.update(value=f'<div align=center><img src=file/{model_jpg_nospace} width=1000px></img></div>')

    return txt_update, jpg_html_update



def on_ui_tabs():
    with gr.Blocks() as modelpreview_interface:
        with gr.Row():
            #model_dict_list = list_all_models()
            list_models = gr.Dropdown(label="Model", choices=list_all_models(), interactive=True, elem_id="quicksettings")
            #refresh_checkpoint = gr.Button(value=refresh_symbol, elem_id="refresh_sd_model_checkpoint")
            #list_models = gr.Dropdown(label="List Models", elem_id="list_models_id", choices=[v for k, v in model_dict_list.items()], value=next(iter(model_dict_list.keys())), interactive=True)
        with gr.Row():
            txt_list = ""
            dummy = gr.Textbox(label='Tags (if any)', value=f'{txt_list}', interactive=False, lines=1)
        with gr.Row():
            preview_image_html = gr.HTML()

        list_models.change(
            fn=show_model_preview,
            inputs=[
            list_models,
            ],
            outputs=[
            dummy,
            preview_image_html,
            ]
        )

#        refresh_checkpoint.click(
#            fn=refresh_models,
#            inputs=[],
#            outputs=[
#            list_models,
#            ]
#        )
        

    return (modelpreview_interface, "Model Previews", "modelpreview_interface"),

script_callbacks.on_ui_tabs(on_ui_tabs)