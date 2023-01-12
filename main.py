import time
import cv2
from PIL import ImageGrab
import numpy as np
from pynput.mouse import Button, Controller
import threading

def intervalFunc():
    global COUNT, LAST_DETECTED

    img = ImageGrab.grab(bbox=(610, 300, 610 + 565, 300 + 200))

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)
    img = cv2.inRange(img, (7, 100, 100), (11, 255, 255))

    detected_circles = cv2.HoughCircles(img,
                                        cv2.HOUGH_GRADIENT, 1.4, 2000, param1=25,
                                        param2=15, minRadius=40, maxRadius=48)

    if detected_circles is not None and COUNT > LAST_DETECTED + 1: # Wait for at least 2 threads before moving away. This prevents the hoop from knocking the ball away instead of catching it
        LAST_DETECTED = COUNT
        point = detected_circles[0][0][0]
        mouse.position = (645 + point, 1000) # 645 is the left edge of the game window

    elif COUNT > LAST_DETECTED + 7: # if nothing is detected for 8 threads, then move the hoop back to the center
        mouse.position = (927, 1000)

mouse = Controller()
wait = time.sleep

wait(2)
mouse.position = (890, 650)  # click play button
wait(0.5)
mouse.press(Button.left)
mouse.release(Button.left)
wait(0.5)

mouse.position = (886, 1000)
wait(0.5)
mouse.press(Button.left) # click to start game

COUNT = 0
LAST_DETECTED = 0

while True:
    t = threading.Thread(target=intervalFunc)
    t.start()
    wait(0.1)
    COUNT += 1
