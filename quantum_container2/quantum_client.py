# quantum_client.py
import socket

# Setup socket for receiving data from Quantum Container 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12346))  # Bind to port 12346
s.listen(1)

# Accept incoming connection from Quantum Container 1
conn_q, addr_q = s.accept()
print(f"Connection from Quantum Container 1: {addr_q}")

# Receive data from Quantum Container 1
data = conn_q.recv(1024)
print(f"Received data from Quantum Container 1: {data.decode()}")

# Close connection with Quantum Container 1
conn_q.close()

# Setup socket for sending data to Machine B
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.18.0.5', 12347))  # Connect to Machine B using its IP address
client_socket.send(data)  # Send data to Machine B
print(f"Data sent to Machine B: {data.decode()}")
client_socket.close()
