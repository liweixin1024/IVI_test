import os
import time
from UsbUpDdata.demo.Log import Logger
import uiautomator2 as u2
import subprocess


class T60Ydevices():

    def getDvicesInfo(self):
        # 获取设备名
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
                    Logger.info("Successfully obtained the device SN code:%s" % (devices))
                    return devices
                else:
                    Logger.warn("Device SN code not obtained, continue to wait")
                    time.sleep(10)
        except Exception as e:
            Logger.error("Failed to get device SN code:%s" % (e))

    def T60YUsbUpdata(self, IP):
        """
        T60Y车型进行U盘升级
        """
        try:
            # os.popen("python -m uiautomator2 init").read()
            d = u2.connect(IP)
            if d(resourceId="android:id/button2", text="关闭").exists:
                d(resourceId="android:id/button1", text="确定").click()
            time.sleep(1)
            if d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").exists:
                d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").click()
                d(resourceId="com.gxatek.cockpit.account:id/tv_experience", text="体验模式").click()
            time.sleep(1)
            d(resourceId="com.gxa.service.systemui:id/all_menu").click()
            Logger.info("进入所有应用")
            time.sleep(1)
            d(text="设置").click()
            Logger.info('点击设置')
            time.sleep(2)
            d(resourceId="com.gxatek.cockpit.settings:id/system_left").click()
            Logger.info('点击系统通用')
            time.sleep(2)
            if not d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").exists:
                d.swipe(1152, 246, 1152, 715, 0.5)
            time.sleep(2)
            Logger.info('点击系统时间进入工程模式')
            while d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").exists:
                d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
            time.sleep(3)
            d(resourceId="android:id/text1", text="USB升级").click()
            Logger.info('进入USB升级')
            time.sleep(2)
            while d(resourceId='com.desaysv.ivi.vds.upgrade:id/version_txt', text='版本信息').exists:
                d(resourceId='com.desaysv.ivi.vds.upgrade:id/version_txt', text='版本信息').click()
            Logger.info('点击版本信息，进入刷机设置项')
            time.sleep(2)
            d(resourceId='com.desaysv.ivi.vds.upgrade:id/check_repeat', text='防止重复刷机').click()
            Logger.info('取消勾选防重复刷机选项')
            time.sleep(2)
            d(resourceId='com.desaysv.ivi.vds.upgrade:id/check_error', text='启用防刷错机制').click()
            Logger.info('取消勾选防刷错机制')
            time.sleep(2)
            d(resourceId='com.desaysv.ivi.vds.upgrade:id/img_back').click()
            Logger.info('返回USB升级界面')
            time.sleep(2)
            d(resourceId="com.desaysv.ivi.vds.upgrade:id/bt_select_file", text='升级U盘软件包').click()
            Logger.info('点击升级U盘软件包')
            time.sleep(2)
            d(resourceId="com.desaysv.ivi.vds.upgrade:id/iv_icon").click()
            Logger.info('选择U盘软件包升级')
            time.sleep(2)
            d(resourceId="com.desaysv.ivi.vds.upgrade:id/btn_confirm", text="确认").click()
            Logger.info('点击确认,开始升级')
            Logger.warn("Start USB upgrade,please wait")
        except Exception as e:
            Logger.error("Failed to enter the upgrade process:%s" % (e))

    def T60YGetVersionAndLog(self, IP):
        """
        获取T60Y车型版本号和日志
        """
        try:
            d = u2.connect(IP)
            if d(resourceId="android:id/button2", text="关闭").exists:
                d(resourceId="android:id/button1", text="确定").click()
            time.sleep(1)
            if d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").exists:
                d(resourceId="com.gxatek.cockpit.launcher:id/tv_agree", text="同意").click()
                d(resourceId="com.gxatek.cockpit.account:id/tv_experience", text="体验模式").click()
            time.sleep(1)
            d(resourceId="com.gxa.service.systemui:id/all_menu").click()
            Logger.info("进入所有应用")
            time.sleep(1)
            d(text="设置").click()
            Logger.info('点击设置')
            time.sleep(2)
            d(resourceId="com.gxatek.cockpit.settings:id/system_left").click()
            Logger.info('点击系统通用')
            time.sleep(2)
            if not d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").exists:
                d.swipe(1152, 246, 1152, 715, 0.5)
            time.sleep(2)
            Logger.info('点击系统时间进入工程模式')
            while d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").exists:
                d(resourceId="com.gxatek.cockpit.settings:id/current_time_text").click()
            time.sleep(3)
            d(resourceId="android:id/text1", text="USB升级").click()
            Logger.info('进入USB升级')
            time.sleep(2)
            version = d(resourceId="com.desaysv.ivi.vds.upgrade:id/tv_soc_version").get_text()
            Logger.info(f'获取版本信息,当前SOC版本为{version}')
            Logger.info(
                "Successfully obtained the version information. The version is: %s , starting to export the log" % (
                    version))
            # os.popen("adb -s 1234567 shell logcat -d  > ./A13Ylogcat.txt").read()
            # Logger.info("Importing logs, please wait")
            # time.sleep(1)
            # Logger.info("Log exported successfully")
        except Exception as e:
            Logger.error("Failed to enter the upgrade process:%s" % e)

    def getDvicesIP(self, device):
        """
        获取T60Y车型IP地址
        """
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
            return devicesname
        except Exception as e:
            Logger.error("IP acquisition failed:%s" % e)

    def push_update(self, device, qnx_path, remotepath):
        """
        从本地push升级包到U盘
        :param device: 设备ip，例如："192.168.12.157:5555"
        :param qnx_path: 复制文件的路径、即升级包push到qnx所在路径，例如：'/mnt/，建议qnx端放在/mnt目录下，其他目录的空间可能不够
        :param remotepath: 目标地址，升级包拷贝到U盘的地址，例如：'/mnt/media_rw/usb0/A13Y_AVNT_Update/'
        author: lulei
        """
        localpath = "E:/output/usb/"
        zip_file = os.listdir(localpath)
        for i in zip_file:
            cmd = 'adb -s ' + device + r' push ' + localpath + i + " " + qnx_path
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
            k = 0
            while cp.poll() is None:
                subprocess.Popen('adb connect ' + device)
                time.sleep(1 + k)
                k += 1
            Logger.info(f'复制文件{i}到U盘成功')
            Logger.info(f'开始删除{qnx_path}路径下{i}文件')
            rm = subprocess.Popen(r'adb -s ' + device + ' shell rm' + ' ' + qnx_path + '/' + i)
            z = 0
            while rm.poll() is None:
                subprocess.Popen('adb connect ' + device)
                time.sleep(1 + z)
                z += 1
            Logger.info(f'删除{qnx_path}路径下{i}文件成功')
            pu.kill()
            cp.kill()
            rm.kill()

        Logger.info('---------------------------')
        Logger.info('U盘升级包准备完成')


if __name__ == '__main__':
    t60y = T60Ydevices()
    t60y.T60YUsbUpdata()
