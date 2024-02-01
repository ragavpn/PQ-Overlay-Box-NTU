import socket
import oqs
import pickle

# Setup socket for receiving data from Quantum Container 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12346))  # Bind to port 12346
s.listen(1)

# Accept incoming connection from Quantum Container 1
conn_q, addr_q = s.accept()
print(f"Connection from Quantum Container 1: {addr_q}")

# Create a Key Encapsulation object
kemalg = "Kyber512"
with oqs.KeyEncapsulation(kemalg) as client:
    # Generate a key pair
    public_key_client = client.generate_keypair()

    # Send the public key to Quantum Container 1
    conn_q.send(public_key_client)
    print("Public key sent to Quantum Container 1")

    # Receive the serialized list from the socket
    serialized_values = conn_q.recv(1024)

    # Deserialize the list
    values = pickle.loads(serialized_values)
    ciphertext = values[0]
    shared_secret_server = values[1]
    data = values[2]

    # the client decapsulates the server's ciphertext to obtain the shared secret
    shared_secret_client = client.decap_secret(ciphertext)

    if (shared_secret_client != shared_secret_server):
        raise Exception("Shared secrets are not equal!")
    else:
        print("Shared secrets are equal!")
    
    print(f"Data received from Quantum Container 1: {data.decode()}")
    
    conn_q.close()

# Setup socket for sending data to Machine B
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('machine_b', 12347))  # Connect to Machine B using its IP address
client_socket.send(data)  # Send data to Machine B
print(f"Data sent to Machine B: {data}")
client_socket.close()