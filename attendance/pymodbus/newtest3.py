from pymodbus.client import ModbusTcpClient
import random
import time

plcIP = "192.168.7.43"
PORT = 5009

start = True
stop = False

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)



def newClient(client):
    while True:
        try:
            randomInt = random.randint(0, 50)
            time.sleep(2)
            client.write_register(0, randomInt , slave=1)
            r=client.read_holding_registers(0,10,slave=1)
            x = r.registers[0]
            # print(type(x),x)
            if(client.read_coils(0, 1, slave=1).bits[0] == True):
                print("....first if..... ",client.read_coils(0, 3, slave=1).bits[0])   
                client.write_coil(2, start , slave=1)
                if (x >= 27) and (client.read_coils(2,1,slave=1).bits[0]==True):
                    print(".....second if......")
                    client.write_coil(4, start , slave=1)
                    # time.sleep(1)
                    # r=client.read_holding_registers(0,10,slave=1)
                    print("read register",r.registers)
                else:
                    print(".....third if......")
                    client.write_coil(4, stop , slave=1)
                    # time.sleep(1)
                    # r=client.read_holding_registers(0,10,slave=1)
                    print("read register",r.registers)
            if(client.read_coils(1, 1,slave=1).bits[0]==start):
                print(".....fourth if.....")
                client.write_coil(0, stop , slave=1)
                client.write_coil(2, stop, slave=1)
                client.write_coil(4, stop, slave=1)
            if(client.read_coils(1,1,slave=1).bits[0]==True and client.read_coils(0,1,slave=1).bits[0]==True):
                client.write_coil(4 ,False,slave = 1)
            result = client.read_coils(0, 10, slave=1)  
            print("read coil:",result.bits)                      
                # client.close()                         
                # print("...connection closed....")

        except Exception as e:
            print("An error occurred:",e)
            client.close()                         
            print("...connection closed....")
            time.sleep(2)
            connect = client.connect()      
            print("...connecting Again...",connect)
if __name__ == '__main__':
    print("hello")
    client = ModbusTcpClient(plcIP,PORT)   
    client.connect()
    # start push button
    client.write_coil(0,1,slave=1)
    # stop push button
    client.write_coil(1,1,slave=1)
    # fan on-off
    client.write_coil(4,1,slave=1)
    # temperature
    # client.write_register()

    if(client.connect()):
        newClient(client)
    else:
        print("not connected ")
