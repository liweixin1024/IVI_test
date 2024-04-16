import os
import time
import zipfile
import paramiko
import datetime
from DB_Autotest.demo.Log import Logger
from DB_Autotest.demo.A19 import A19devices
from DB_Autotest.demo.ComReadWrite import ComReadWrite
from DB_Autotest.dingtalk.dingrobot import DingTalkBot
from stat import S_ISDIR as isdir
import subprocess
from dingtalk import dingrobot
from datetime import datetime

class Download():
    def __init__(self):
        # 服务器连接信息
        self.com = ComReadWrite(comport='COM117', combaud='921600')
        self.dd = DingTalkBot()
        try:
            remoteIP = '192.168.150.150'
            remoteusername = 'lulei'
            remotepassword = 'lulei@456'
            remoteport = 22
            # 连接远程服务器
            self.t = paramiko.Transport((remoteIP, remoteport))
            self.t.connect(username=remoteusername, password=remotepassword)
            self.sftp = paramiko.SFTPClient.from_transport(self.t)
            Logger.info("Successfully connected to the server")
        except Exception as e:
            Logger.error("Failed to connect to the server:%s" % (e))

    def Checkversionexists(self, remote_dir_name):
        # 检查是否存在最新版本
        try:
            Checkresult = 0
            date = datetime.datetime.now().strftime('%Y%m%d')
            path = remote_dir_name
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
                    self.down_from_remote(sub_remote, sub_local)
            else:
                # 文件，直接下载
                Logger.warn('开始下载文件：' + remote_dir_name)
                self.sftp.get(remote_dir_name, local_dir_name)
            Logger.info("File or folder download complete")
        except Exception as e:
            self.disconnect()
            Logger.error("Failed to close the connection to the remote server:%s" % (e))

    def get_file(self, remote_dir_name, local_dir_name):
        Logger.info('开始下载文件：' + remote_dir_name)
        self.sftp.get(remote_dir_name, local_dir_name)

    def check_local_dir(self, local_dir_name):
        # 本地文件夹是否存在，不存在则创建
        try:
            if not os.path.exists(local_dir_name):
                os.makedirs(local_dir_name)
            Logger.info("The current directory does not exist. The current directory has been created")
        except Exception as e:
            Logger.error("Local folder existence failed:%s" % (e))

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

    # def connect(self, func):
    #
    #     def connect_devices(device):
    #         """
    #             通过wifi连接车机
    #         """
    #         subprocess.Popen('adb connect ' + device)
    #         time.sleep(1)
    #         func()
    #         return connect_devices

    def connect_devices(self, device):
        """
            通过wifi连接车机
        """
        subprocess.Popen('adb connect ' + device)
        time.sleep(1)

    def cp_updatepackage(self, devices, file_path: str, target_path: str = '/mnt/media_rw/usb1'):
        """
        复制升级包到U盘
        :param devices: 设备ip
        :param file_path: 复制文件的路径、即升级包push到qnx所在路径
        :param target_path: 目标地址，升级包拷贝到U盘的地址，默认为/mnt/media_rw/usb1
        """
        os.popen('adb connect ' + devices)
        time.sleep(3)
        os.popen(r'adb -s ' + devices + ' shell cp -rf ' + file_path + ' ' + target_path)

    def mv_filename(self, filename: str, tar_filename: str):
        """
        修改文件名
        :param filename:  被修改的文件名，如/mnt/media_rw/A58_AVNT_Update
        :param tar_filename: 目标修改的文件名，如/mnt/media_rw/A13Y_AVNT_Update
        """
        os.rename(filename, tar_filename)

    def getDvicesIP(self, device):
        # 获取车型IP地址
        try:
            time.sleep(2)
            cmd = r'adb -s ' + device + r' shell ifconfig | findstr "192.168.12"'
            with os.popen(cmd, 'r') as f:
                text = f.read()
            s = text.split("          inet addr:")
            ss = s[1].split("  Bcast:192.168.12.255  Mask:255.255.255.0")
            IP = ss[0]
            Logger.info("Successfully obtained IP:%s" % IP)
            devicesname = IP + ":5555"
            print(devicesname)
            return devicesname
        except Exception as e:
            Logger.error("IP acquisition failed:%s" % e)


    def push_update(self, qnx_path, remotepath):
        """
        从本地push升级包到U盘
        :param device: 设备ip，例如："192.168.12.157:5555"
        :param qnx_path: 复制文件的路径、即升级包push到qnx所在路径，例如：'/mnt/，建议qnx端放在/mnt目录下，其他目录的空间可能不够
        :param remotepath: 目标地址，升级包拷贝到U盘的地址，例如：'/mnt/media_rw/usb0/A13Y_AVNT_Update/'
        author: lulei
        """
        device = self.getDvicesIP("12345678")
        subprocess.Popen("adb tcpip 5555")
        self.connect_devices(device)
        Logger.info(f'已连接{device}')
        localpath = "E:/output/usb/"
        zip_file = os.listdir(localpath)
        for i in zip_file:
            cmd = 'adb -s ' + device + r' push ' + localpath + i + " " + qnx_path
            # cmd = 'adb' + r' push ' + localpath + i + " " + qnx_path
            Logger.info(f'开始push文件{i}到{qnx_path}')
            pu = subprocess.Popen(cmd)
            j = 0
            while pu.poll() is None:
                Logger.info(f'当前进程状态为{pu.poll()},NONE为运行中，0为正常结束，2为子进程不存在')
                subprocess.Popen('adb connect ' + device)
                subprocess.Popen('adb shell du -sh mnt/')
                time.sleep(1 + j)
                j += 1
            Logger.info(f'push文件{i}到{qnx_path}成功')
            Logger.info(f'开始复制文件{i}到U盘')
            cp = subprocess.Popen(r'adb -s ' + device + ' shell cp -rf ' + qnx_path + '/' + i + ' ' + remotepath)
            # cp = subprocess.Popen(r'adb' + ' shell cp -rf ' + qnx_path + '/' + i + ' ' + remotepath)
            k = 0
            while cp.poll() is None:
                subprocess.Popen('adb connect ' + device)
                time.sleep(1 + k)
                k += 1
            Logger.info(f'复制文件{i}到U盘成功')
            Logger.info(f'开始删除{qnx_path}路径下{i}文件')
            rm = subprocess.Popen(r'adb -s ' + device + ' shell rm' + ' ' + qnx_path + '/' + i)
            # rm = subprocess.Popen(r'adb' + ' shell rm' + ' ' + qnx_path + '/' + i)
            z = 0
            while rm.poll() is None:
                subprocess.Popen('adb connect ' + device)
                time.sleep(1 + z)
                z += 1
            Logger.info(f'删除{qnx_path}路径下{i}文件成功')
            pu.kill()
            cp.kill()
            rm.kill()
        subprocess.Popen("adb disconnect " + device)
        Logger.info(f"断开与{device}的连接")
        Logger.info('---------------------------')
        Logger.info('U盘升级包准备完成')


    # def push_update_1(self, device, qnx_path, remotepath):
    #     """
    #     从本地push升级包到U盘
    #     :param device: 设备ip，例如："192.168.12.157:5555"
    #     :param qnx_path: 复制文件的路径、即升级包push到qnx所在路径，例如：'/mnt/，建议qnx端放在/mnt目录下，其他目录的空间可能不够
    #     :param remotepath: 目标地址，升级包拷贝到U盘的地址，例如：'/mnt/media_rw/usb0/A13Y_AVNT_Update/'
    #     author: lulei
    #     """
    #     localpath = "E:\A13Y_AVNT_Update"
    #     cmd = 'adb -s ' + device + r' push ' + localpath + " " + qnx_path
    #     Logger.info(f'开始push文件到{qnx_path}')
    #     pu = subprocess.Popen(cmd)
    #     while pu.poll() is None:
    #         Logger.info(f'当前进程状态为{pu.poll()},NONE为运行中，0为正常结束，2为子进程不存在')
    #         subprocess.Popen('adb connect ' + device)
    #         subprocess.Popen('adb shell du -sh mnt/')
    #         time.sleep(60 * 5)
    #     Logger.info(f'push文件到{qnx_path}成功')
    #     Logger.info(f'开始复制文件到U盘')
    #     cp = subprocess.Popen(r'adb -s ' + device + ' shell cp -rf ' + qnx_path + '/' + ' ' + remotepath)
    #     while cp.poll() is None:
    #         subprocess.Popen('adb connect ' + device)
    #         time.sleep(60 * 5)
    #     Logger.info(f'复制文件到U盘成功')
    #     Logger.info(f'开始删除{qnx_path}路径文件')
    #     rm = subprocess.Popen(r'adb -s ' + device + ' shell rm' + ' ' + qnx_path)
    #     while rm.poll() is None:
    #         subprocess.Popen('adb connect ' + device)
    #         time.sleep(60 * 5)
    #     Logger.info(f'删除{qnx_path}路径下文件成功')
    #     pu.kill()
    #     cp.kill()
    #     rm.kill()
    #
    #     Logger.info('---------------------------')
    #     Logger.info('U盘升级包准备完成')

    def expect_vison(self):
        """
        生成预期的版本号
        """
        current_date = datetime.now()
        # formatted_date = current_date.strftime("%Y%m%d")[2:]
        # Logger.info(f"formatted_date ={formatted_date}")
        # expect_vison = "GACNE_A19_AVNT_ST_" + formatted_date
        expect_vison = "GACNE_A19_AVNT_ST_240327"
        # Logger.info(f"expect_vison ={expect_vison}")
        self.dd.send_dbtest_info(db_ver="GACNE_A19_AVNT_ST_240307_1631D_D", res=True)
        return expect_vison

    def get_uupfile(self):
        """
        获取U盘升级包
        """
        self.get_file("/home/share/ci_deploy/A19_xinghe/GACNE_A19_AVNT_ST_240307_1631D_D.zip", "E:/pack/GACNE_A19_AVNT_ST_240307_1631D_D.zip")
        self.unzifile("E:/pack/GACNE_A19_AVNT_ST_240307_1631D_D.zip", "E:/")
        self.disconnect()
        # self.connect_devices('12345678')
        self.push_update("/mnt", '/mnt/media_rw/usb0')
        # self.connect_devices('12345678')

    def usb_to_adb(self):
        self.com.ComRead()
        time.sleep(30 * 60)
        self.com.ComToAdb()
        time.sleep(10)

if __name__ == '__main__':
    download = Download()
    # a19test = A19devices()
    # com = ComReadWrite(comport='COM117', combaud='921600')
    # download.get_file("/home/share/ci_deploy/A19_xinghe/GACNE_A19_AVNT_ST_240307_1631D_D.zip", "E:/pack/GACNE_A19_AVNT_ST_240307_1631D_D.zip")
    # download.unzifile("E:/pack/GACNE_A19_AVNT_ST_240307_1631D_D.zip", "E:/")
    # download.disconnect()
    # download.connect_devices('192.168.12.107:5555')
    # download.push_update("/mnt", '/mnt/media_rw/usb0')
    # download.connect_devices('192.168.12.107:5555')
    # a19test.A19UsbUpdata()
    # com.ComRead()
    # time.sleep(30 * 60)
    # com.ComToAdb()
    # time.sleep(10)
    # download.connect_devices('12345678')
    # download.expect_vison()
    download.getDvicesIP('12345678')


