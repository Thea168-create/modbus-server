from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging
import socket
from threading import Thread

# Enable logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the expected login message
EXPECTED_LOGIN_MESSAGE = "Q2685SY008TX9765"
SERVER_PORT = 502

# Initialize the Modbus datastore
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

# Function to log client connections
def log_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", SERVER_PORT))
        s.listen()
        logging.info(f"Server listening for connections on port {SERVER_PORT}...")
        while True:
            conn, addr = s.accept()
            logging.info(f"New connection from {addr}")
            data = conn.recv(1024).decode().strip()
            if data.startswith(EXPECTED_LOGIN_MESSAGE):
                logging.info(f"Valid login message received from {addr}")
            else:
                logging.warning(f"Invalid login message from {addr}: {data}")
            conn.close()

# Start the Modbus TCP server
def start_modbus_server():
    logging.info("Starting Modbus TCP Server...")
    StartTcpServer(context, address=("0.0.0.0", SERVER_PORT))

# Run the logging thread and Modbus server
if __name__ == "__main__":
    # Start the logging thread
    Thread(target=log_connections, daemon=True).start()
    
    # Start the Modbus server
    try:
        start_modbus_server()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
