import socket
import time

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

    try:
        # Step 1: Wait for Login Message
        data = conn.recv(1024)
        if not data:
            print(f"Connection closed by {addr}")
            conn.close()
            continue

        message = data.decode()
        print(f"Received login message from {addr}: {message}")

        # Step 2: Send Login ACK
        if "LOGIN" in message:
            ack_message = "LOGIN_OK"
            conn.send(ack_message.encode())
            print(f"Sent Login ACK to {addr}: {ack_message}")

            # Step 3: Send Downstream Message (e.g., 0x80)
            downstream_message = b'\x80'
            conn.send(downstream_message)
            print(f"Sent downstream message to {addr}: 0x80")

            # Step 4: Wait for Downstream Response (e.g., 0x80)
            data = conn.recv(1024)
            if data == b'\x80':
                print(f"Received downstream response from {addr}: 0x80")

                # Step 5: Send Modbus Polling Command (Read 2 input registers from Slave ID 1)
                modbus_polling_command = b'\x01\x04\x00\x00\x00\x02\x71\xCB'  # Modbus RTU command
                conn.send(modbus_polling_command)
                print(f"Sent Modbus polling command to {addr}")

                # Step 6: Wait for Sensor Data Response
                data = conn.recv(1024)
                if data:
                    print(f"Received sensor data from {addr}: {data.hex()}")
                else:
                    print("No sensor data received.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()
        print(f"Connection closed with {addr}")
