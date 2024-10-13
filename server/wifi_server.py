import configparser
import socket
import time
import json
from picarx import Picarx
from time import sleep
from tracking import StateTracker


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


def encode_data(temperature, state: StateTracker):
    data = {'Temperature': temperature, 'Orientation': state.state.orientation, 
            'X': state.state.x, 'Y': state.state.y, 'Distance Traveled From Start': state.get_distance_traveled()}
    return json.dumps(data)

def handle_arrows(conn, state: StateTracker):
    px = Picarx()
    data = conn.recv(1024).decode()    # receive 1024 Bytes of message in binary format
    if data:
        print(data)
        if (data == "forward\r\n"):
            px.set_dir_servo_angle(0)
            px.forward(10)
            sleep(1)
            state.update_state_position('Forward')
            # px.set_cam_tilt_angle(60)
        elif (data == "left\r\n"):
            #px.set_cam_tilt_angle(60)
            px.set_dir_servo_angle(-30)
            px.forward(10)
            sleep(1)
            state.update_state_position('Left')
        elif (data == "right\r\n"):
            px.set_dir_servo_angle(30)
            px.forward(10)
            sleep(2)
            state.update_state_position('Right')
        else:
            px.set_dir_servo_angle(0)
            px.backward(10)
            sleep(2)
            state.update_state_position('Backward')
        px.forward(0)
        # conn.sendall(data)

def initialize_server():
    state = StateTracker()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print('start')

        try:
            while True:
                conn, addr = s.accept()
                print("connected by: ", addr)

                handle_arrows(conn, state)
                temperature = read_cpu_temperature()

                data = encode_data(temperature, state)

                conn.sendall(data.encode())
                time.sleep(2)

        except Exception as e:
            print("Error occurred:", e)
        finally:
            print("Closing socket for info pannel.")
            conn.close()
            s.close()


if __name__ == '__main__':
    initialize_server()
