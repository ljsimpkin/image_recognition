from PIL import Image
import face_recognition
import cv2

def faces_in_picture(picture):
	# Load the jpg file into a numpy array
	image = face_recognition.load_image_file(picture)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
	rgb_small_frame = small_image[:, :, ::-1]

	# face_locations = face_recognition.face_locations(image)
	face_locations = face_recognition.face_locations(rgb_small_frame)

	number_of_faces = len(face_locations)

	print("{} face(s) in this photograph.".format(number_of_faces))

	# for face_location in face_locations:

	#     # Print the location of each face in this image
	#     top, right, bottom, left = face_location
	#     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

	#     # You can access the actual face itself like this:
	#     face_image = image[top:bottom, left:right]
	#     pil_image = Image.fromarray(face_image)
	#     pil_image.show()

	return (False if number_of_faces == 0 else True)