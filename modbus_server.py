from pymodbus.server.async import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusContext
from pymodbus.transaction import ModbusTcpProtocol
import logging

# Set up logging for better output
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Create a Modbus datastore
store = ModbusSlaveContext()
context = ModbusContext(slaves=store, single=True)

# Create the Modbus server
server = ModbusTcpServer(context, address=("0.0.0.0", 5020))

# Start the server
server.serve_forever()
