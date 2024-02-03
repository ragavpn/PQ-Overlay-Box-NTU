# import socket
# import oqs
# import pickle

# def receive_all(sock, buffer_size=4096):
#     data = b""
#     while True:
#         part = sock.recv(buffer_size)
#         data += part
#         if len(part) < buffer_size:
#             # either 0 or end of data
#             break
#     return data

# # Setup socket for receiving data from Quantum Container 1
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('0.0.0.0', 12346))  # Bind to port 12346
# s.listen(1)

# # Accept incoming connection from Quantum Container 1
# conn_q, addr_q = s.accept()
# print(f"Connection from Quantum Container 1: {addr_q}")

# # create signer and verifier with sample signature mechanisms
# sigalg = "Dilithium2"
# with oqs.Signature(sigalg) as verifier:

#     serialized_values = receive_all(conn_q)

#     # Deserialize the list
#     values = pickle.loads(serialized_values)
#     data = values[0]
#     signature = values[1]
#     signer_public_key = values[2]

#     # verifier verifies the signature
#     is_valid = verifier.verify(data, signature, signer_public_key)

#     if (is_valid == False):
#         raise Exception("Invalid signature!")
    
#     print("Data received from Quantum Container 1")
#     conn_q.close()

# # Setup socket for sending data to Machine B
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('machine_b', 12347))  # Connect to Machine B using its IP address
# client_socket.send(data)  # Send data to Machine B
# print("Data sent to Machine B")
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

def start_server_a_relay(server_a_host, server_a_port, server_b_host, server_b_port):
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
    SERVER_A_HOST = "quantum_container1"  # Change this to the appropriate address for Server A
    SERVER_A_PORT = 12345  # Change this to the appropriate port for Server A

    SERVER_B_HOST = "machine_b"  # Change this to the appropriate address for Server B
    SERVER_B_PORT = 54321  # Change this to the appropriate port for Server B

    start_server_a_relay(SERVER_A_HOST, SERVER_A_PORT, SERVER_B_HOST, SERVER_B_PORT)