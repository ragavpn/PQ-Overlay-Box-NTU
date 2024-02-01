import socket
import oqs
import pickle

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

# Create a Key Encapsulation object
kemalg = "Kyber512"
with oqs.KeyEncapsulation(kemalg) as server:
    # Receive the public key from Quantum Container 2
    public_key_client = client_socket.recv(1024)

    # Encapsulate the data
    ciphertext, shared_secret_server = server.encap_secret(public_key_client)

    # Create a list of values
    values = [ciphertext, shared_secret_server, data]

    # Serialize the list into a byte stream
    serialized_values = pickle.dumps(values)

    # Send the ciphertext to Quantum Container 2
    client_socket.send(serialized_values)
    print(f"Ciphertext sent to Quantum Container 2: {data.decode()}")
client_socket.close()