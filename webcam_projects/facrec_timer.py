import face_recognition
import cv2
import numpy as np
import time


video_capture = cv2.VideoCapture(0)

liam_image = face_recognition.load_image_file("known_images/liam.jpg")
liam_face_encoding = face_recognition.face_encodings(liam_image)[0]

kalindi_image = face_recognition.load_image_file("known_images/kalindi.jpg")
kalindi_face_encoding = face_recognition.face_encodings(kalindi_image)[0]

known_face_encodings = [
    # liam_face_encoding,
    # kalindi_face_encoding
]
known_face_names = [
    # "Barack Obama",
    # "Kalindi"
]

funny_names = [
    "Mr305",
    "Snoop",
    "Barack Obama",
    "Elvis",
    "Jacinda"
]

face_locations = []
face_encodings = []
face_names = []
all_face_names = {}
process_this_frame = True

log_dict = {}
time_log = []
del_index = []
name_id = 0

f = open("timelog.txt","w")
f = open("timelog.txt","a+")

while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # Else we create a new ID
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            else:
                known_face_encodings.append(face_encoding)
                try:
                    known_face_names.append(funny_names[name_id])
                    name = funny_names[name_id]
                except:
                    known_face_names.append("person " + str(name_id))
                    name = "person " + str(name_id)
                name_id += 1


            face_names.append(name)
            all_face_names[name] = 1

            if not name in log_dict:
                print (name, "Timer Started")
                log_dict[name] = {}
                log_dict[name]["name"] = name
                log_dict[name]["start"] = time.time()


        # Smarter way to delete?
        del_index = []

        for x in all_face_names:
            if not x in face_names:
                if not "end" in log_dict[x]:
                    log_dict[x]["end"] = time.time()
                    del_index.append(x)

        for x in del_index:
            f.write(str(log_dict[x]) + "\n")
            print (x, "Timer Finished")
            print ("finished", log_dict[x])
            time_log.append(log_dict[x])
            del all_face_names[x]
            del log_dict[x]

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


key_dict = {}
print ("time log = ", time_log)
for row in time_log:
    if not row["name"] in key_dict:
        key_dict[row["name"]] = 0
    key_dict[row["name"]] += row["end"] - row["start"]

print (key_dict)


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


# def main:
#     initalise variables
#     train model on existing images
#     Start program:
#         Find faces in frame
#         Compare faces to those trained
#         Add new faces to train
#         save new faces
#         return log of times, 
#     print a graph

