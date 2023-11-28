import serial.tools.list_ports
import struct
import time

# ports = serial.tools.list_ports.comports()
#
# for port, desc, hwid in sorted(ports):
#         print("{}: {} [{}]".format(port, desc, hwid))
# ser=serial.Serial(port="COM4", baudrate=115200)
# #ser.close()
# if (port == 0):
#         return "Pace Maker Not Connected"
# else:
#         pace_maker = serial.Serial(port="COM" + str(port), baudrate=115200)
#
pace_maker = serial.Serial(port="COM4", baudrate=115200,timeout=1)
#pace_maker.open()
Header = '<19i'
# Header = '<2B4Hf2Hf4HfH3f'
# if (AA == 'OFF'):
#         AA = 0
# if (VA == 'OFF'):
#         VA = 0
# AA = float(AA)
# VA = float(VA)
# data = struct.pack(Header, 0x16, 0x55, mode,APW, VPW, LR,AA, VA, ARP, VRP,AVD, AS, VS, RecovTime, RF, MSR,  AT, ReactTime, ATS)
# print(len(data))
pace_maker.write(struct.pack('<2Bf', 0x16, 0x22, 0))

# print(len(data))
time.sleep(0.5)
print("print 1")
serialdata = pace_maker.read(9)
serialdata = serialdata.decode('utf-8').strip()
# print(serialdata)
# pace_maker.close()

print("print 2")
# print(len(data))
mode_pacemaker = struct.unpack('B', serialdata[0:1])
LR_pacemaker = struct.unpack('B', serialdata[1:5])
APW_pacemaker = struct.unpack('f', serialdata[5:9])
# VPW_pacemaker = struct.unpack('f', serialdata[23:27])
print(mode_pacemaker)
print(LR_pacemaker)
print(APW_pacemaker)
# print(VPW_pacemaker)
# VA_pacemaker = struct.unpack('f', serialdata[24:28])
# ARP_pacemaker = struct.unpack('H', serialdata[28:30])
# VRP_pacemaker = struct.unpack('H', serialdata[30:32])
# AA_pacemaker = struct.unpack('f', serialdata[32:36])
# RecovTime_pacemaker = struct.unpack('H', serialdata[36:38])
# RF_pacemaker = struct.unpack('H', serialdata[38:40])
# MSR_pacemaker = struct.unpack('H', serialdata[40:42])
# AVD_pacemaker = struct.unpack('H', serialdata[42:44])
# AT_pacemaker = struct.unpack('f', serialdata[44:48])
# ReactTime_pacemaker = struct.unpack('H', serialdata[48:50])
# ATS_pacemaker = struct.unpack('f', serialdata[50:54])
# VS_pacemaker = struct.unpack('f', serialdata[54:58])
# print(mode_pacemaker[0], LR_pacemaker[0], APW_pacemaker[0], VPW_pacemaker[0], VA_pacemaker[0], ARP_pacemaker[0], VRP_pacemaker[0], AA_pacemaker[0], RecovTime_pacemaker[0], RF_pacemaker[0], MSR_pacemaker[0],
#     AVD_pacemaker[0], AT_pacemaker[0], ReactTime_pacemaker[0], ATS_pacemaker[0], VS_pacemaker[0])

# try:
#         serial.Serial(port="COM4", baudrate=115200)
#         print("Connected to 4")
# except:
#         print("No Connection")
#
# try:
#         serial.Serial(port="COM3", baudrate=115200)
#         print("Connected to 3")
# except:
#         print("No Connection 3")