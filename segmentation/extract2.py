import cv2
import numpy as np
import os

answer = 'answers2'

def addImg(img,savePath,t):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape[:2]
    kernel = np.ones((13,13),np.uint8)

    e = cv2.erode(img,kernel,iterations = 2)  
    d = cv2.dilate(e,kernel,iterations = 1)
    ret, th = cv2.threshold(d, 150, 255, cv2.THRESH_BINARY_INV)

    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(th, mask, (200,200), 255); # position = (200,200)
    out = cv2.bitwise_not(th)
    out= cv2.dilate(out,kernel,iterations = 3)

        # Fill rectangular contours
    cnts = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(out, [c], -1, (255,255,255), -1)

    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
    opening = cv2.morphologyEx(out, cv2.MORPH_OPEN, kernel, iterations=4)

    # Draw rectangles

    i=0

    if t=='A':
        i=4
    elif t=='B':
        i=6 


    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w>1000:

            crop = img[y-10:y+h-5,x:x+w]
            os.makedirs('extracted/'+savePath,exist_ok=True)

            cv2.imwrite('extracted/'+savePath+'/'+t+str(i)+'.jpg',crop)
            i=i-1





fileDict = {}

for f in os.listdir(answer):
    
    vals = f.split('.')
    sno = vals[0][-1]
    indx = vals[0][:-1]

    fileDict[indx]={}

for f in os.listdir(answer):
    
    # print(f)
    vals = f.split('.')
    sno = vals[0][-1]
    indx = vals[0][:-1]

    path = os.path.join(answer,f)
    print(path)
    currImg = cv2.imread(path)
    fileDict[indx][sno]=currImg


for key,val in fileDict.items():

 
    for k,img in val.items():
        addImg(img,key,k)

    # crop = image[y-10:y+h-5,x:x+w]
    # os.makedirs('extracted/'+savePath,exist_ok=True)

    # cv2.imwrite('extracted/'+savePath+'/'+t+str(i)+'.jpg',crop)
    # i=i-1