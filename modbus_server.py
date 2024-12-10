import logging
from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Enable logging to see server activity
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Define data store with initial test data
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [1, 0, 1, 1, 0, 1, 0, 1, 1, 0]),  # Discrete Inputs: 1, 0, 1, etc.
    co=ModbusSequentialDataBlock(0, [1, 1, 0, 0, 1, 1, 1, 0, 0, 1]),  # Coils: Mixed values
    hr=ModbusSequentialDataBlock(0, [100, 200, 300, 400, 500]),       # Holding Registers: 100, 200, etc.
    ir=ModbusSequentialDataBlock(0, [10, 20, 30, 40, 50])             # Input Registers: 10, 20, etc.
)

context = ModbusServerContext(slaves=store, single=True)

# Server identity information
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyCompany'
identity.ProductCode = 'MyModbusServer'
identity.VendorUrl = 'http://mycompany.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'ModbusTCPServer'
identity.MajorMinorRevision = '1.0'

# Run the Modbus TCP server on port 502
if __name__ == "__main__":
    print("Starting Modbus TCP Server on port 502...")
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))
