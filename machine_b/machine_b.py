# machine_b.py

import socket

# Setup socket for receiving data from Quantum Container 2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12347))  # Bind to port 12347
s.listen(1)

# Accept incoming connection from Quantum Container 2
conn_q, addr_q = s.accept()
print(f"Connection from Quantum Container 2: {addr_q}")

# Receive data from Quantum Container 2
data = conn_q.recv(1024)
print(f"Received data from Quantum Container 2: {data.decode()}")

# Close connection with Quantum Container 2
conn_q.close()
