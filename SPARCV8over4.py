#Falta convertir valores registros y  mem en hexa
#Bloquear Step si esta en rojo

import network
import socket
import ure
import json


#BACKEND MEM#########################
import array
import uctypes

memory={}

struct_32 = {
    "value": uctypes.UINT32 | 0  # UINT32 es un entero sin signo de 32 bits, y 0 es el offset en la estructura
}

def get_uctype(address):
    if  address not in memory:
        memory[address]=uctypes.struct(address, struct_32)
    return memory[address]



   
    
def read_memory(address,rd):
    assert address % 4 == 0, f"The address {address} is not divisible by 4."
    print('read_memory',address)
    return get_uctype(address).value

def write_memory(address,data):
    assert address % 4 == 0, f"The address {address} is not divisible by 4."
    print( 'write_memory',address,data)
    get_uctype(address).value=data
     
 

def malloc(num_bytes,rd):
    assert num_bytes % 4 == 0, f"The number {num_bytes} is not divisible by 4."
    buff_0 = array.array('b', (10+_ for _ in range(num_bytes)))
    dir0 = uctypes.addressof(buff_0)
    print('malloc',num_bytes,dir0,type(dir0))
    for address in range(dir0,dir0+num_bytes,4):
        write_memory(address,0)
    
    return dir0

#################################


URL_other='http://192.168.175.1:8000/'

# Connect to Wi-Fi
ssid = 'Ejemplo'
password = '12345678'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# HTML content to serve
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assembler Code Step Simulator</title>
    <style>
        textarea { width: 100%; }
        pre { background-color: #f0f0f0; padding: 10px; }
        table { width: 100%; }
        th, td { padding: 5px; text-align: left; }
    </style>
</head>
<body>
    <h1>Assembler Code Step Simulator</h1>
    <textarea id="codeInput" rows="15" cols="60">
backend 1
malloc R5,16
MOV R1,5
SETHI R2,1048944
LD R3,[R2+28]
SUBcc R1,R1,1
BzC -3
backend  0
NOP

    </textarea>
    <br>
    <button onclick="step()"  id="btn_step">Step</button
    <h2>Simulation Output</h2>
    <pre id="output"></pre>
    <h2>Register States</h2>
    <table>
        <thead>
            <tr><th>Register</th><th>Value</th></tr>
        </thead>
        <tbody id="registerTable">
        </tbody>
    </table>

  

<div id="memory-container">
    <!--input type="text" id="memory_address" placeholder="Memory Address"/-->
    <div id="backend-switch">
        <label class="switch">
            <input type="checkbox" id="backend-checkbox">
            <span class="slider"></span>
        </label>
        <span id="backend-text">Backend</span>
    </div>
</div> 
    
    <h2>Memory </h2>
<textarea id="memoryInput" rows="10" cols="60">  </textarea>


        <!-- Link to the external JavaScript file -->
        <script src="https://gerardomunoz.github.io/SPARCV8over4/SPARCV8over4_sim.js"></script>
        <!--script src="http://192.168.175.1:8000/SPARCV8over4_sim.js"></script-->
    </body>
</html>
"""

def str2tuple(txt):
    print('str2tuple',txt)
    return txt.strip("()[}").replace('%2C',',').split(",")
                  

# Function to handle incoming requests
def handle_request(client):
    request = client.recv(1024)
    request_str = request.decode('utf-8')
    
    print('Received request:')
    print(request_str)

    # Serve the HTML page
    if 'GET / ' in request_str or 'GET /api' not in request_str:
        client.send('HTTP/1.1 200 OK\r\n')
        client.send('Content-Type: text/html\r\n')
        client.send('Access-Control-Allow-Origin: {URL_other}\r\n')
        client.send('Access-Control-Allow-Credentials: true\r\n')
 
        client.send('Connection: close\r\n\r\n')
        client.sendall(html)
        client.close() 
    
    # Handle the API request
    elif 'GET /api' in request_str:
        match = ure.search(r'GET /api\?([^\s]+) HTTP', request_str)
        response_dir={}
        if match:
            query_string = match.group(1)
            params = query_string.split('&')
            json_data = {}
            for param in params:
                key, value = param.split('=')
                json_data[key] = value
            
            print("Received JSON data:")
            dat_r=json.dumps(json_data)
            print(json_data)  # Pretty print the JSON data
            for key,val in json_data.items():
                print('dic',key,val)
                if key=='malloc':
                    numb,rd = str2tuple(val)
                    numb=int(numb)
                    address=malloc(numb,rd)
                    for addr_i in range(address,address+numb,4):
                        response_dir[addr_i]=0
                    response_dir[rd]=address
                elif key=='write_memory':
                    
                    #cleaned_string = val.strip("()")
                    #addr,dat = cleaned_string.split(",")
                    addr,dat = str2tuple(val)
                    addr=int(addr)
                    dat=int(dat)
                    write_memory(addr,dat)
                    response_dir[addr]=dat
                elif key=='read_memory':
                    addr,rd = str2tuple(val)
                    addr=int(addr)
                    dat=read_memory(addr,rd)
                    response_dir[addr]=dat
                    response_dir[rd]=dat
#     def malloc(num_bytes):
#     print('malloc',num_bytes)
# 
# 
# def write_memory(address,data):
#     print( 'write_memory',address,data)
#     
#     
# read_memory(address):
#     print('read_memory',address)
        response_json = json.dumps(response_dir)
        print(response_json)
        client.send('HTTP/1.1 200 OK\r\n')
        #client.send('Content-Type: text/plain\r\n')
        #client.send('Connection: close\r\n\r\n')
        #client.send('Request received and processed\r\n')
        client.send('Content-Type: application/json\r\n')
        client.send('Connection: close\r\n\r\n')
        client.send(response_json)  # Send JSON response
    
    client.close()

# Start the server
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    
    print('Server listening on', addr)
    
    while True:
        client, addr = server_socket.accept()
        print('Client connected from', addr)
        handle_request(client)

# Start the web server
start_server()
#Powered by ChatGPT