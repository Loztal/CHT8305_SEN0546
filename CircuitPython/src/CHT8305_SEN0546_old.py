#
# MIT License
#
#Copyright (c) 2023 Henrik Roslund
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#
import time
from smbus2 import SMBus, i2c_msg

I2Cbus = SMBus(1)
time.sleep(0.5)

#
# CHT8305
# Decimal address:  64  | Hexa address:  0x40
#
CHT8305_Address = 0x40
# Registers
REG_TEMPERATURE = 0x00
REG_HUMIDITY = 0x01
REG_CONFIG = 0x02
REG_ALERT_SETUP = 0x03
REG_MANUFACTURE_ID = 0xFE
REG_VERSION_ID = 0xFF

BIT_T_RES = 2
BIT_H_RES = 0
BIT_BATTERY_OK = 3
BIT_ACQ_MODE = 4
BIT_HEATER = 5
BIT_RST = 7
T_RES_14 = 0
T_RES_11 = 1
H_RES_14 = 0
H_RES_11 = 1
H_RES_8 = 2

wLength = 0
ReadBuf_CHT8305_Temp_Reg = bytes(wLength)
ReadBuf_CHT8305_Hum_Reg = bytes(wLength)
ReadBuf_CHT8305_Manufacture_ID_Reg = bytes(wLength)

com_CHT8305_T_Reg = [0x00, 0x00, 0x00, 0x00]
com_CHT8305_H_Reg = [REG_HUMIDITY, 0x00, 0x00, 0x00]
com_CHT8305_Config_Reg_new = [REG_CONFIG, 0x10, 0x00]
com_CHT8305_Config_Reg_old = [0x10, 0x00]
com_CHT8305_Manufacture_ID_Reg = bytearray(2)

#Config_write_msg = i2c_msg.write(CHT8305_Address, com_CHT8305_Config_Reg_new)
#I2Cbus.i2c_rdwr(Config_write_msg)
#I2Cbus.write_i2c_block_data(CHT8305_Address, REG_CONFIG, com_CHT8305_Config_Reg_old)
time.sleep(0.02)
Temperature_write_msg = i2c_msg.write(CHT8305_Address, REG_TEMPERATURE)
Temperature_read_msg = i2c_msg.read(CHT8305_Address, com_CHT8305_T_Reg)
I2Cbus.i2c_rdwr(Temperature_write_msg, Temperature_read_msg)
#I2Cbus.write_i2c_block_data(CHT8305_Address, REG_TEMPERATURE, com_CHT8305_T_Reg)
time.sleep(0.02)

#print("i2c.readfrom_mem(CHT8305_Address, 0, 1): ", i2c.readfrom_mem(CHT8305_Address, 0, 2))
ReadBuf_CHT8305_Temp_Reg = I2Cbus.readfrom(CHT8305_Address, 4)
#print("ReadBuf_CHT8305_Temp_Reg: ", ReadBuf_CHT8305_Temp_Reg)
#print("ReadBuf_CHT8305_Temp_Reg[0]: ", hex(ReadBuf_CHT8305_Temp_Reg[0]), " | ",ReadBuf_CHT8305_Temp_Reg[0])
#print("ReadBuf_CHT8305_Temp_Reg[1]: ", hex(ReadBuf_CHT8305_Temp_Reg[1]), "| ", ReadBuf_CHT8305_Temp_Reg[1])
#print("ReadBuf_CHT8305_Temp_Reg[2]: ", hex(ReadBuf_CHT8305_Temp_Reg[2]), "| ", ReadBuf_CHT8305_Temp_Reg[2])
#print("ReadBuf_CHT8305_Temp_Reg[3]: ", hex(ReadBuf_CHT8305_Temp_Reg[3]), "| ", ReadBuf_CHT8305_Temp_Reg[3])
#print("ReadBuf_CHT8305_Temp_Reg[4]: ", ReadBuf_CHT8305_Temp_Reg[4])
#print("ReadBuf_CHT8305_Temp_Reg[5]: ", ReadBuf_CHT8305_Temp_Reg[5])

temp_prep = ReadBuf_CHT8305_Temp_Reg[0] << 8 | ReadBuf_CHT8305_Temp_Reg[1]
#print("temp_prep: ", bin(temp_prep))
temp = (temp_prep *165/65535)-40
print("temp: ", temp)

I2Cbus.writeto(CHT8305_Address, REG_HUMIDITY, com_CHT8305_H_Reg)
time.sleep(0.02)
ReadBuf_CHT8305_Hum_Reg = I2Cbus.readfrom(CHT8305_Address, 4)
hum_prep = ReadBuf_CHT8305_Hum_Reg[0] << 8 | ReadBuf_CHT8305_Hum_Reg[1]
hum_prep_from_temp = ReadBuf_CHT8305_Temp_Reg[2] << 8 | ReadBuf_CHT8305_Temp_Reg[3]
#print("hum_prep: ", hum_prep)
hum = (hum_prep /65535)*100
hum_from_temp = (hum_prep_from_temp /65535)*100
print("hum: ", hum)
print("hum_from_temp: ", hum_from_temp)

I2Cbus.writeto(CHT8305_Address, REG_MANUFACTURE_ID, com_CHT8305_Manufacture_ID_Reg)
time.sleep(0.02)
ReadBuf_CHT8305_Manufacture_ID_Reg = I2Cbus.readfrom(CHT8305_Address, 2)
print("ReadBuf_CHT8305_Manufacture_ID_Reg: ", ReadBuf_CHT8305_Manufacture_ID_Reg)
print("ReadBuf_CHT8305_Manufacture_ID_Reg[0]: ", hex(ReadBuf_CHT8305_Manufacture_ID_Reg[0]), " | ",ReadBuf_CHT8305_Manufacture_ID_Reg[0])
print("ReadBuf_CHT8305_Manufacture_ID_Reg[1]: ", hex(ReadBuf_CHT8305_Manufacture_ID_Reg[1]), "| ", ReadBuf_CHT8305_Manufacture_ID_Reg[1])
