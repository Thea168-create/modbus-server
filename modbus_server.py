from pymodbus.server.sync import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging
from pymodbus.exceptions import InvalidMessageReceivedException

# Enable logging to display messages in the terminal
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

# Set up the Modbus slave (server) datastore
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (if used for control)
)

context = ModbusServerContext(slaves=store, single=True)

# Function to respond with heartbeat ACK message ("A")
def send_heartbeat_ack(client_socket):
    try:
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
    try:
        if request.function_code == 16:
            print(f"Received write request: {request}")
            for i, value in enumerate(request.values):
                start_address = request.address + i
                print(f"Writing value {value} to register {start_address}")
                context[0].setValues(3, start_address, [value])

            # Send heartbeat acknowledgment after processing write request
            send_heartbeat_ack(client_socket)
    except InvalidMessageReceivedException as e:
        log.error(f"Invalid Modbus message received: {e}")
        # Respond with a Modbus error code (e.g., Exception Code 0x01 for illegal function)
        send_heartbeat_ack(client_socket)

# Handle Modbus request (this will handle regular Modbus requests like Read, Write)
def handle_request(request, client_socket):
    """
    Handle incoming Modbus requests.
    """
    try:
        print(f"Received Modbus request: {request}")
        if request.function_code == 16:
            handle_write_request(request, client_socket)
        else:
            send_heartbeat_ack(client_socket)
    except InvalidMessageReceivedException as e:
        log.error(f"Error processing Modbus request: {e}")
        send_heartbeat_ack(client_socket)  # Send error response to client

# Start the Modbus TCP server (Master)
def start_modbus_server():
    """
    Starts the Modbus server, listening for client connections on port 1234.
    """
    print("Starting Modbus TCP Server on port 1234...")
    server = ModbusTcpServer(context, address=("0.0.0.0", 1234))  # Server listens on port 5020
    server.serve_forever()

# Start the server
if __name__ == "__main__":
    start_modbus_server()
