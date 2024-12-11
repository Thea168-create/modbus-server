from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging
import socket

# Enable logging to display messages in the terminal
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

# Set up the Modbus slave (server) datastore
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (if used for control)
)

context = ModbusServerContext(slaves=store, single=True)

# Expected login message (ASCII)
EXPECTED_LOGIN_MESSAGE = "Q2685SY008TX9765"

# Handle the login request from the client
def handle_login(client_socket):
    try:
        # Receive the login message from the client (up to 1024 bytes)
        login_message = client_socket.recv(1024).decode('ascii')
        log.debug(f"Received login message: {login_message}")

        if login_message == EXPECTED_LOGIN_MESSAGE:
            # Send acknowledgment for the login
            client_socket.send(b"LOGIN_SUCCESS")
            log.debug("Login successful, ready to receive Modbus requests")
        else:
            # Respond with an error if the login message is incorrect
            client_socket.send(b"LOGIN_FAILED")
            log.debug("Login failed, invalid login message")
            client_socket.close()
            return False  # Stop further communication

        return True  # Proceed to handle Modbus requests
    except Exception as e:
        log.error(f"Error during login: {e}")
        return False

# Function to handle write requests (Function Code 16) from the RTU
def handle_write_request(request, client_socket):
    try:
        if request.function_code == 16:
            log.debug(f"Received write request: {request}")
            for i, value in enumerate(request.values):
                start_address = request.address + i
                log.debug(f"Writing value {value} to register {start_address}")
                context[0].setValues(3, start_address, [value])

            # Send heartbeat acknowledgment after processing write request
            send_heartbeat_ack(client_socket)
    except Exception as e:
        log.error(f"Error processing write request: {e}")

# Function to handle Modbus request (Function Code 3, 16, etc.)
def handle_request(request, client_socket):
    try:
        log.debug(f"Received Modbus request: {request}")
        if request.function_code == 16:
            handle_write_request(request, client_socket)
        else:
            send_heartbeat_ack(client_socket)
    except Exception as e:
        log.error(f"Error processing Modbus request: {e}")
        send_heartbeat_ack(client_socket)

# Function to respond with heartbeat ACK message ("A")
def send_heartbeat_ack(client_socket):
    try:
        message = b"A"  # Heartbeat ACK message in ASCII
        client_socket.send(message)  # Send ASCII "A" as acknowledgment
        log.debug("Heartbeat acknowledgment 'A' sent to RTU.")
    except Exception as e:
        log.error(f"Error sending heartbeat acknowledgment: {e}")

# Start the Modbus TCP server (Master)
def start_modbus_server():
    """
    Starts the Modbus server, listening for client connections on port 5020.
    """
    log.debug("Starting Modbus TCP Server on port 5020...")
    server = ModbusTcpServer(context, address=("0.0.0.0", 5020))  # Server listens on port 5020
    
    # Start listening for client connections
    while True:
        client_socket, client_address = server.server.accept()  # Accept incoming connection
        log.debug(f"Client Connected: {client_address}")

        if not handle_login(client_socket):  # Handle login first
            continue  # Skip further processing if login fails
        
        # Now that the client has logged in, proceed to handle Modbus requests
        server.handle_request(client_socket)

# Start the server
if __name__ == "__main__":
    start_modbus_server()
