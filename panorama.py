import cv2
import numpy as np
import os
import shutil
import imutils


# def rescale(img):
#     scale = 0.5;
#     h,w = img.shape[:2];
#     h = int(h*scale);
#     w = int(w*scale);
#     return cv2.resize(img, (w,h));


# folder = "frames/";
# if os.path.isdir(folder):
#     shutil.rmtree(folder);
# os.mkdir(folder);

# cap = cv2.VideoCapture("VID20230103171212.mp4"); 
# counter = 0;

# orb = cv2.ORB_create();
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False);


# _, last = cap.read();
# last = rescale(last);
# cv2.imwrite(folder + str(counter).zfill(5) + ".png", last);


# kp1, des1 = orb.detectAndCompute(last, None);


# cutoff = 50; 



# prev = None;
# while True:
 
#     ret, frame = cap.read();
#     if not ret:
#         break;

  
#     frame = rescale(frame);

  
#     kp2, des2 = orb.detectAndCompute(frame, None);

   
#     matches = bf.knnMatch(des1, des2, k=2);

   
#     good = []
#     for m,n in matches:
#         if m.distance < 0.5*n.distance:
#             good.append(m);

 
#     print(len(good));
#     if len(good) < cutoff:
      
#         counter += 1;
#         last = frame;
#         kp1 = kp2;
#         des1 = des2;
#         cv2.imwrite(folder + str(counter).zfill(5) + ".png", last);
#         print("New Frame: " + str(counter));


#     cv2.imshow("Frame", frame);
#     cv2.waitKey(1);
#     prev = frame;


# counter += 1;
# cv2.imwrite(folder + str(counter).zfill(5) + ".png", prev);


# print("Counter: " + str(counter));
##################################################################



# folder = "frames/";
# filenames = os.listdir(folder);
# images = [];
# for file in filenames:   
#     img = cv2.imread(folder + file);
#     images.append(img);
# stitcher = cv2.createStitcher();
# (status, stitched) = stitcher.stitch(images);
# cv2.imshow("Stitched", stitched);
# cv2.imwrite("t.jpg",stitched)
# cv2.waitKey(0);


###########################################################

protopath = "MobileNetSSD_deploy.prototxt"
modelpath = "MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


def main():
    image = cv2.imread('t.jpg')
    image = imutils.resize(image, width=600)

    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 0.007843, (W, H), 127.5)

    detector.setInput(blob)
    person_detections = detector.forward()

    for i in np.arange(0, person_detections.shape[2]):
        confidence = person_detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(person_detections[0, 0, i, 1])

            if CLASSES[idx] != "person":
                continue

            person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = person_box.astype("int")

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)

    cv2.imshow("Results", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()





********************************************************************************************************************
#####################################################################################################################
04/01/2023
######################################################################################################################
import cv2
import numpy as np
import os
import shutil
import imutils

import uuid
id = uuid.uuid4()



def rescale(img):
    scale = 0.5
    h,w = img.shape[:2]
    h = int(h*scale)
    w = int(w*scale)
    return cv2.resize(img, (w,h))


folder = "frames/"
if os.path.isdir(folder):
    shutil.rmtree(folder)
os.mkdir(folder)

cap = cv2.VideoCapture("video/3.mp4"); 
counter = 0

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)


_, last = cap.read()
last = rescale(last)
cv2.imwrite(folder + str(counter).zfill(5) + ".png", last)


kp1, des1 = orb.detectAndCompute(last, None)


cutoff = 50; 



prev = None
while True:
 
    ret, frame = cap.read()
    if not ret:
        break

  
    frame = rescale(frame)

  
    kp2, des2 = orb.detectAndCompute(frame, None)

   
    matches = bf.knnMatch(des1, des2, k=2)

   
    good = []
    for m,n in matches:
        if m.distance < 0.5*n.distance:
            good.append(m)

 
    print(len(good))
    if len(good) < cutoff:
      
        counter += 1
        last = frame
        kp1 = kp2
        des1 = des2
        cv2.imwrite(folder + str(counter).zfill(5) + ".png", last)
        print("New Frame: " + str(counter))


    # cv2.imshow("Frame", frame);
    # cv2.waitKey(1);
    prev = frame


counter += 1
cv2.imwrite(folder + str(counter).zfill(5) + ".png", prev)


print("Counter: " + str(counter))
##################################################################

folder = "frames/"
filenames = os.listdir(folder)
images = []

for file in filenames:   
    img = cv2.imread(folder + file)
    images.append(img)
stitcher = cv2.createStitcher()
(status, stitched) = stitcher.stitch(images)
# cv2.imshow("Stitched", stitched);
cv2.imwrite("stitched_img.jpg",stitched)
# cv2.waitKey(0);


###########################################################

protopath = "model/MobileNetSSD_deploy.prototxt"
modelpath = "model/MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]


def main():
    image = stitched
    # image = cv2.imread('o.jpg')
    image = imutils.resize(image, width=1900)

    (H, W) = image.shape[0:2]

    blob = cv2.dnn.blobFromImage(image, 0.007843, (W, H), 127.5)

    detector.setInput(blob)
    person_detections = detector.forward()

    for i in np.arange(0, person_detections.shape[2]):
        confidence = person_detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(person_detections[0, 0, i, 1])

            if CLASSES[idx] != "person":
                continue

            person_box = person_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
            (startX, startY, endX, endY) = person_box.astype("int")

            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imwrite("update image/"+str(id)+".jpg",image)

    cv2.imshow("Results", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()





