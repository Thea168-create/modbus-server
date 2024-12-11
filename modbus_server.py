import socket
import logging
from pymodbus.server.sync import StartTcpServer, ModbusTcpServer, ModbusRequestHandler
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

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

# Custom request handler to validate the login message
class CustomRequestHandler(ModbusRequestHandler):
    def handle(self):
        try:
            # Receive data and validate the login message if present
            data = self.request.recv(1024).decode().strip()
            if data.startswith(EXPECTED_LOGIN_MESSAGE):
                logging.info(f"Valid login message received from {self.client_address}")
                # Remove the login message before processing Modbus request
                modbus_data = data[len(EXPECTED_LOGIN_MESSAGE):]
                self.request.sendall(modbus_data.encode())
            else:
                logging.warning(f"Invalid login message from {self.client_address}: {data}")
                self.request.sendall(b"Invalid login message\n")
        except Exception as e:
            logging.error(f"Error handling request: {e}")
        finally:
            self.request.close()

# Start the Modbus TCP server with the custom handler
def start_modbus_server():
    logging.info(f"Starting Modbus TCP Server on port {SERVER_PORT}...")
    server = ModbusTcpServer(context, address=("0.0.0.0", SERVER_PORT), handler=CustomRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")

# Main function
if __name__ == "__main__":
    start_modbus_server()
