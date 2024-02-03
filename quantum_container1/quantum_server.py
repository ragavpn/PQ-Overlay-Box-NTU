# import socket
# import oqs
# import pickle

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('0.0.0.0', 12345))  # Bind to port 12345
# s.listen(1)

# # Accept incoming connection from Machine A
# conn_a, addr_a = s.accept()
# print(f"Connection from Machine A: {addr_a}")

# # Receive data from Machine A
# data = conn_a.recv(1024)
# print("Received data from Machine A")

# # Close connection with Machine A
# conn_a.close()

# # Setup socket for sending data to Quantum Container 2
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('quantum_container2', 12346))  # Connect to Quantum Container 2

# # create signer and verifier with sample signature mechanisms
# sigalg = "Dilithium2"
# with oqs.Signature(sigalg) as signer:

#     # signer generates its keypair
#     signer_public_key = signer.generate_keypair()

#     # signer signs the message
#     signature = signer.sign(data)

#     # Create a list of values
#     values = [data, signature, signer_public_key]

#     # Serialize the list into a byte stream
#     serialized_values = pickle.dumps(values)

#     # Send the ciphertext to Quantum Container 2
#     client_socket.send(serialized_values)
#     print("Data and Signature sent to Quantum Container 2")
# client_socket.close()

import socket
import ssl
import threading

def handle_client(client_socket, server_b_host, server_b_port):
    # Connect to Server B
    server_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_b_socket.connect((server_b_host, server_b_port))

    # Wrap sockets in SSL
    client_socket = ssl.wrap_socket(client_socket, server_side=True, keyfile="server-key.pem", certfile="server-cert.pem", ssl_version=ssl.PROTOCOL_TLS)

    server_b_socket = ssl.wrap_socket(server_b_socket, ssl_version=ssl.PROTOCOL_TLS)

    # Create a relay from client to server B
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        server_b_socket.send(data)

        data = server_b_socket.recv(4096)
        if not data:
            break
        client_socket.send(data)

    # Close the connections
    client_socket.close()
    server_b_socket.close()

def start_relay(server_a_host, server_a_port, server_b_host, server_b_port):
    server_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_a.bind((server_a_host, server_a_port))
    server_a.listen(5)

    print(f"Listening for incoming connections on {server_a_host}:{server_a_port}")

    while True:
        client_socket, addr = server_a.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, server_b_host, server_b_port))
        client_handler.start()

if __name__ == "__main__":
    SERVER_A_HOST = "machine_a"  # Change this to the appropriate address for Server A
    SERVER_A_PORT = 12345  # Change this to the appropriate port for Server A

    SERVER_B_HOST = "quantum_container2"  # Change this to the appropriate address for Server B
    SERVER_B_PORT = 54321  # Change this to the appropriate port for Server B

    start_relay(SERVER_A_HOST, SERVER_A_PORT, SERVER_B_HOST, SERVER_B_PORT)