from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusTcpFramer
import logging
import socket

# Enable logging to display messages in the terminal
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a datastore
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
)

context = ModbusServerContext(slaves=store, single=True)

# Function to log when data is read or written
def log_request(request):
    # Log client connection info (client's IP address and port)
    client_ip = request.client
    client_port = request.client_port
    print(f"Connection from {client_ip}:{client_port} - Request received: {request}")
    return request

# Override the default read/write functions to include logging
context.read_holding_registers = log_request
context.write_registers = log_request
context.read_coils = log_request
context.write_coils = log_request

# Start the Modbus TCP server on port 1234
if __name__ == "__main__":
    print("Starting Modbus TCP Server on port 1234...")
    StartTcpServer(context, address=("0.0.0.0", 1234))
