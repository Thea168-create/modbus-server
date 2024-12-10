from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataStore
from pymodbus.datastore import ModbusSlaveContext, ModbusContext
from pymodbus.device import ModbusDeviceIdentification

# Create datastore and slave context
store = ModbusSequentialDataStore()
slave_context = ModbusSlaveContext(hr=store)
context = ModbusContext(slave_context)

# Set up server identity
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyVendor'
identity.ProductCode = 'ModbusServer'
identity.ProductName = 'Modbus TCP Server'
identity.ModelName = 'Model1'

# Start the Modbus server
StartTcpServer(context, identity=identity, address=("0.0.0.0", 1234))
