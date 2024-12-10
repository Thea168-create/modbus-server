from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import logging

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

# Start the Modbus TCP server on port 1234
if __name__ == "__main__":
    print("Starting Modbus TCP Server on port 1234...")
    StartTcpServer(context, address=("0.0.0.0", 1234))
