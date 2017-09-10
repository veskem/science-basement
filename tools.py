import urllib
import serial
import random as rnd

# store the temperature to Wolfram Data Drop
def write_datadrop(temp, databin_id):
    url = "https://datadrop.wolframcloud.com/api/v1.0/Add?bin="
    urllib.urlopen(url + databin_id + "&T=" + str(temp))

# generate serial port object
def get_serial(port_name, baud_rate):
    try:
        ser = serial.Serial(
            port=port_name, baudrate=baud_rate,
            parity=serial.PARITY_NONE, timeout=1,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        return ser
    except serial.SerialException:
        print ("Error: port ", port_name, " not found!")
        return 0

# get random number with specified minimum and amplitude value
def get_random(minimum=0.0, amplitude=1.0):
    return minimum + amplitude * rnd.random()
