# Import necessary libraries
from flask import Flask, Response, render_template
from picamera2 import Picamera2
import cv2

# Create a Flask app instance
app = Flask(__name__)

# Initialize PiCamera2
camera = Picamera2()

# Configure camera for preview with specific resolution and color format
camera.configure(camera.create_preview_configuration(
    main={"format": 'XRGB8888', "size": (640, 480)}
))

# Start the camera
camera.start()

# Function to generate video frames continuously
def gen_frames():
    while True:
        # Capture a frame from the camera as a NumPy array
        frame = camera.capture_array()

        # Rotate the frame 180 degrees (adjust angle if needed)
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Encode frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpeg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format with proper MIME type headers
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the main page — renders the video HTML template
@app.route('/')
def index():
    return render_template('video.html')  # Ensure this file is in the 'templates/' folder

# Route that provides the video feed to the frontend via MJPEG streaming
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Entry point — runs the app on all network interfaces, port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
