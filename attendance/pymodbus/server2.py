# Server with specific slave Id

from pymodbus.server import StartTcpServer , ModbusTcpServer
from pymodbus.server import ModbusSimulatorServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# import pymodbus

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def run_server():

    # block = ModbusSequentialDataBlock(0, [888]*32)
    # store = ModbusSlaveContext(hr=block)
    Store = ModbusSlaveContext(
        di = ModbusSequentialDataBlock(0,[0]*100),
        co = ModbusSequentialDataBlock(0,[0]*100),
        hr = ModbusSequentialDataBlock(0,[0]*100),
        ir = ModbusSequentialDataBlock(0,[0]*100)
    )
    Store1 = ModbusSlaveContext(
        disc_inp = ModbusSequentialDataBlock(0,[0]*100),
        disc_co = ModbusSequentialDataBlock(0,[0]*100),
        ana_hr = ModbusSequentialDataBlock(0,[0]*100),
        ana_ir = ModbusSequentialDataBlock(0,[0]*100)
    )
    # context = ModbusServerContext(slaves = Store, single=True)

    # print(context[0].getValues(1,0,count = 10))
   
    # print(Store.getValues(3,0,count=10))

    # print(Store.getValues(4,0,count=10))

    slaves  = {
               0x01: Store,
               0x05: Store1
              }
    context = ModbusServerContext(slaves=slaves, single=False)
    


    StartTcpServer(context = context,address = ("192.168.7.43", 5009))

if __name__ == "__main__":
    run_server()