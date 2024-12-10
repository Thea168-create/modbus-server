from pymodbus.server.sync import ModbusTcpServer  # For pymodbus 2.x
from pymodbus.datastore import ModbusSlaveContext  # Only use ModbusSlaveContext
import logging

# Set up logging for better output
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a Modbus datastore
store = ModbusSlaveContext()  # Only ModbusSlaveContext needed

# Create the Modbus server
server = ModbusTcpServer(store, address=("0.0.0.0", 5020))  # Directly pass the store

# Start the server
server.serve_forever()
