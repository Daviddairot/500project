import csv
import cv2
import json
import serial
from .models import ArduinoData
from django.shortcuts import render
import os
from django.conf import settings
import base64
from django.http import HttpResponse, JsonResponse
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
import subprocess
from django.core.management.base import BaseCommand


def home(request):
    return render(request, 'home.html')

@csrf_exempt
def index(request):
    return render(request, 'index.html')

@gzip.gzip_page
def video_feed(request):
    # Open camera
    cap = cv2.VideoCapture(0)

    def frame_generator():
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break
            # Convert frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                break
            # Yield the JPEG frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')




CSV_FILE = 'arduino_data.csv'

@csrf_exempt
def serial_data(request):
    if request.method == 'POST':
        try:
            # Extract data from the POST request
            data = request.POST.get('data')  # Assuming the data is sent as 'data'

            # Prepare the data for 10 rows
            rows = [[data] for _ in range(10)]

            # Append data to the CSV file for 10 rows
            with open(CSV_FILE, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)  # Write the prepared data to the CSV file

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    

@csrf_exempt
def csv_data(request):
    if request.method == 'GET':
        try:
            # Read data from CSV file
            data = None
            with open(CSV_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)[-1:]  # Read the last 10 rows from the CSV file

            return JsonResponse({'status': 'success', 'data': data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)



@csrf_exempt
def send_command(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        try:
            with open('button_status.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([data])
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def ad_in(request):
    if request.method == 'GET':
        # Open the serial port (adjust the port and baudrate as needed)
        with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as ser:
            # Read data from the serial port
            data_from_arduino = ser.readline().decode().strip()
            print(data_from_arduino)

            # Parse the data as JSON
            try:
                data = json.loads(data_from_arduino)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Failed to parse JSON data from Arduino'}, status=400)

            # Extract food level from the data
            food_level = data.get('foodLevel')

            # Create an instance of the ArduinoData model and save the food level
            arduino_data = ArduinoData.objects.create(food_level=food_level)
            print(arduino_data)

            # Optionally, return a JSON response to acknowledge successful data saving
            return JsonResponse({'message': 'Food level saved successfully'})
    else:
        # Return an error response for other HTTP methods
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)


def video_feed(request):

    return render(request, 'video_feed.html')