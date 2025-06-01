import face_recognition
import cv2
import os
import glob
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            return [], []

        # Encode faces detected in the frame
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Initialize list to store recognized face names
        face_names = []

        # Compare each face encoding in the frame with known face encodings
        for face_encoding in face_encodings:
            # Compare the face encoding with known face encodings
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Check if there's a match with any known face
            if True in matches:
                # Find the index of the first match
                match_index = matches.index(True)
                name = self.known_face_names[match_index]

            face_names.append(name)

        return face_locations, face_names


def main():
    # Initialize SimpleFacerec instance
    sfr = SimpleFacerec()

    # Load encoding images for face recognition
    sfr.load_encoding_images("images/")

    # Load camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        # Detect known faces in the captured frame
        face_locations, face_names = sfr.detect_known_faces(frame)

        # Display the captured frame with face recognition results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back the face locations if the frame was resized
            top *= sfr.frame_resizing
            right *= sfr.frame_resizing
            bottom *= sfr.frame_resizing
            left *= sfr.frame_resizing

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release camera and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
