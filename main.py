from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
colorR = 139, 139, 139
detector = HandDetector(detectionCon=0.8)

cx, cy, width, height = 100, 100, 200, 200


class DragRectangle():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        width, height = self.size

        # if finger in rectangle area
        if cx - width // 2 < cursor[0] < cx + width // 2 and \
                cy - height // 2 < cursor[1] < cy + height // 2:
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRectangle([x*250+150, 150]))

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:

        length, _, _ = detector.findDistance(8, 12, img)
        if length < 40:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)


        ## Draw
        for rect in rectList:
            cx, cy = rect.posCenter
            width, height = rect.size
            cv2.rectangle(img, (cx - width // 2, cy - height // 2),
                          (cx + width // 2, cy + height // 2), colorR, cv2.FILLED)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
