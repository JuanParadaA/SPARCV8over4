#Falta convertir valores registros y  mem en hexa
#Mem y registros repetidos Quitar uno
#ordenar registros y memoria

import network
import socket
import ure
import json
import time




# import socketpool
# import wifi
import os  # Assuming a filesystem is available
import network
import socket
#import ure
#import json
#import time

# Import the API method from the separate file
from api import api

# Start the server
def start_server(ap=True):
    if ap:
        # wifi.radio.start_ap("RPi-Pico", "12345678")
        # print("wifi.radio ap:", wifi.radio.ipv4_address_ap)
        wlan=network.WLAN(network.AP_IF)
        wlan.active(True)
        wlan.config(essid="RPi-Pico", password="12345678")
        if wlan.active():            
            print("Current SSID",wlan.config('essid'))
            print("IP Address:", ap.ifconfig()[0])
        else:
            print("AP inactive:", wlan.status())

    else:    
        # wifi.radio.connect("Ejemplo","12345678")
        # print("wifi.radio:", wifi.radio.ipv4_address)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect("Ejemplo","12345678")
        for _ in range(10):
            if wlan.isconnected():
                break
            print('.',end='')
            time.sleep(1)
        if wlan.isconnected():
            print("IP Address:", wlan.ifconfig())
        else:
            print("Falied:", wlan.status())
            # The status() method provides connection states:
                        # 
            # Handle connection error
            # Error meanings
            # 0  Link Down
            # 1  Link Join
            # 2  Link NoIp
            # 3  Link Up
            # -1 Link Fail
            # -2 Link NoNet
            # -3 Link BadAuth        


#     pool = socketpool.SocketPool(wifi.radio)
#     s = pool.socket()
#     s.bind(('', 80))
#     s.listen(5)
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    
    print('Server listening on', addr)


    return server_socket

# Get the correct content type based on file extension
def get_content_type(filename):
    if filename.endswith('.html'):
        return 'text/html'
    elif filename.endswith('.js'):
        return 'application/javascript'
    elif filename.endswith('.css'):
        return 'text/css'
    elif filename.endswith('.png'):
        return 'image/png'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    elif filename.endswith('.gif'):
        return 'image/gif'
    else:
        return 'application/octet-stream'

# Check if file exists using os.listdir()
def file_exists(filename):
    directory = '.'  # Directory where the files are stored
    files = os.listdir(directory)  # List all files in the directory
    return filename.lstrip('/') in files

# Serve files or handle API requests
def handle_request(client):
    #buffer = bytearray(1024)  # Create a mutable buffer
    #bytes_received, address = client.recvfrom(buffer)  # Receive data into the buffer and get the sender's address
    request, address = client.recvfrom(1024)#buffer)  # Receive data into the buffer and get the sender's address
    #request = buffer[:bytes_received]
    request_str = request.decode('utf-8')

    # Extract the requested file from the request
    try:
        request_file = request_str.split(' ')[1]
        print('request_file', request_file)
        if request_file == '/':
            request_file = '/index.html'  # Default to index.html if no file is requested
    except IndexError:
        client.send('HTTP/1.1 400 Bad Request\r\n')
        client.close()
        return

    # Check if the request is for the API endpoint
    if request_file.startswith('/api'):
        # Call the api() method from api.py
        client.send(api( request_str))
        client.close()
        return

    # Construct the full file path (you can adjust this to match your file structure)
    file_path = '.' + request_file  # Assuming files are in the current directory

    # Check if the file exists
    if file_exists(request_file):
        print('file_exists')
        # Get the content type for the requested file
        content_type = get_content_type(file_path)

        # Send headers
        client.send('HTTP/1.1 200 OK\r\n')
        client.send(f'Content-Type: {content_type}\r\n')
        client.send('Connection: close\r\n\r\n')

        # Send the file content in chunks
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(1000)
                if not chunk:
                    break
                if chunk[-1]=='\r':
                    chunk += file.read(1) # completes '\r\n'
                client.send(chunk)
                time.sleep_ms(100)
    else:
        print('file does not exist')
        # Send 404 Not Found response
        client.send('HTTP/1.1 404 Not Found\r\n')
        client.send('Content-Type: text/html\r\n')
        client.send('Connection: close\r\n\r\n')
        client.send('<h1>404 Not Found</h1>')

    client.close()

# Start the server and listen for connections
s = start_server(ap=False)
while True:
    conn, addr = s.accept()
    print(f'Got a connection from {addr}')
    handle_request(conn)