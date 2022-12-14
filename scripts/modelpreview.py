import os.path
from pathlib import Path

import pathlib
import os
import re
import glob

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

# Function to create HTML code for a given image file
def create_html_code(file):
    # Create the HTML code for the image
    space_replace = file.replace(" ","%20")
    html_code = f'<div align=center><img src=file/{file} width=1000px></img></div>'
    #html_code = '<img src="{}" alt="Image file: {}">'.format(file, file)
  
    # Return the HTML code
    return html_code

# Function to search for image files with a similar name to the input string
def search_and_display_images(input_str):
    txt_file = None
    # Create a regex pattern to match image files with a similar name to the input string
    pattern = re.compile(r'.*' + input_str + r'.*\.(png|jpg)')
    txt_pattern = re.compile(r'.*' + input_str + r'.*\.txt')
    # Get the current working directory
    #cwd = os.getcwd()
    cwd = Path('models/Stable-diffusion')
  
    # Initialize a list to store the HTML code for all the images
    html_code_list = []
  
    # Search for PNG and JPG files with a similar name to the input string in the current directory and its subdirectories
    for file in glob.glob(os.path.join(cwd, '**'), recursive=True):
        # Check if the file is a PNG or JPG file with a similar name to the input string
        if pattern.match(file):
            # If so, create the HTML code for the image
            html_code = create_html_code(file)

            # Append the HTML code to the list
            html_code_list.append(html_code)
        if txt_pattern.match(file):
            txt_file = file
    # Return the list of HTML code
    return html_code_list, txt_file


def refresh_models():
    model_list = sd_models.checkpoint_tiles()
    refresh_ckpt = gr.Dropdown.update(label="Model", choices=list_all_models(), interactive=True, elem_id="quicksettings")
    return refresh_ckpt

def show_model_preview(modelname=None):
    modelname = modelname.split(' [',1)[0].split('\\')[-1].replace(".ckpt","").replace(".safetensor","")

    model_text_file = None
    model_jpg_file = None
    txt_update = None
    jpg_html_update = None

#    for txt_file in Path('models/Stable-diffusion').rglob('*.txt'):
#        if txt_file.name == f'{modelname}.txt':
#            if model_text_file is None:
#                model_text_file = txt_file.name
#                model_text_path = Path(txt_file)

#    if model_text_file is not None:
#        with open(model_text_path, "r", encoding="utf8") as file:
#            output_text = ""
#            for line in file:
#                output_text = f'{output_text}{line.strip()}\n'
#        txt_update = gr.Textbox.update(value=output_text)
    html_code_list = []
    found_txt_file = None
    html_code_list, found_txt_file = search_and_display_images(modelname)
    if found_txt_file:
        with open(found_txt_file, "r", encoding="utf8") as file:
                output_text = ""
                for line in file:
                    output_text = f'{output_text}{line.strip()}\n'
        txt_update = gr.Textbox.update(value=output_text)
    image_preview_html = '<br>'.join(html_code_list)
    if html_code_list:
        jpg_html_update = gr.HTML.update(value=image_preview_html)
#    for jpg_file in Path('extensions').rglob('*.jpg'):
#        if jpg_file.name == modelname.replace(".ckpt",".jpg"):
#            if model_jpg_file is None:
#                model_jpg_file = jpg_file.name
#                model_jpg_path = Path(jpg_file)
#    for jpg_file in Path('models/Stable-diffusion').rglob('*.jpg'):
#        if jpg_file.name == modelname.replace(".ckpt",".jpg"):
#            if model_jpg_file is None:
#                model_jpg_file = jpg_file.name
#                model_jpg_path = Path(jpg_file)

#    if model_jpg_file is not None:
#        model_jpg_nospace = str(model_jpg_path).replace(" ","%20")
#        jpg_html_update = gr.HTML.update(value=f'<div align=center><img src=file/{model_jpg_nospace} width=1000px></img></div>')

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