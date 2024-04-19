import cv2
import face_recognition
import numpy as np
import csv

# Load the static picture
static_image = face_recognition.load_image_file('received_frame.jpg')

# Initialize variables for the CSV file
csv_filename = "face_recognition_result.csv"
csv_header = ["Result"]
csv_data = []

# Load the Haar cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to detect faces in an image
def detect_faces(img):
    face_locations = face_recognition.face_locations(img)
    return face_locations

# Function to detect eyes in a face ROI
def detect_eyes(face_roi):
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_face, 1.1, 4)
    return len(eyes) > 0  # Returns True if eyes are detected, False otherwise

# Function to check liveness (dummy implementation)
def check_liveness(face_roi, static_image):
    # Dummy implementation: Compare the size of the detected face with the size of the static image
    live_size = face_roi.shape[0] * face_roi.shape[1]
    static_size = static_image.shape[0] * static_image.shape[1]
    similarity = live_size / static_size
    return similarity

# Function to write data to CSV file
def write_to_csv(data):
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to capture live video from the camera
def capture_video():
    # Open the video capture device
    video_capture = cv2.VideoCapture(0)
    
    # Variable to track the current result
    current_result = None
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        # Convert the frame from BGR color to RGB color
        rgb_frame = frame[:, :, ::-1]
        
        # Detect faces in the frame
        face_locations = detect_faces(rgb_frame)
        
        # Display the results
        for (top, right, bottom, left) in face_locations:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            # Simulate liveness check by comparing with the static image
            face_roi = frame[top:bottom, left:right]
            
            # Check if eyes are open
            if not detect_eyes(face_roi):
                result = "False (Eyes closed)"
            else:
                similarity = check_liveness(face_roi, static_image)
                if similarity > 0.2:  # Lower threshold for liveness check
                    result = "True"
                else:
                    result = "False"
            
            # Write result to CSV file if it changes
            if result != current_result:
                current_result = result
                write_to_csv([result])
        
        # Display the resulting image
        cv2.imshow('Face Biometric System', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

# Main function
if __name__ == "__main__":
    capture_video()
