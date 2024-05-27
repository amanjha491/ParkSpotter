import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('CarParkVideo.mp4')

#Storing Boxes Dimension
with open('ParkingPosition', 'rb') as f:
    posList = pickle.load(f)

# Width and Height of Box
width, height = 107, 48

# Function of Find Parking Space Count
def checkParkingSpace(imgPro):

    #Space Count Variable Inisilize With 0
    spaceCounter = 0

    #Traverse through all Slots
    for pos in posList:
        x, y = pos      # position of x and y axis
        imgCrop = imgPro[y:y + height, x:x + width]     #cropping the slots
        count = cv2.countNonZero(imgCrop)        #counting Non zero value of binary image


        if count < 900:   # threshold value is 900 (empty)
            color = (0, 255, 0)
            thickness = 2
            spaceCounter += 1
        else:       # occupied
            color = (0, 0, 255)
            thickness = 2

            #framing
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=1, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free Slots : {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=2, offset=20, colorR=(0,200,0))

# Traverse through frames of Video
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Image processing of each frame of video
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Function call and Display for each frame of Video 
    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)

    cv2.waitKey(10)