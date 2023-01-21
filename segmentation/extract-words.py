import cv2
import os
import numpy as np

if not os.path.exists("words"):
    os.makedirs("words")

# Read image
img = cv2.imread('B2.jpg')
img = cv2.GaussianBlur(img, (15, 15), 2)
    # 5,5 gave 84 words, at 3
    # 7,7 gave 66 words, at 3
# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#cv2.imwrite('thresh.jpg', thresh)

# Inverse the image
img_bin = 255-thresh
#cv2.imwrite('img_bin.jpg',img_bin)

# Define kernel length


kernel_length = np.array(img).shape[1]//600 #<<<<<<<<<<<<<<<<<<<<<<<<< tweaks needed here
print(kernel_length, ' kernel_length')

# Define verticle kernel
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))

# Apply morphological operations
img_temp1 = cv2.erode(img_bin, ver_kernel, iterations=1)
cv2.imwrite('eroded.jpg',img_temp1)
img_temp2 = cv2.dilate(img_temp1, ver_kernel, iterations=3)
cv2.imwrite('dilated.jpg',img_temp2)

# Find contours
contours, hierarchy = cv2.findContours(img_temp2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Define the kernel for horizontal dilation and erosion
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))


# Extract words and save as separate images
for idx, cnt in enumerate(contours):
    x, y, w, h = cv2.boundingRect(cnt)
    roi = img[y:y+h, x:x+w]
    # Create the file path for the word image
    file_path = os.path.join("words", "word"+str(idx)+".png")
    # Save the word image
    cv2.imwrite(file_path, roi)


print(idx+1, ' images extracted')
