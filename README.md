# Human-detection
Human Detection with face recognition can be used in drones also
# Drone-Based Human Detection and Face Recognition System

## Overview
This project implements a human detection and face recognition system designed for drone deployment in post-disaster scenarios. The system uses a pre-trained MobileNet SSD model to detect and count people in real-time video feeds. It can also recognize known faces if needed, enabling efficient identification and tracking of individuals in disaster-stricken areas.

## Features
- **Human Detection:** Real-time detection and counting of people using MobileNet SSD.
- **Face Recognition:** Optionally capture and recognize faces from the video feed using a simple face recognition library.
- **Live Video Feed:** Works with webcam or any IP camera URL input.
- **User Interaction:** GUI prompt for switching between detection-only and face recognition modes.

## How It Works
1. The drone captures a live video stream.
2. The MobileNet SSD model detects humans in each frame, highlighting them with bounding boxes.
3. If the operator chooses, the system captures an image for face recognition and identifies known individuals.
4. Counts and confidence scores are displayed on the video feed for situational awareness.

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- NumPy
- [simple_facerec](https://github.com/ageitgey/face_recognition) or equivalent face recognition library
- Tkinter (for user prompts)
- Pre-trained MobileNet SSD model files: `deploy.prototxt` and `mobilenet_iter_73000.caffemodel`

## Setup
1. Clone this repository.
2. Place the MobileNet SSD model files (`deploy.prototxt`, `mobilenet_iter_73000.caffemodel`) in the project directory.
3. Install required Python packages:
   
   pip install opencv-python numpy simple_facerec

4. Ensure you have a camera or replace `url` variable with your IP camera feed URL.

## Usage

Run the main script:

```bash
python drone_human_detection.py
```

* When prompted, select **Yes** to perform face recognition.
* Press **Enter** to capture an image for face encoding.
* Press **q** to quit the application.

## Notes

* The code assumes class ID 15 corresponds to people in the MobileNet SSD model.
* Confidence threshold is set to 0.2 by default; adjust for your environment.
* Ensure the "images" folder contains known faces for recognition or it will capture a new one on demand.

## Future Improvements

* Integration with drone flight control APIs for autonomous operation.
* Adding multi-class detection for other objects of interest.
* Optimize for edge devices with limited processing power.

---

### Author

Created for a post-disaster drone project to locate and recognize people in hazardous environments.


