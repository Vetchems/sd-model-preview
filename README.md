# sd-model-preview
Extension for Automatic1111 Stable Diffusion WebUI to display tags from a text file and a jpg preview for custom models.

## About
A lot of new models and dreambooth finetunes are appearing and its becoming harder to keep track of what models output what styles and what tags are used to call these styles.
This extension allows you to create a txt file and jpg/png's with the same name as your model and have this info easily displayed for later reference in webui.

## Installation
1. From the extensions tab in web ui click install from url
2. Paste `https://github.com/Vetchems/sd-model-preview` into the url box.
3. Click Install
4. from the Installed tab click apply and restart.
5. Put txt and img files in the  `models\Stable-diffusion` with the same name as your model. (model.ckpt, model.txt, model,jpg). You may append something after the name to enable multiple preview images (model_portrait.jpg, model_nsfw.png). Subfolders may be used.

## Usage
1. After creating the txt files and images select the Model Preview tab in web ui
2. Select a model from the dropdown list. (if the model has the txt and img files they will be shown)

![screenshot](https://github.com/Vetchems/sd-model-preview/raw/main/sd-model-preview.png)
