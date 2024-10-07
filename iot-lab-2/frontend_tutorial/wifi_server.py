import configparser
import socket
import time


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




with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print('start')

    try:
        while True:
            conn, addr = s.accept()
            print("connected by: ", addr)
        

            data = read_cpu_temperature()
            conn.sendall(str(data).encode())
            time.sleep(2)

    except Exception as e: 
        print("Error occurred:", e)
    finally:
        print("Closing socket for info pannel.")
        conn.close()
        s.close()    


        

