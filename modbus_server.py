from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

# Enable logging to help with debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize the Modbus datastore with holding registers for incoming data
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),     # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0]*100),     # Coils
    hr=ModbusSequentialDataBlock(0, [0]*100),     # Holding Registers for incoming data
    ir=ModbusSequentialDataBlock(0, [0]*100)      # Input Registers
)

context = ModbusServerContext(slaves=store, single=True)

# Function to log incoming data
def log_data(context):
    while True:
        # Read holding registers (address 0 to 5 for 6 sensor inputs)
        data = context[0].getValues(3, 0, 6)
        logging.info(f"Received data: {data}")

# Start the Modbus TCP server
if __name__ == "__main__":
    from threading import Thread
    print("Starting Modbus TCP Server on port 502...")
    # Run the data logging in a separate thread
    Thread(target=log_data, args=(context,)).start()
    StartTcpServer(context, address=("0.0.0.0", 502))
