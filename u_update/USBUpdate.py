#!/usr/bin/python
# -*-coding: utf-8 -*-
import os
import time
import serial
import zipfile
import logging
import paramiko
import datetime
import threading
import uiautomator2 as u2
from stat import S_ISDIR as isdir

DevicesIP = {"A13YIP": "", "A8EIP": "", "A21IP": "", "A18VIP": ""}


class Log:

    def __init__(self):
        # 第一步，创建一个logger
        logfilename = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        self.logger = logging.getLogger(logfilename)  # file_name为多个logger的区分唯一性
        self.logger.setLevel(logging.DEBUG)  # Log等级总开关
        # 如果已经有handler，则用追加模式，否则直接覆盖
        mode = 'a' if self.logger.handlers else 'w'
        # 第二步，创建handler，用于写入日志文件和屏幕输出
        log_path = os.getcwd() + '/'
        logfile = log_path + logfilename + '.log'
        fmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        formatter = logging.Formatter(fmt)
        # 文件输出
        fh = logging.FileHandler(logfile, mode=mode)
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        fh.setFormatter(formatter)
        # 往屏幕上输出
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)  # 设置屏幕上显示的格式
        sh.setLevel(logging.INFO)
        # 先清空handler, 再添加
        self.logger.handlers = []
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


Logger = Log()


class Download():
    def __init__(self):
        # 服务器连接信息
        try:
            host_name = '192.168.53.53'
            user_name = 'liweiquan'
            password = 'Zhongling@123'
            port = 22
            # 连接远程服务器
            self.t = paramiko.Transport((host_name, port))
            self.t.connect(username=user_name, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.t)
            Logger.info("Successfully connected to the server")
        except Exception as e:
            Logger.error("Failed to connect to the server:%s" % (e))

    def Checkversionexists(self, remote_dir_name):
        try:
            Checkresult = 0
            date = datetime.datetime.now().strftime('%Y%m%d')
            path = remote_dir_name + '/' + date
            self.sftp.stat(path)
            Checkresult = True
            Logger.info("The latest version exists")
            return Checkresult
        except IOError:
            Checkresult = False
            Logger.warn("The latest version does not exist")
            return Checkresult

    def down_from_remote(self, remote_dir_name, local_dir_name):
        # 远程下载文件
        try:
            remote_file = self.sftp.stat(remote_dir_name)
            if isdir(remote_file.st_mode):
                # 文件夹，不能直接下载，需要继续循环
                self.check_local_dir(local_dir_name)
                Logger.warn('开始下载文件夹：' + remote_dir_name)
                for remote_file_name in self.sftp.listdir(remote_dir_name):
                    sub_remote = os.path.join(remote_dir_name, remote_file_name)
                    sub_remote = sub_remote.replace('\\', '/')
                    sub_local = os.path.join(local_dir_name, remote_file_name)
                    sub_local = sub_local.replace('\\', '/')
                    self.down_from_remote(self.sftp, sub_remote, sub_local)
            else:
                # 文件，直接下载
                Logger.warn('开始下载文件：' + remote_dir_name)
                self.sftp.get(remote_dir_name, local_dir_name)
            Logger.info("File or folder download complete")
        except Exception as e:
            Logger.error("Failed to close the connection to the remote server:%s" % e)

    def check_local_dir(self, local_dir_name):
        # 本地文件夹是否存在，不存在则创建
        try:
            if not os.path.exists(local_dir_name):
                os.makedirs(local_dir_name)
            Logger.info("The current directory does not exist. The current directory has been created")
        except Exception as e:
            Logger.error("Local folder existence failed:%s" % e)

    def unzifile(self, zipfilepath, unzipfilepath):
        # 解压文件
        try:
            f = zipfile.ZipFile(zipfilepath, 'r')  # 压缩文件位置
            for file in f.namelist():
                f.extract(file, unzipfilepath)  # 解压位置
            f.close()
            Logger.info("Successfully decompressed the file")
        except Exception as e:
            Logger.error("Failed to decompress the file:%s" % e)

    def disconnect(self):
        # 关闭连接
        try:
            self.t.close()
            Logger.info("Successfully shut down the remote server")
        except Exception as e:
            Logger.error("Failed to close the remote server:%s" % e)


class ComReadWrite():
    def __init__(self):
        try:
            comPort = input("请输入端口号,例如COM16：")
            self.port = serial.Serial(comPort, 115200)
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
                    return
                else:
                    Logger.warn("Read the serial port log. The content is:%s" % line)

        except Exception as e:
            Logger.error("Failed to read serial port log:%s" % e)

    def ComToAdb(self):
        try:
            self.port.write("root\n".encode())
            self.port.write("telnet 192.168.118.1\n".encode())
            self.port.write("setprop persist.vendor.bosch.usb2.mode peripheral\n".encode())
            Logger.info("Successfully switched to ADB")
        except Exception as e:
            Logger.error("ADB switch failed:%s" % e)

    def ComToHost(self):
        try:
            self.port.write("root\n".encode())
            self.port.write("telnet 192.168.118.1\n".encode())
            self.port.write("setprop persist.vendor.bosch.usb2.mode host\n".encode())
            Logger.info("Successfully switched to HOST")
        except Exception as e:
            Logger.error("HOST switch failed:%s" % (e))

    def CloseCom(self):
        try:
            self.port.close()
            Logger.info("Port closed successfully")
        except Exception as e:
            Logger.error("Failed to close port:%s" % e)


def getDvicesInfo():
    try:
        while True:
            with os.popen(r'adb devices', 'r') as f:
                text = f.read()
            s = text.split("\n")  # 切割换行
            result = [x for x in s if x != '']  # 列生成式去掉空
            devices = []
            result.remove("List of devices attached ")
            # 可能有多个手机设备
            for i in result:
                dev = i.split("\tdevice")
                if len(dev) >= 2:
                    devices.append(dev[0])
            if len(devices) >= 1:
                Logger.info("Successfully obtained the device SN code:%s" % devices)
                return devices
            else:
                Logger.warn("Device SN code not obtained, continue to wait")
                time.sleep(10)
    except Exception as e:
        Logger.error("Failed to get device SN code:%s" % e)


def A13YUsbUpdata(IP):
    try:
        os.popen("python -m uiautomator2 init").read()
        d = u2.connect(IP)
        if d(resourceId="android:id/button2", text="关闭").exists:
            d(resourceId="android:id/button1", text="确定").click()
        time.sleep(1)
        if d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").exists:
            d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").click()
            d(resourceId="com.gxatek.cockpit.account:id/tv_experience", text="体验模式").click()
        time.sleep(1)
        d(resourceId="com.gxa.service.systemui:id/all_menu").click()
        time.sleep(1)
        d(resourceId="com.gxa.service.systemui:id/item_name", text="系统设置").click()
        time.sleep(1)
        d(resourceId="com.gxatek.cockpit.settings:id/system_left").click()
        time.sleep(1)
        if not d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").exists:
            d.swipe(1152, 246, 1152, 715, 0.5)
        time.sleep(1)
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
        time.sleep(1)
        d(resourceId="android:id/text1", text="USB升级").click()
        time.sleep(1)
        d(resourceId="com.gxatek.cockpit.diagnostic:id/usb_update").click()
        time.sleep(1)
        d(resourceId="android:id/button1", text="确定").click()
        Logger.warn("Start USB upgrade,please wait")
    except Exception as e:
        Logger.error("Failed to enter the upgrade process:%s" % (e))


def A13YGetVersionAndLog(IP):
    try:
        os.popen("python -m uiautomator2 init").read()
        d = u2.connect_adb_wifi(IP)
        if d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").exists:
            d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").click()
            d(resourceId="com.gxatek.cockpit.account:id/tv_experience", text="体验模式").click()
        time.sleep(1)
        d(resourceId="com.gxa.service.systemui:id/all_menu").click()
        time.sleep(1)
        d(resourceId="com.gxa.service.systemui:id/item_name", text="系统设置").click()
        time.sleep(1)
        d(resourceId="com.gxatek.cockpit.settings:id/system_left", text="系统设定").click()
        time.sleep(1)
        if not d(resourceId="com.gxatek.cockpit.settings:id/number_view_title", text="系统版本").exists:
            d.swipe(1152, 715, 1152, 246, 0.5)
        time.sleep(1)
        version = d(resourceId="com.gxatek.cockpit.settings:id/number_view_text").get_text()
        Logger.warn("Successfully obtained the version information. The version is: %s , starting to export the log" % (
            version))
        os.popen("adb -s 1234567 shell logcat -d  > ./A13Ylogcat.txt").read()
        Logger.warn("Importing logs, please wait")
        time.sleep(1)
        Logger.info("Log exported successfully")
    except Exception as e:
        Logger.error("Failed to enter the upgrade process:%s" % (e))


# download = Download()
# # 远程文件路径（需要绝对路径）
# remote_dir = '/home/share/ci_deploy/gq8155/20220608/output/GACXXXX_A13Y_AVNT_SH_220608.R8.02_D.zip'
# # 本地文件存放路径（绝对路径或者相对路径都可以）
# local_dir = './start-client.zip'

# # 远程文件开始下载
# download.down_from_remote(remote_dir, local_dir)
# download.Checkversionexists('/home/share/ci_deploy/gq8155A8E')

Ser = ComReadWrite()
Ser.ComToAdb()
time.sleep(1)
A13YUsbUpdata("1234567")
time.sleep(1)
Ser.ComRead()
time.sleep(5)
Ser.ComToAdb()
time.sleep(5)
A13YGetVersionAndLog("1234567")
Ser.CloseCom()

