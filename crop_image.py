
from PIL import Image
import glob
import os 
from natsort import natsorted
 
im = Image.open('2.jpg')
 
width, height = im.size
# overlap = int(width/100*10)
img_part_wid = 400
overlap = int(img_part_wid/100*10)

wid = img_part_wid


r = 1
while width >= img_part_wid:
    img_part_wid = img_part_wid + wid
    r = r + 1 
    

left = 0
top = 0
right = wid
bottom = height

for i in range(r): 
    im1 = im.crop((left, top, right, bottom))
    im1.save('test11/'+str(i)+'.png')
    if width >= right:
        right = right + wid
        left = left + wid
    else:
        crop_im_l = right
        right = width
        
       


files = glob.glob("test11/*",recursive=True)
# print(files)

a = natsorted(files)

# print(a)

for i in a:
    
    try:
        image1 = Image.open("test12/output.png")
        image2 = Image.open(i)

        pos1 = image1.width
        pos2 = image2.width
        height = image1.height
        if i == a[-1]:
            last_w = crop_im_l - width
            
            image2 = Image.open(i)

            width, height = image2.size
            im1 = image2.crop((0, 0, width-last_w, height))
            im1.save(i)
            
            image2 = Image.open(i)
            pos2 = image2.width
            img3 = Image.new("RGB", (pos1+pos2-overlap, height), "white")
        else:
            img3 = Image.new("RGB", (pos1+pos2-overlap, height), "white")

        img3.paste(image1, (0, 0))
        img3.paste(image2, (pos1-overlap, 0))

        img3.save("test12/output.png","PNG")
    except:
        image1 = Image.open(i)
        
        pos1 = image1.width
        img3 = Image.new("RGB", (pos1, height), "white")
        
        img3.paste(image1, (0, 0))
        img3.save("test12/output.png","PNG")
        
