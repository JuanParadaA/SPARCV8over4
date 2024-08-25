import socketpool
import wifi

URL_other='https://raw.githubusercontent.com'

wifi.radio.connect("Ejemplo","12345678")
pool=socketpool.SocketPool(wifi.radio)

print("wifi.radio",wifi.radio.hostname, wifi.radio.ipv4_address)
s = pool.socket()
s.setsockopt(pool.SOL_SOCKET, pool.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
response = """
/*
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
MOV R1,5
SETHI R2,1048944
LD R3,[R2+28]
SUBcc R1,R1,1
BzC -3
NOP

    </textarea>
    <br>
    <button onclick="step()">Step</button>
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
                <input type="checkbox">
                <span class="slider"></span>
            </label>
            <span>Backend</span>
        </div>
    </div>
    
    
    <h2>Memory </h2>
<textarea id="memoryInput" rows="10" cols="60">  </textarea>



        <!-- Link to the external JavaScript file -->
        <script src="https://gerardomunoz.github.io/SPARCV8over4/SPARCV8over4_sim.js"></script>
    </body>
</html>
"""


while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  buffer = bytearray(1024)  # Create a mutable buffer
  bytes_received, address = conn.recvfrom_into(buffer)  # Receive data into the buffer and get the sender's address
  print("Received from:", address)
  print("Received data:", buffer[:bytes_received])
  conn.send('HTTP/1.1 200 OK\r\n')
  conn.send('Content-Type: text/html\r\n')
  conn.send(f'Access-Control-Allow-Origin: {URL_other}\r\n')
  conn.send('Access-Control-Allow-Credentials: true\r\n')
  conn.send('\r\n')
  conn.send(response)
  conn.close()