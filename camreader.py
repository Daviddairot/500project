import cv2
import requests

# Function to capture video frames and send them to Django app
def stream_video():
    # OpenCV video capture from camera
    cap = cv2.VideoCapture(0)  # Change to the appropriate camera index if multiple cameras are available
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Encode frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        # Send frame to Django app
        url = 'http://localhost:8000/video_stream/'  # Replace with your Django app's URL
        files = {'frame': ('frame.jpg', frame_bytes)}
        response = requests.post(url, files=files)
        if response.status_code != 200:
            print('Error:', response.text)

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

# Start streaming video
stream_video()
