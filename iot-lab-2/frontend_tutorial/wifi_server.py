import configparser
import socket
import time
import json
from picarx import Picarx
from time import sleep

config = configparser.ConfigParser()
config.read('config.ini')
HOST = config.get('Raspberry Pi', 'ip_address') # IP address of your Raspberry PI
PORT = 65431          # Port to listen on (non-privileged ports are > 1023)
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)     
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket for interactive")
        client.close()
        s.close()    
"""


def read_cpu_temperature():
    # Read the CPU temperature
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = float(f.read()) / 1000  # Convert from millidegrees to degrees Celsius
    return temp


def encode_data(temperature):
    data = {'temperature': temperature,'car_direction': "None", 'speed':0, 'distance_travel': 0}
    return json.dumps(data)

def handle_arrows(conn):
    px = Picarx()
    data = conn.recv(1024).decode()    # receive 1024 Bytes of message in binary format
    if data:
        print(data)
        if (data == "forward\r\n"):
            px.set_dir_servo_angle(0)
            px.forward(80)
            # px.set_cam_tilt_angle(60)
        elif (data == "left\r\n"):
            #px.set_cam_tilt_angle(60)
            px.set_dir_servo_angle(-30)
            px.forward(80)
        elif (data == "right\r\n"):
            px.set_dir_servo_angle(30)
            px.forward(80)
        else:
            px.set_dir_servo_angle(0)
            px.backward(80)

        sleep(0.5)
        px.forward(0)
        # conn.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print('start')

    try:
        while True:
            conn, addr = s.accept()
            print("connected by: ", addr)
        
            handle_arrows(conn)
            temperature = read_cpu_temperature()

            data = encode_data(temperature)

            conn.sendall(data.encode())
            time.sleep(2)

    except Exception as e: 
        print("Error occurred:", e)
    finally:
        print("Closing socket for info pannel.")
        conn.close()
        s.close()    


        

