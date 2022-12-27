from augraphy import *
import cv2  

pipeline = default_augraphy_pipeline()
img = cv2.imread("./input/2.jpg")
data = pipeline.augment(img)
augmented = data["output"]
