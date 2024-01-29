# machine_a.py

import socket

# Data to be sent from Machine A
data = b"Hello from Machine A!"

# Setup socket for sending data to Quantum Container 1
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('quantum_container1', 12345))  # Connect to Quantum Container 1
client_socket.send(data)  # Send data to Quantum Container 1
print(f"Data sent from Machine A to Quantum Container 1: {data.decode()}")
client_socket.close()
