import socket

# Server configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()
    
    if "LOGIN" in message:
        print(f"Received login message from {addr}: {message}")
        # Send Login ACK
        ack_message = "ACK: LOGIN_OK"
        sock.sendto(ack_message.encode(), addr)
        print(f"Sent ACK to {addr}: {ack_message}")
    else:
        print(f"Received data from {addr}: {message}")
