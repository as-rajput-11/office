import cv2
import imutils
from numpy import empty
import pytesseract
from PIL import Image, ImageEnhance
import uuid
import os

def createList(r1, r2):
    return list(range(r1, r2+1))
      
# Driver Code
r1, r2 = 1, 63
list = createList(r1, r2)

for j in list:
    try:
        # imsave =  Image.open('images/'+str(i)+'.jpg')
        image = cv2.imread('FinalImag/'+str(j)+'.jpg')
        image = imutils.resize(image, width=300 )
        cv2.imshow("original image", image)
        #cv2.waitKey(0)

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("greyed image", gray_image)
        #cv2.waitKey(0)

        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17) 
        cv2.imshow("smoothened image", gray_image)
        #cv2.waitKey(0)


        edged = cv2.Canny(gray_image, 30, 200) 
        cv2.imshow("edged image", edged)
        #cv2.waitKey(0)


        cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image1=image.copy()
        cv2.drawContours(image1,cnts,-1,(0,255,0),3)
        cv2.imshow("contours",image1)
        #cv2.waitKey(0)


        cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
        screenCnt = None
        image2 = image.copy()
        cv2.drawContours(image2,cnts,-1,(0,255,0),3)
        cv2.imshow("Top 30 contours",image2)
        # cv2.waitKey(0)


        i=7
        for c in cnts:
                perimeter = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
                if len(approx) == 4: 
                        screenCnt = approx
                        
                x,y,w,h = cv2.boundingRect(c) 
                new_img=image[y:y+h,x:x+w]
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break
        # print(type(screenCnt))

        cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
        cv2.imshow("image with detected license plate", image)
        # cv2.waitKey(0)

        Cropped_loc = './7.png'
        cv2.imshow("cropped", cv2.imread(Cropped_loc))
        plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
        print("Number plate is:", plate)
        cu = 0
        Delete = ['oOo\nOS\nSoo\n=o\nKo\n\x0c', '2083665\n\n \n\x0c', ' \n\x0c',  ' \n\x0c', ' \n\x0c', ' \n\x0c','\x0c', '\x0c',   '\x0c', '\x0c', '\x0c', 'ET\nKL.o1cc 50\n\x0c',  '\x0c', ' \n\n \n\x0c', '\x0c',  '\x0c', ' \n\x0c', ' \n\x0c',' \n\n \n\x0c', ' \n\x0c',  '\x0c',  ' \n\x0c',  ' \n\x0c', ' \n\x0c', '\x0c', ' \n\x0c','MONON]\n\x0c', '\x0c']
        for k in Delete:
            # print('+++++++++++++++---------------++++++++++++++++')
            if plate == k and cu == 0:
                os.remove('FinalImag/'+str(j)+'.jpg')
                # os.remove('crop_img_ocr/'+str(i)+'.jpg')
                print('+++++++++++++++++Deleted++++++++++++++++++++')
                cu = 1
                # imsave =  Image.open('FinalImag/'+str(i)+'.jpg')
            
        # cv2.waitKey(0)
        # imsave.save('FinalImag/'+str(uuid.uuid4())+'.jpg')
        
        cv2.destroyAllWindows()
    
    
    except:
        try:
            os.remove('FinalImag/'+str(j)+'.jpg')
        except:
            print('------------skip---------------')


