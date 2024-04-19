import serial
import csv
import requests
import time
import cv2
import face_recognition

CSV_FILE = 'button_status.csv'  # Path to the CSV file
ARDUINO_PORT = '/dev/ttyACM0'     # Arduino serial port
face_file = 'face_recognition_result.csv'

def read_serial_data_and_send_to_django():
    with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(line)
                    send_to_django(line)
            except UnicodeDecodeError:
                print("Error decoding line with UTF-8 encoding")
                try:
                    line = ser.readline().decode('ascii').strip()
                    if line:
                        print(line)
                        send_to_django(line)
                except UnicodeDecodeError:
                    print("Error decoding line with ASCII encoding")
                    try:
                        line = ser.readline().decode('latin1').strip()
                        if line:
                            print(line)
                            send_to_django(line)
                    except UnicodeDecodeError:
                        print("Error decoding line with Latin-1 encoding")
                        try:
                            line = ser.readline().decode('iso-8859-1').strip()
                            if line:
                                print(line)
                                send_to_django(line)
                        except UnicodeDecodeError:
                            print("Error decoding line with ISO-8859-1 encoding")
                            continue

def send_to_django(data):
    url = 'http://localhost:8000/serial_data/'  # Adjust the URL to your Django server endpoint
    payload = {'data': data}  # Assuming the data received from Arduino is sent as 'data'
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Data sent to Django successfully")
        else:
            print(data)
            print("Failed to send data to Django")
    except Exception as e:
        print("Error:", e)
    #read
    with open(CSV_FILE, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] == 'true':
                send_command_to_arduino()
    
    with open(face_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] == 'True':
                unlock()

def send_command_to_arduino():
    with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
        command = b'hello\n'  # Adjust the command as needed
        print(command)
        ser.write(command)
        print("Command sent to Arduino:", command)

def unlock():
    with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
        print("Unlocking...")
        command = b'unlock\n'  # Adjust the command as needed
        print(command)
        ser.write(command)
        print("Command sent to Arduino:", command)

if __name__ == "__main__":
    read_serial_data_and_send_to_django()