
import numpy as np

# Create two 3x3 matrices
matrix1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

# Compare the two matrices and modify matrix1 accordingly
mask = matrix1 >= matrix2
matrix1[mask] = -20

print(matrix1)



##############################


import cv2
import numpy as np
from PIL import Image

watermark = cv2.imread('0_2_line.png', cv2.IMREAD_UNCHANGED)
image = cv2.imread('0.png', cv2.IMREAD_UNCHANGED) 
            
# print(watermark)                       
# matrix = np.array(watermark)

# image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

subtraction_value = 20

result = np.clip(watermark - subtraction_value, a_min=0, a_max=None)
result = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR,cv2.IMREAD_UNCHANGED)


result1 =np.add(result, image)
result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
# result1 = np.clip(image + result, a_min=0, a_max=None)
print(result1)

cv2.imwrite('aaaaa.png',result1)
