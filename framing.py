import cv2
import pickle

# Width and Height of Box
width, height = 107, 48

# if not marked the slot
try:
    with open('ParkingPosition', 'rb') as slot:
        positionLists = pickle.load(slot)
except:
    # if already marked the slot
    positionLists = []


# function to mark OR unmark
def mouseClick(events, x, y, flags, parameters):
    if events == cv2.EVENT_LBUTTONDOWN: # left click to unmark the slot
        positionLists.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:    # right click to mark the slot
        for i, pos in enumerate(positionLists):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positionLists.pop(i)

    with open('ParkingPosition', 'wb') as slot:
        pickle.dump(positionLists, slot)

# function  to mark the slot
while True:
    img = cv2.imread('FrameImage.png')
    for pos in positionLists:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)



