from PIL import Image
from os.path import join as pjoin, exists
from os import mkdir

def convert(input_image_path: str, output_image_folder: str, filename: str="background.png"):
    with Image.open(input_image_path) as image:
        if not exists(output_image_folder):
            mkdir(output_image_folder)
        image.save(pjoin(output_image_folder, filename), "PNG")

