# Drone-Based Human Detection and Face Recognition System

## 🚁 Overview

This project implements a human detection and face recognition system designed for drone deployment in post-disaster scenarios. The system uses a pre-trained MobileNet SSD model to detect and count people in real-time video feeds. It can also recognize known faces if needed, enabling efficient identification and tracking of individuals in disaster-stricken areas.

--------------------------------------------------

## 🔍 Features

- **Human Detection:** Real-time detection and counting of people using MobileNet SSD.
- **Face Recognition:** Optional image capture and face recognition using a face recognition library.
- **Live Video Feed:** Works with both USB webcam and IP camera feeds.
- **Web-Based Streaming (Optional):** Stream camera feed over the network using a Flask server.
- **User Prompt:** GUI option to switch between detection-only and face recognition modes.

--------------------------------------------------

## ⚙️ How It Works

1. The drone captures a live video stream.
2. The MobileNet SSD model detects humans in each frame and highlights them with bounding boxes.
3. If enabled, the system captures an image and performs face recognition on known faces.
4. Detection count and confidence scores are displayed in the video feed for situational awareness.
5. Optionally, stream the video feed using a browser via Flask.

--------------------------------------------------

## 🧰 Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Tkinter (for GUI prompts)
- [simple_facerec](https://github.com/ageitgey/face_recognition) or similar library
- Flask (for optional live video streaming)
- `picamera2` (if using Raspberry Pi camera)
- Pre-trained MobileNet SSD model files:
  - `deploy.prototxt`
  - `mobilenet_iter_73000.caffemodel`

--------------------------------------------------

## 📦 Setup

1. Clone this repository.
2. Download and place the MobileNet SSD model files in the project directory:
   - [`deploy.prototxt`](https://github.com/chuanqi305/MobileNet-SSD/blob/master/deploy.prototxt)
   - [`mobilenet_iter_73000.caffemodel`](https://github.com/chuanqi305/MobileNet-SSD/blob/master/mobilenet_iter_73000.caffemodel)
3. Install dependencies:

   ```bash
   pip install opencv-python numpy flask picamera2

> Note: If using face recognition, also install that separately:

```bash
pip install face_recognition
```

--------------------------------------------------

## 🚀 Usage (Desktop/Drone Mode)

Run the main detection script:

```bash
python drone_human_detection.py
```

* When prompted, select **Yes** to enable face recognition.
* Press **Enter** to capture an image of the face for encoding.
* Press **q** to quit the application.

--------------------------------------------------

## 🌐 Optional: Live Feed via Flask Web Server

If you want to stream the detection feed over the network (e.g., for drone operator visibility or remote monitoring):

1. Use the `video.py` Flask server script.

2. Start the server:

   ```bash
   python video.py
   ```

3. Open a browser and go to:

   ```
   http://<your-device-ip>:5000
   ```

> ✅ The Flask app supports both USB webcam (`cv2.VideoCapture`) and Raspberry Pi Camera via `picamera2`.

Make sure:

* Camera is properly connected
* Required permissions are granted
* You are on the same network as the device

---

## 📁 Folder Structure

```
project/
│
├── video.py                  # Flask server for live video stream
├── drone_human_detection.py # Main detection and recognition script
├── deploy.prototxt
├── mobilenet_iter_73000.caffemodel
├── templates/
│   └── video.html            # HTML page for live stream
├── images/                   # Known faces for recognition
└── README.md
```

--------------------------------------------------

## 📌 Notes

* The system assumes class ID `15` corresponds to "person" in the MobileNet SSD model.
* Default detection confidence threshold is `0.2` — you can tweak this as needed.
* Ensure the `images/` folder has known face images for recognition. Otherwise, it will ask to capture a new one during runtime.
* Flask-based streaming is ideal for headless setups or when physical display is inaccessible.

---

## 🔮 Future Improvements

* Integration with drone flight control systems (e.g., MAVLink).
* Add support for multi-object detection (e.g., fire, injured, animals).
* Onboard processing optimizations for low-power edge devices.
* Secure streaming with authentication.

--------------------------------------------------

## 🧑‍💻 Author

# Sahil
Engineer | Robotics & AI Enthusiast
--------------------------------------------------

