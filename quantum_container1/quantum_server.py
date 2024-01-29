# quantum_server.py

import socket

# Setup socket for receiving data from Machine A
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12345))  # Bind to port 12345
s.listen(1)

# Accept incoming connection from Machine A
conn_a, addr_a = s.accept()
print(f"Connection from Machine A: {addr_a}")

# Receive data from Machine A
data = conn_a.recv(1024)
print(f"Received data from Machine A: {data.decode()}")

# Close connection with Machine A
conn_a.close()

# Setup socket for sending data to Quantum Container 2
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('quantum_container2', 12346))  # Connect to Quantum Container 2
client_socket.send(data)  # Send data to Quantum Container 2
print(f"Data sent to Quantum Container 2: {data.decode()}")
client_socket.close()
