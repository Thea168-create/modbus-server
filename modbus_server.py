import asyncio
from pymodbus.server.asyncio import ModbusTcpServer  # Updated import for asyncio
from pymodbus.datastore import ModbusSlaveContext, ModbusContext
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

# Start the server using asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(server.serve_forever())
