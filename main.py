import socket
import threading
import rsa

# Generate RSA public and private keys
public_key, private_key = rsa.newkeys(1024)
public_partner = None

# Ask the user whether they want to host or connect to a host
choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    # If user chooses to host
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.102", 9999))  # Bind the server to the local address and port
    server.listen()  # Listen for incoming connections

    # Accept a connection from a client
    client, _ = server.accept()
    
    # Send the public key to the client
    client.send(public_key.save_pkcs1("PEM"))
    
    # Receive the client's public key
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    # If user chooses to connect to a host
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.1.102", 9999))  # Connect to the server

    # Receive the server's public key
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    
    # Send the public key to the server
    client.send(public_key.save_pkcs1("PEM"))

else:
    exit()  # Exit if the choice is neither 1 nor 2

# Function to handle sending messages
def sending_messages(c):
    while True:
        message = input("")  # Get message input from user
        c.send(rsa.encrypt(message.encode(), public_partner))  # Encrypt and send the message
        print("You: " + message)

# Function to handle receiving messages
def receiving_messages(c):
    while True:
        # Decrypt and print the received message
        print('Partner: ', rsa.decrypt(c.recv(1024), private_key).decode())

# Start threads for sending and receiving messages
threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
