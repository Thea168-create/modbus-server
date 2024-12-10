from pymodbus.server.sync import ModbusTcpServer  # For pymodbus 2.x
from pymodbus.datastore import ModbusSlaveContext, ModbusContext  # ModbusContext is available in 2.x
import logging

# Set up logging for better output
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a Modbus datastore
store = ModbusSlaveContext()
context = ModbusContext(slaves=store, single=True)  # Using ModbusContext for pymodbus 2.x

# Create the Modbus server
server = ModbusTcpServer(context, address=("0.0.0.0", 5020))

# Start the server
server.serve_forever()
