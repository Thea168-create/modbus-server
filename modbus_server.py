from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusSocketFramer
from pymodbus.server.sync import ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
import logging
import socket
from threading import Thread

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Modbus datastore
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)

context = ModbusServerContext(slaves=store, single=True)

# Function to log incoming connections
def log_connections(host='0.0.0.0', port=502):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        logging.info(f"Listening for client connections on {host}:{port}...")
        while True:
            conn, addr = s.accept()
            logging.info(f"New client connected: {addr}")
            conn.close()

# Start the Modbus TCP server
if __name__ == "__main__":
    # Run the connection logging in a separate thread
    Thread(target=log_connections, daemon=True).start()

    print("Starting Modbus TCP Server on port 502...")
    StartTcpServer(context, address=("0.0.0.0", 502))
