from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging
import socket

# Enable logging to display messages in the terminal
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Set up the Modbus slave (server) datastore
# Holding Registers will store 32-bit values (split into two 16-bit registers)
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (e.g., for AIN0-AIN5)
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (if used for control)
)

context = ModbusServerContext(slaves=store, single=True)

# Function to respond with heartbeat ACK message ("A")
def send_heartbeat_ack(client_socket):
    try:
        # When the server receives "Q", it responds with "A"
        message = b"A"  # Heartbeat ACK message in ASCII
        client_socket.send(message)  # Send ASCII "A" as acknowledgment
        print("Heartbeat acknowledgment 'A' sent to RTU.")
    except Exception as e:
        print(f"Error sending heartbeat acknowledgment: {e}")

# Function to handle write requests (Function Code 16) from the RTU
def handle_write_request(request, client_socket):
    """
    Handles a write request from the RTU (client).
    This will write data to the holding registers in the Modbus server.
    """
    if request.function_code == 16:
        # Process the write request and update the holding registers
        print(f"Received write request: {request}")
        
        # Example: Writing 32-bit data (mapping 20128, 20130, etc.)
        # Each 32-bit data takes 2 registers, so we map to two holding registers
        for i, value in enumerate(request.values):
            start_address = request.address + i
            print(f"Writing value {value} to register {start_address}")
            context[0].setValues(3, start_address, [value])
        
        # Send heartbeat acknowledgment after processing write request
        send_heartbeat_ack(client_socket)

# Handle Modbus request (this will handle regular Modbus requests like Read, Write)
def handle_request(request, client_socket):
    """
    Handle incoming Modbus requests.
    """
    print(f"Received Modbus request: {request}")
    
    # If it's a write request (Function Code 16), we will handle it here
    if request.function_code == 16:
        handle_write_request(request, client_socket)
    else:
        send_heartbeat_ack(client_socket)  # Send heartbeat acknowledgment for other requests

# Start the Modbus TCP server (Master)
def start_modbus_server():
    """
    Starts the Modbus server, listening for client connections on port 5020.
    """
    print("Starting Modbus TCP Server on port 5020...")
    server = ModbusTcpServer(context, address=("0.0.0.0", 5020))  # Server listens on port 5020
    server.serve_forever()

# Start the server
if __name__ == "__main__":
    start_modbus_server()
