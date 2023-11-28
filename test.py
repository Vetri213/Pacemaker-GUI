import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

try:
        serial.Serial(port="COM4", baudrate=115200)
        print("Connected to 4")
except:
        print("No Connection")

try:
        serial.Serial(port="COM3", baudrate=115200)
        print("Connected to 3")
except:
        print("No Connection 3")