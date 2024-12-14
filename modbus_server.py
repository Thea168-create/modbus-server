import socket

# Server configuration
UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 1234     # Port number to match the RTU configuration

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on port {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
    print(f"Received data: {data.decode()} from {addr}")
