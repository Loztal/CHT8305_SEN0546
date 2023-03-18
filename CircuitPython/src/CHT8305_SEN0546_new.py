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
import board, busio, time

# I2C Address for the CHT8305/SEN0546
CHT8305_Address = 0x40
I2C_Delay_time = 0.01
# Registers
REG_TEMPERATURE = 0x00
REG_HUMIDITY = 0x01
REG_CONFIG = 0x02
REG_ALERT_SETUP = 0x03
REG_MANUFACTURE_ID = 0xFE
REG_VERSION_ID = 0xFF

i2c = busio.I2C(board.SCL, board.SDA)

print ("I2C Devices found: ", [hex(i) for i in i2c.scan()])


def get_CHT8305_CONFIG ():
    i2c.writeto(CHT8305_Address, bytes([REG_CONFIG]), stop = False)
    time.sleep(I2C_Delay_time)
    Config_setting = bytearray(2)
    i2c.readfrom_into(CHT8305_Address, Config_setting)
    print("Config setting hex: ", hex(Config_setting[0]), hex(Config_setting[1]))
    print("Config setting bin: ", bin(Config_setting[0]), bin(Config_setting[1]))
def set_CHT8305_CONFIG_HEATER_ON ():
    i2c.writeto(CHT8305_Address, bytes([REG_CONFIG]), stop = False)
    time.sleep(I2C_Delay_time)
    Config_setting = bytearray(2)
    Config_setting[0] = 0x30
    Config_setting[1] = 0x00
    print("Config setting Heater ON hex: ", hex(Config_setting[0]), hex(Config_setting[1]))
    i2c.readfrom_into(CHT8305_Address, Config_setting)
    time.sleep(I2C_Delay_time)
    #i2c.writeto_then_readfrom(CHT8305_Address, Config_setting, Config_setting)
    print("Config Heater ON hex: ", hex(Config_setting[0]), hex(Config_setting[1]))
    print("Config Heater ON bin: ", bin(Config_setting[0]), bin(Config_setting[1]))
def set_CHT8305_CONFIG_HEATER_OFF ():
    i2c.writeto(CHT8305_Address, bytes([REG_CONFIG]), stop = False)
    time.sleep(I2C_Delay_time)
    Config_setting = bytearray(2)
    Config_setting[0] = 0x10
    Config_setting[1] = 0x00
    i2c.readfrom_into(CHT8305_Address, Config_setting)
    print("Config Heater OFF hex: ", hex(Config_setting[0]), hex(Config_setting[1]))
    print("Config Heater OFF bin: ", bin(Config_setting[0]), bin(Config_setting[1]))
def get_CHT8305_MANUFACTURE_ID ():
    i2c.writeto(CHT8305_Address, bytes([REG_MANUFACTURE_ID]), stop = False)
    time.sleep(I2C_Delay_time)
    Manufacture_ID = bytearray(2)
    i2c.readfrom_into(CHT8305_Address, Manufacture_ID)
    print("Manufacture-ID hex: ", hex(Manufacture_ID[0]), hex(Manufacture_ID[1]))
def get_CHT8305_VERSION_ID ():
    i2c.writeto(CHT8305_Address, bytes([REG_VERSION_ID]), stop = False)
    time.sleep(I2C_Delay_time)
    Version_ID = bytearray(2)
    i2c.readfrom_into(CHT8305_Address, Version_ID)
    print("Version-ID hex: ", hex(Version_ID[0]), hex(Version_ID[1]))
def get_CHT8305_TEMPERATURE_HUMIDITY ():
    i2c.writeto(CHT8305_Address, bytes([REG_TEMPERATURE]), stop = False)
    time.sleep(I2C_Delay_time)
    Temperature_raw = bytearray(4)
    Temperature_raw[0] = REG_TEMPERATURE
    i2c.readfrom_into(CHT8305_Address, Temperature_raw)
    #print("Temperature_raw hex: ", hex(Temperature_raw[0]), hex(Temperature_raw[1]), hex(Temperature_raw[2]), hex(Temperature_raw[3]))
    Temperature_prep = Temperature_raw[0] << 8 | Temperature_raw[1]
    Temperature = (Temperature_prep * 165 / 65535) - 40
    print("Temperature: ", Temperature)
    Humidity_prep = Temperature_raw[2] << 8 | Temperature_raw[3]
    Humidity = (Humidity_prep / 65535) * 100
    print("Humidity from Temp: ", Humidity)
def get_CHT8305_HUMIDITY ():
    i2c.writeto(CHT8305_Address, bytes([REG_HUMIDITY]), stop = False)
    time.sleep(I2C_Delay_time)
    Humidity_raw = bytearray(4)
    Humidity_raw[0] = REG_HUMIDITY
    i2c.readfrom_into(CHT8305_Address, Humidity_raw)
    #print("Humidity_raw hex: ", hex(Humidity_raw[0]), hex(Humidity_raw[1]), hex(Humidity_raw[2]), hex(Humidity_raw[3]))
    Humidity_prep = Humidity_raw[0] << 8 | Humidity_raw[1]
    Humidity = (Humidity_prep / 65535) * 100
    print("Humidity: ", Humidity)
if __name__ == "__main__":
    #get_CHT8305_CONFIG()
    #time.sleep(I2C_Delay_time)
    #set_CHT8305_CONFIG_HEATER_ON()
    #time.sleep(I2C_Delay_time)
    #get_CHT8305_CONFIG()
    #time.sleep(I2C_Delay_time)
    #set_CHT8305_CONFIG_HEATER_OFF()
    #time.sleep(I2C_Delay_time)
    #get_CHT8305_CONFIG()
    #time.sleep(I2C_Delay_time)
    #get_CHT8305_MANUFACTURE_ID()
    #get_CHT8305_VERSION_ID()
    get_CHT8305_TEMPERATURE_HUMIDITY()
    #get_CHT8305_HUMIDITY()