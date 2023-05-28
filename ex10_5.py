import cv2
import numpy as np
import copy
import RPi.GPIO as GPIO
def main():
    BT1 = 21
    BT2 = 26
    # Mo camera
    cap = cv2.VideoCapture(0)
    print("Capture is ok")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    isdraw = False
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("Press BT1")
            while True:
                ret, src = cap.read()
                frame = copy.copy(src)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, (35, 89, 107), (45, 241, 213))
                # Tim contour
                _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                result = cv2.bitwise_or(frame, frame, mask=mask)
                if GPIO.input(BT2) == GPIO.LOW:
                    isdraw = True
                if isdraw:
                    draw(contours, result)
                cv2.imshow("Camera", src)
                cv2.imshow("Threshold", result)          
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    GPIO.cleanup()
                    cv2.destroyAllWindows()
                    break
def nothing(X):
    pass
def draw(contours, frame):
    if contours is None:
        print("No have contours. Please try to again")
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 300:
            hull = cv2.convexHull(contours[i])
            cv2.drawContours(frame, [hull], -1, (0, 255, 0))
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()