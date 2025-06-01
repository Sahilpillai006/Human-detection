import cv2
import os
import numpy as np
from simple_facerec import SimpleFacerec
import tkinter as tk
from tkinter import messagebox

url = 0  # Video source: 0 means default webcam. Can be replaced by a URL for IP camera or flask stream

# Load pre-trained MobileNet SSD model for human detection
def load_mobilenet_model():
    # Load Caffe model and prototxt defining network architecture
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')
    return net

# Detect and count people in a frame using MobileNet SSD
def detect_people(frame, net):
    # Resize frame to 300x300 for the MobileNet input
    frame_resized = cv2.resize(frame, (300, 300))
    # Create blob from image with scaling factor and mean subtraction
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    total_people = 0
    total_confidence = 0.0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # Class ID 15 corresponds to 'person' in COCO dataset for this model
        if confidence > 0.2 and int(detections[0, 0, i, 1]) == 15:
            total_people += 1
            total_confidence += confidence
            (h, w) = frame.shape[:2]
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # Draw bounding box around detected person
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Avoid division by zero
    average_confidence = total_confidence / max(1, total_people)
    return total_people, average_confidence

# Capture image from camera and save it for face recognition training
def capture_and_save_image():
    # Create directory if not exists
    if not os.path.exists("images"):
        os.makedirs("images")

    cap = cv2.VideoCapture(url)

    # Clear existing images in the folder to avoid confusion
    existing_images = os.listdir("images")
    for image_file in existing_images:
        os.remove(os.path.join("images", image_file))

    # Capture loop - press Enter to capture and save
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        try:
            # Optional: Flip frame if needed (commented out)
            # frame = cv2.flip(frame, 0)

            cv2.imshow("Camera Frame", frame)
            key = cv2.waitKey(1)
            if key == 13:  # Enter key pressed
                image_path = os.path.join("images", "Person_Found.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Image saved to {image_path}")
                cv2.destroyWindow("Camera Frame")
                break

        except Exception as e:
            print(f"Error capturing image: {e}")

    cap.release()

# Main face recognition routine
def recognize_faces():
    # Initialize face recognizer and load known encodings
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # Load human detection model for supplementary info
    net = load_mobilenet_model()

    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        try:
            # Optional frame flip if needed
            # frame = cv2.flip(frame, 0)

            # Detect people count and confidence in frame
            total_people, average_confidence = detect_people(frame, net)

            # Display counts on screen
            cv2.putText(frame, f'Total People: {total_people}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Average Confidence: {average_confidence:.2f}', (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Detect and recognize faces using SimpleFacerec
            face_locations, face_names = sfr.detect_known_faces(frame)

            # Draw bounding boxes and labels for recognized faces
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, top - 6), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('frame', frame)

            # Quit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Error processing frame: {e}")

    cap.release()
    cv2.destroyAllWindows()

# Simple human detection display only
def human_detection():
    net = load_mobilenet_model()
    cap = cv2.VideoCapture(url)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame from the camera.")
            break

        try:
            # Optional frame flip if needed
            # frame = cv2.flip(frame, 0)

            total_people, average_confidence = detect_people(frame, net)

            cv2.putText(frame, f'Total People: {total_people}', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Average Confidence: {average_confidence:.2f}', (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"Error processing frame: {e}")

    cap.release()
    cv2.destroyAllWindows()

# Prompt user with a GUI popup to decide whether to find someone
def prompt_user():
    root = tk.Tk()
    root.withdraw()  # Hide main tkinter window
    user_response = messagebox.askyesno("Find Someone", "Do you want to find someone?")
    return user_response

# Entry point
find_someone = prompt_user()

if find_someone:
    # Capture image and run face recognition
    capture_and_save_image()
    recognize_faces()
else:
    # Run human detection only
    human_detection()
