from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# Define data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
    hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers
)
context = ModbusServerContext(slaves=store, single=True)

# Server identity
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyCompany'
identity.ProductCode = 'MyModbusServer'
identity.VendorUrl = 'http://mycompany.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'ModbusTCPServer'
identity.MajorMinorRevision = '1.0'

# Run the server on port 502
if __name__ == "__main__":
    print("Starting Modbus TCP Server...")
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 502))
