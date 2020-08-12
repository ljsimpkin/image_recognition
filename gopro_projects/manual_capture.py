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

while True:
    ret, frame = cap.read()

    if ret == True:
        if cv2.waitKey(1) & 0xFF == ord('f'):
            photo_face_find(gpCam)

    cv2.imshow("feed", frame)

    if time() - t >= 2.5:
        sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
        t=time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()





