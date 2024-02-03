# # machine_b.py

# import socket

# # Setup socket for receiving data from Quantum Container 2
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('0.0.0.0', 12347))  # Bind to port 12347
# s.listen(1)

# # Accept incoming connection from Quantum Container 2
# conn_q, addr_q = s.accept()
# print(f"Connection from Quantum Container 2: {addr_q}")

# # Receive data from Quantum Container 2
# data = conn_q.recv(1024)
# print(f"Received data from Quantum Container 2: {data.decode()}")

# # Close connection with Quantum Container 2
# conn_q.close()


import socket
import ssl

# Load server certificate and key
server_cert = 'cert/machine_b.crt'
server_key = 'cert/machine_b.key'
ca_cert = 'cert/ca.crt'  # CA certificate for verification

# Create a TLS context with TLS 1.3 protocol
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=ca_cert)

# Listen for incoming TLS connections
with socket.create_server(('0.0.0.0', 12347)) as server:
    with context.wrap_socket(server, server_side=True) as ssock:
        # Accept incoming connections
        conn, addr = ssock.accept()
        with conn:
            # Receive data from Machine A
            data = conn.recv(1024)
            print("Received data from Machine A")
