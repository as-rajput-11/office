from PIL import Image


def combine_images(columns, space, images):
    rows = len(images) 
    if len(images) % columns:
        rows += 1
    width_max = max([Image.open(image).width for image in images])
    height_max = max([Image.open(image).height for image in images])
    background_width = width_max*columns
    background_height = height_max*rows
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 0))
    x = 0
    y = 0
    for i, image in enumerate(images):
        img = Image.open(image)
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        background.paste(img, (x+x_offset, y+y_offset))
        x += width_max 
        if (i+1) % columns == 0:
            y += height_max 
            x = 0
    background.save('image.png')


combine_images(columns=1, space=0, images=['/home/bisag/project work task_2023/logo replace/logo_replacement/ips_logo_guj/main-qimg_transparent.png','/home/bisag/project work task_2023/logo replace/logo_replacement/ips_logo_guj/2.jpg'])