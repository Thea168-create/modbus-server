import socket

# Server configuration
TCP_IP = "0.0.0.0"  # Listen on all available interfaces
TCP_PORT = 1234

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)

print(f"Listening for TCP connections on port {TCP_PORT}...")

while True:
    conn, addr = sock.accept()
    print(f"Connection established with {addr}")
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received data from {addr}: {message}")
        
        # Optional: Send ACK message
        if "LOGIN" in message:
            ack_message = "LOGIN_OK"
            conn.send(ack_message.encode())
            print(f"Sent ACK to {addr}: {ack_message}")
    
    conn.close()
    print(f"Connection closed with {addr}")
