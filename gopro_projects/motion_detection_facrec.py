import cv2
import numpy as np
from time import time
import socket
from goprocam import GoProCamera
from goprocam import constants

import find_faces_in_picture
from find_faces_in_picture import faces_in_picture

import shutil
from os import listdir
import os

import webbrowser

def photo_face_find(gpCam):
    gpCam.downloadLastMedia(gpCam.take_photo(0))

    files = os.listdir()
    picture = ""

    for file in files:
        if (file.find("JPG") != -1):
            picture = file

    faces_in_picture(picture)
    shutil.move(picture, "faces/" + picture)


t=time()

gpCam = GoProCamera.GoPro()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
gpCam.livestream("start")

cap = cv2.VideoCapture("udp://10.5.5.9:8554")

ret1, frame1 = cap.read()
ret2, frame2 = cap.read()

i = 0
t_buff = time()

while True:
    ret1, frame1 = ret2, frame2
    ret2, frame2 = cap.read()

    if time() - t_buff > 3 and ret1 == True and ret2 == True:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            print (cv2.contourArea(contour))
            if cv2.contourArea(contour) < 800:
                continue
            print (i, "Motion Detected!", '\a')
            # webbrowser.open('https://www.youtube.com/watch?v=iuy-oOJCOoM&t=103s')
            i += 1
            photo_face_find(gpCam)
            t_buff = time()
            break;

    cv2.imshow("feed", frame1)

    if time() - t >= 2.5:
        sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
        t=time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()





