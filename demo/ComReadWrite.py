import time

import serial
from DB_Autotest.demo.Log import Logger


class ComReadWrite:
    def __init__(self, comport, combaud):
        try:
            self.port = serial.Serial(comport, combaud, timeout=30)
            Logger.info("Serial port connection succeeded")
        except Exception as e:
            Logger.error("Serial port connection failed:%s" % e)

    def ComRead(self):
        try:
            while True:
                tmp = str(self.port.readline())
                line0 = ""
                if len(tmp) != 0:
                    if r"\r\n'" in tmp:
                        line0 = tmp.split(r"\r\n'")[0]
                    if r"b'" in line0:
                        line = line0.split(r"b'")[1]
                if line == "SUSD_ANIMATION_READY":
                    Logger.info("Successfully read serial port log")
                    return True
                else:
                    Logger.info("Read the serial port log. The content is:%s" % line)
        except Exception as e:
            Logger.error("Failed to read serial port log:%s" % e)

    def ComToAdb(self):
        try:
            self.port.write("dtach -a /tmp/android\n".encode())
            self.port.write("setprop persist.sv.debug.adb_enable 1\n".encode())
            # self.port.write("setprop persist.vendor.bosch.usb2.mode peripheral\n".encode())
            Logger.info("Successfully switched to ADB")
        except Exception as e:
            Logger.error("ADB switch failed:%s" % e)

    def ComToHost(self):
        try:
            self.port.write("dtach -a /tmp/android\n".encode())
            self.port.write("setprop persist.sv.debug.adb_enable 0\n".encode())
            Logger.info("Successfully switched to HOST")
        except Exception as e:
            Logger.error("HOST switch failed:%s" % (e))

    def CloseCom(self):
        try:
            self.port.close()
            Logger.info("Port closed successfully")
        except Exception as e:
            Logger.error("Failed to close port:%s" % (e))

    def logcat(self):
        self.port.write("root\n".encode())
        self.port.write("telnet 192.168.118.1\n".encode())
        self.port.write("logcat\n".encode())
        tmp = str(self.port.readline())
        time.sleep(60)
        Logger.info(f'{tmp}')


if __name__ == '__main__':
    com = ComReadWrite(comport='COM117', combaud='921600')
    com.get_dbversion()

