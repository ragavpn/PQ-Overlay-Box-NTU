# # machine_a.py

# import socket

# # Data to be sent from Machine A
# data = b"Hello from Machine A!"

# # Setup socket for sending data to Quantum Container 1
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('quantum_container1', 12345))  # Connect to Quantum Container 1
# client_socket.send(data)  # Send data to Quantum Container 1
# print(f"Data sent from Machine A to Quantum Container 1: {data.decode()}")
# client_socket.close()


import socket
import ssl

# Load client certificate and key
client_cert = 'cert/machine_a.crt'
client_key = 'cert/machine_a.key'

# Create a TLS context with TLS 1.3 protocol
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='cert/ca.crt')  # Specify the CA's certificate
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.set_ciphers('ECDHE+AESGCM')

# Connect to Machine B
with socket.create_connection(('quantum_container1', 12345)) as sock:
    with context.wrap_socket(sock, server_hostname='machine_b') as ssock:
        # Send data over the TLS connection
        ssock.sendall(b'Hello from Machine A!')
