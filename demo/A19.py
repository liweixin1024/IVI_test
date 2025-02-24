import os
import time
from demo.Log import Logger
import uiautomator2 as u2
import subprocess
from dingtalk.dingrobot import DingTalkBot

class A19devices():
    def __init__(self, IP="192.168.7.81:5555"):
        self.d = u2.connect(IP)
        self.dt = DingTalkBot()

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

    def A19UsbUpdata(self):
        # A19车型进行U盘升级
        # os.popen("python -m uiautomator2 init").read()
        # if self.d(text="体验模式").exists:
        #     Logger.info("进入体验模式")
        #     self.d(text="体验模式").click()
        # time.sleep(1)
        # if self.d(resourceId="com.gxa.authorize:id/permission_name", text="位置信息").exists:
        #     Logger.info("进行位置信息授权")
        #     self.d(resourceId="com.gxa.authorize:id/confirm_button", text="12个月内允许").click()
        #     time.sleep(3)
        self.d(resourceId="com.gxa.service.systemui:id/car_setting").click()
        Logger.info("进入我的车")
        time.sleep(2)
        self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="系统设置").click()
        Logger.info('进入系统设置')
        time.sleep(3)
        self.d.swipe(0.646, 0.382, 0.605, 0.52, 0.5)
        Logger.info("滑动到时间与日期")
        time.sleep(1)
        if not self.d(text="时间与日期").exists:
            Logger.info('无法进入工程模式')
        Logger.info('点击系统时间进入工程模式')
        time.sleep(1)
        while self.d(resourceId="com.gxatek.cockpit.car.settings:id/current_time_text").exists:
            self.d(resourceId="com.gxatek.cockpit.car.settings:id/current_time_text").click()
        time.sleep(3)
        self.d(resourceId="com.android.engmode:id/btn_title", text="USB升级").click()
        Logger.info('进入USB升级')
        time.sleep(1)
        self.d(resourceId="com.desaysv.ivi.vds.upgrade:id/bt_select_file", text="升级U盘软件包").click()
        Logger.info('点击升级U盘软件包')
        time.sleep(1)
        self.d(resourceId="com.desaysv.ivi.vds.upgrade:id/tv_item", text="/GAC-A02_20240307_SOC.zip").click()
        Logger.info('选择U盘软件包')
        time.sleep(1)
        if self.d(resourceId="com.desaysv.ivi.vds.upgrade:id/tv_remind", text="安装过程中车机将会重启，是否现在安装？").exists:
            self.d(resourceId="com.desaysv.ivi.vds.upgrade:id/btn_confirm", text="确认").click()
        Logger.info('点击确认,开始升级')
        Logger.warn("Start USB upgrade,please wait")

    def a19getlog(self):
        # 获取A19车型版本号和日志
        os.popen("adb -s 1234567 shell logcat -d  > ./A13Ylogcat.txt").read()
        Logger.warn("Importing logs, please wait")
        time.sleep(1)
        Logger.info("Log exported successfully")

    def get_update_res(self):
        if self.d(text="体验模式").exists:
            Logger.info("进入体验模式")
            self.d(text="体验模式").click()
        time.sleep(1)
        if self.d(resourceId="com.gxa.authorize:id/permission_name", text="位置信息").exists:
            Logger.info("进行位置信息授权")
            self.d(resourceId="com.gxa.authorize:id/confirm_button", text="12个月内允许").click()
        time.sleep(3)
        while not self.d(text="升级成功").exists:
            time.sleep(90)
        try:
            self.d(text="确认").click()
        except:
            Logger.info("无法获取升级结果")

    def getDvicesIP(self, device):
        # 获取A19车型IP地址
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
        localpath = "E:/output/usb"
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

    def get_dbversion(self):
        self.process = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(2)
        self.process.stdin.write("getprop|grep -i version.short_name\n")
        self.process.stdin.flush()
        result = self.process.stdout.readline()
        time.sleep(2)
        self.process.kill()
        return result

    def map_activate(self):
        """
        地图激活
        :return:
        """
        #if self.d(resourceId="space.syncore.cockpit.map:id/iv_search_back").exists:
        #    self.d(resourceId="space.syncore.cockpit.map:id/iv_search_back").click()
        if not self.d(resourceId="space.syncore.cockpit.map:id/tv_scale", text="1千米").exists:
            Logger.info("不在地图页面")
            self.d(resourceId="com.gxa.service.systemui:id/home").click()
            time.sleep(1)
            if not self.d(resourceId="space.syncore.cockpit.map:id/tv_scale", text="1千米").exists:
                self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
                Logger.info("点击主页")
                time.sleep(1)
        if self.d(resourceId="space.syncore.cockpit.map:id/iv_search_back").exists:
            self.d(resourceId="space.syncore.cockpit.map:id/iv_search_back").click()
        if self.d(text="手动激活").exists(timeout=5):
            Logger.warn("地图未激活，进行手动激活")
            process = subprocess.Popen("adb shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(2)
            process.stdin.write("setprop sys.vehicle.hardware.map.active.code 00000000000000000XINGHENDA000003\n")
            Logger.info("设置地图手动激活")
            self.d(text="手动激活").click()
            Logger.info("选择手动激活")
            if not self.d(text="4EGSRCPGRBQQH2DBF4EDG9ZX").exists:
                self.d(resourceId="space.syncore.cockpit.map:id/dialog_manual_activation_label_serial_val").set_text("4EGSRCPGRBQQH2DBF4EDG9ZX")
                Logger.info("设置序列号")
            Logger.info("已输入序列号")
            if not self.d(text="2P8DW7BES7CUBXR7M8THVTPY").exists:
                self.d(resourceId="space.syncore.cockpit.map:id/dialog_manual_activation_label_activation_val").set_text(
                "2P8DW7BES7CUBXR7M8THVTPY")
                Logger.info("设置激活号")
            Logger.info("已输入激活号")
            self.d(resourceId="space.syncore.cockpit.map:id/dialog_manual_activation_apply", text="申请激活").click()
            Logger.info("申请激活")
            if self.d(text="手动激活成功").exists:
                Logger.info("手动激活成功")
        else:
            Logger.info("地图已激活")

    def check_version(self):
        """
        版本检查
        """
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/car_setting").click()  # 点击我的车
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="系统设置").click()  # 点击系统设置
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_tab_title", text="系统").click()  # 点击系统
            time.sleep(1)
            actual = self.d(resourceId="com.gxatek.cockpit.car.settings:id/system_upgrade_text").info["text"]
            Logger.info(f"当前版本号为{actual}")
            return actual
        except Exception as e:
            Logger.error(e)

    def connect_wifi(self):
        """
        wifi
        """
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d.xpath(
                '//*[@resource-id="com.gxa.service.systemui:id/state_bar_signal_layout"]/android.widget.FrameLayout[2]').click()
            time.sleep(1)
            if not self.d(resourceId="com.gxa.service.systemui:id/wifi_connect_text",text="可连接网络列表").exists:
                if self.d(resourceId="com.gxa.service.systemui:id/wifi_switcher").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/wifi_switcher").click()
                if self.d.xpath('//*[@content-desc="WLAN|无线网络|Wifi|网络连接::connectpanel_connectpanel_wlan"]/android.widget.TextView[1]').exists:
                    self.d.xpath('//*[@content-desc="WLAN|无线网络|Wifi|网络连接::connectpanel_connectpanel_wlan"]/android.widget.TextView[1]').click()
            if not self.d(resourceId="com.gxa.service.systemui:id/item_wifi_index_active").exists:
                if not self.d(resourceId="com.gxa.service.systemui:id/title", text="智能软件内部").exists:
                    self.d(scrollable=True).scroll.to(resourceId="com.gxa.service.systemui:id/title", text="智能软件内部")
                self.d(resourceId="com.gxa.service.systemui:id/title", text="智能软件内部").click() #选择"智能软件内部"wifi
                time.sleep(1)
                if self.d(resourceId="com.gxa.service.systemui:id/et_input").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/et_input").send_keys("zmrj8888")
                    time.sleep(1)
                    self.d(resourceId="com.gxa.service.systemui:id/btn_positive",text="确定").click()
                time.sleep(1)
            if self.d(resourceId="com.gxa.service.systemui:id/btn_positive").exists:
                Logger.info("当前wifi已连接")
                return True
            elif self.d(resourceId="com.gxa.service.systemui:id/rightImage").exists:
                self.d(resourceId="com.gxa.service.systemui:id/rightImage").click()
                if self.d(resourceId="com.gxa.service.systemui:id/btnDisconnect",text="断开连接").exists:
                    Logger.info("当前wifi已连接")
                    return True
            else:
                Logger.warn("当前wifi未连接")
                return False
                time.sleep(1)
            
        except Exception as e:
            Logger.error(e)
            return False

    def open_iqiyi(self):
        try:
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="爱奇艺").click()
            time.sleep(3)
            if self.d(resourceId="com.qiyi.video.iv:id/ll_home_page_search").exists:
                Logger.info("爱奇艺播放成功")
                return True
            else:
                Logger.warn("爱奇艺播放失败")
                return False
        except Exception as e:
            Logger.error(e)
            return False

    def navigat(self):
        try:
            time.sleep(3)
            if not self.d(resourceId="space.syncore.cockpit.map:id/tv_scale", text="1千米").exists:
                Logger.info("不在地图页面")
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                if not self.d(resourceId="space.syncore.cockpit.map:id/tv_scale", text="1千米").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
                    Logger.info("点击主页")
                    time.sleep(1)
            Logger.info("回到地图页面")
            if self.d(resourceId="com.gxatek.cockpit.launcher:id/mile_hint_text",text="小计里程").exists:
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
            elif self.d(resourceId="com.gxatek.cockpit.launcher:id/setting").exists:
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
            if self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input", text="输入名称").exists(timeout=6):
                self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input", text="输入名称").send_keys(
                    "天府广场")
            else:
                """
                if self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit",text="退出").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit",text="退出").click()
                elif self.d(resourceId="space.syncore.cockpit.map:id/simple_exit",text="退出").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/simple_exit",text="退出").click()
                elif self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").click()
                """
                self.d.click(1237,534)
                self.d.click(1237,534)
                time.sleep(1)
                if self.d.xpath('//android.widget.FrameLayout[1]').exists:
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").click()
                elif self.d(resourceId="space.syncore.cockpit.map:id/simple_exit").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/simple_exit").click()
                if self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/ib_search_btn"]/android.widget.ImageView[1]').exists:
                    self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/ib_search_btn"]/android.widget.ImageView[1]').click()
                elif self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input").click()
                elif self.d(resourceId="space.syncore.cockpit.map:id/ib_search_btn").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/ib_search_btn").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input", text="输入名称").exists:
                    self.d(resourceId="space.syncore.cockpit.map:id/set_suggest_search_input", text="输入名称").send_keys("天府广场")  # 输入框输入地址
            time.sleep(3)
            if self.d.xpath(
                '//*[@resource-id="space.syncore.cockpit.map:id/srv_recycler_view"]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageButton[1]').exists:
                self.d.xpath(
                    '//*[@resource-id="space.syncore.cockpit.map:id/srv_recycler_view"]/android.widget.RelativeLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageButton[1]').click()
            time.sleep(2)
            self.d(resourceId="space.syncore.cockpit.map:id/iv_more_icon",
                        description="第一个详情|第一条详情|第一种详情|第1个详情|第1条详情|第1种详情::Pathplanning_Routedetails1").click()  # 点击"..."
            time.sleep(1)
            self.d(resourceId="space.syncore.cockpit.map:id/tv_similuation_navi", text="模拟导航").click()
            time.sleep(1)
            if self.d(resourceId="space.syncore.cockpit.map:id/speedtype", text="中速").exists(timeout=6):
                time.sleep(1)
                self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit", text="退出").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").exists(timeout=6):
                    self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").click()
                return True
            elif self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit",text="退出").exists(timeout=6):
                self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit",text="退出").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").exists(timeout=6):
                    self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").click()
                return True
            elif self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").exists(timeout=6):
                self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").exists(timeout=6):
                    self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").click()
                return True
            elif self.d(resourceId="space.syncore.cockpit.map:id/simple_exit",text="退出").exists(timeout=6):
                self.d(resourceId="space.syncore.cockpit.map:id/simple_exit",text="退出").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").exists(timeout=6):
                    self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").click()
                return True
            elif self.d(resourceId="space.syncore.cockpit.map:id/stv_road_name").exists(timeout=6):
                self.d(resourceId="space.syncore.cockpit.map:id/tbt_exit",text="退出").click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").exists(timeout=6):
                    self.d(resourceId="space.syncore.cockpit.map:id/route_close",text="关闭").click()
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False

    def online_music(self):
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="昊铂悦听").click()
            time.sleep(1)
            self.d(text="网易云音乐").click()
            time.sleep(5)
            if self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_simple_player_play").exists:
                self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_simple_player_play").click()  # 播放音乐
                if self.d(resourceId="com.iflytek.autofly.mediax:id/btn_dialog_account_cancel").exists(timeout=6):
                    self.d(resourceId="com.iflytek.autofly.mediax:id/btn_dialog_account_cancel").click()
            if self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_playlist_play", description="播放第4个#播放第四个#播第4个#播第四个#放第4个#放第四个#听第4个#听第四个").exists:
                self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_playlist_play", description="播放第4个#播放第四个#播第4个#播第四个#放第4个#放第四个#听第4个#听第四个").click()
            elif self.d(resourceId="com.iflytek.autofly.mediax:id/tv_item_music_playlist_desc", text="2024网易云最火流行歌曲推荐（持更）").exists:
                self.d(resourceId="com.iflytek.autofly.mediax:id/tv_item_music_playlist_desc", text="2024网易云最火流行歌曲推荐（持更）").click()
                time.sleep(1)
                self.d(resourceId="com.iflytek.autofly.mediax:id/tv_media_common_button_text", text="全部播放").click()
            else:
                self.d.xpath('//*[@resource-id="com.iflytek.autofly.mediax:id/rv_online_music_content"]/android.view.ViewGroup[2]/android.widget.FrameLayout[1]/androidx.viewpager.widget.ViewPager[1]/androidx.recyclerview.widget.RecyclerView[1]/androidx.recyclerview.widget.RecyclerView[1]/android.view.ViewGroup[1]/android.widget.FrameLayout[1]').click()
            # 通过不通时间点，显示的歌词相同与否来判断是否在播放音乐
            self.d(text="组件").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").exists:
                result1 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").info["text"]
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_author").exists:
                result1 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_author").info["text"]
            # print(result1)
            time.sleep(10)
            if self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").exists:
                result2 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").info["text"]
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_author").exists:
                result2 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_author").info["text"]
            # print(result2)
            time.sleep(1)
            if self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_simple_player_play").exists:
                self.d(resourceId="com.iflytek.autofly.mediax:id/iv_item_music_simple_player_play").click()  # 停止播放
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/iv_play_state").exists:
                self.d(resourceId="com.gxatek.cockpit.shortcut:id/iv_play_state").click()
            if result1 != result2:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def local_music_display(self):
        "本地音乐显示"
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="昊铂悦听").click()
            time.sleep(1)
            self.d(text="本地音源").click()
            time.sleep(1)
            if self.d(resourceId="com.iflytek.autofly.mediax:id/tv_usb_titles", text="USB1").exists:
                return True
            elif self.d(resourceId="com.iflytek.autofly.mediax:id/tv_usb_titles", text="USB2").exists:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def local_music(self):
        "本地音乐"
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="昊铂悦听").click()
            time.sleep(1)
            self.d(text="本地音源").click()
            time.sleep(1)
            if self.d(resourceId="com.iflytek.autofly.mediax:id/tv_no_content", text="当前U盘内无可播放内容").exists:
                Logger.error("U盘无歌曲或未识别到U盘歌曲")
                return False
            self.d(resourceId="com.iflytek.autofly.mediax:id/tv_lm_play_all", text="播放全部").click()  # 播放全部
            time.sleep(5)
            result1 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").info["text"]
            time.sleep(2)
            result2 = self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_lry").info["text"]
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/iv_play_state").click()  # 停止播放
            if result1 != result2:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def open_close_bluetooth(self):
        "开和关闭蓝牙"
        try:
            open_status = False
            close_status = False
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            if not self.d(text="蓝牙").exists(timeout=6):
                self.d(resourceId="com.gxa.service.systemui:id/signal_bt").click()
            time.sleep(1)
            self.d(text="蓝牙").click()
            time.sleep(1)
            if not self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                if self.d(resourceId="com.gxa.service.systemui:id/switcher").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher").click()
                else:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").click()
                time.sleep(1)
                if self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                    open_status = True
                if self.d(resourceId="com.gxa.service.systemui:id/switcher").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher").click()
                else:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").click()
                time.sleep(1)
                if not self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                    close_status = True
            else:
                if self.d(resourceId="com.gxa.service.systemui:id/switcher").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher").click()
                else:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").click()
                time.sleep(1)
                if self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                    close_status = True
                if self.d(resourceId="com.gxa.service.systemui:id/switcher").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher").click()
                else:
                    self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").click()
                time.sleep(1)
                if not self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                    open_status = True
            if open_status == True and close_status == True:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def connect_bluetooth(self):
        "蓝牙连接"
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            if not self.d(text="蓝牙").exists(timeout=6):
                self.d(resourceId="com.gxa.service.systemui:id/signal_bt").click()
            time.sleep(1)
            self.d(text="蓝牙").click()
            time.sleep(1)
            if not self.d(resourceId="com.gxa.service.systemui:id/title", text="自动连接").exists(timeout=6):
                if self.d(resourceId="com.gxa.service.systemui:id/switcher").exists(timeout=6):
                    self.d(resourceId="com.gxa.service.systemui:id/switcher").click()
                elif self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").exists(timeout=6):
                    self.d(resourceId="com.gxa.service.systemui:id/switcher", description="蓝牙开关::connectpanel_bluetooth_bluetoothSwitch").click()
            time.sleep(10)
            if self.d(resourceId="com.gxa.service.systemui:id/im_detail_toggle").exists:
                self.d(resourceId="com.gxa.service.systemui:id/im_detail_toggle").click()
                time.sleep(1)
                if self.d(resourceId="com.gxa.service.systemui:id/btnDisconnect",text="断开连接").exists:
                    self.d(resourceId="com.gxa.service.systemui:id/btnDisconnect",text="断开连接").click()
                time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/title", text="test").click()
            time.sleep(1)
            if self.d(resourceId="com.gxa.service.systemui:id/btn_positive",text="配对").exists(timeout=6):
                self.d(resourceId="com.gxa.service.systemui:id/btn_positive",text="配对").click()
                time.sleep(1)
            if self.d(resourceId="com.gxa.service.systemui:id/im_detail_toggle").exists(timeout=6):
                self.d(resourceId="com.gxa.service.systemui:id/im_detail_toggle").click()
                return True
                time.sleep(1)
            elif self.d(resourceId="com.gxa.service.systemui:id/btnDisconnect",text="断开连接").exists(timeout=6):
                return True
            elif self.d(resourceId="com.gxa.service.systemui:id/syncPhoneTitle",text="同步电话").exists(timeout=6):
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def laucher(self):
        "laucher启动"
        try:
            map_exist = False
            wallpaper_exist=False
            car_exist=False
            self.d(resourceId="com.gxa.service.systemui:id/home").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.launcher:id/mile_hint_text",text="小计里程").exists or self.d(resourceId="com.gxatek.cockpit.launcher:id/power_hint_text",text="续航里程").exists:
                car_exist=True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                if self.d(resourceId="com.gxatek.cockpit.launcher:id/setting").exists:
                    wallpaper_exist=True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                self.d.click(1237,534)
                self.d.click(1237,534)
                time.sleep(1)
                if self.d.xpath('//android.widget.FrameLayout[1]').exists:
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/tv_scale",text="1千米").exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[2]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/ib_search_btn"]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_home").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_company").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_gas").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_coll").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/ele_img").exists:
                    map_exist = True
            elif self.d(resourceId="com.gxatek.cockpit.launcher:id/setting").exists:
                wallpaper_exist=True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                self.d.click(1237,534)
                self.d.click(1237,534)
                time.sleep(1)
                if self.d.xpath('//android.widget.FrameLayout[1]').exists:
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/tv_scale",text="1千米").exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[2]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/ib_search_btn"]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_home").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_company").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_gas").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_coll").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/ele_img").exists:
                    map_exist = True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                if self.d(resourceId="com.gxatek.cockpit.launcher:id/mile_hint_text",text="小计里程").exists:
                    car_exist=True
                elif self.d(resourceId="com.gxatek.cockpit.launcher:id/car_model_click_view").exists:
                    car_exist=True
                elif self.d(resourceId="com.gxatek.cockpit.launcher:id/power_hint_text",text="续航里程").exists:
                    car_exist=True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
            else:
                self.d.click(1237,534)
                self.d.click(1237,534)
                time.sleep(1)
                if self.d.xpath('//android.widget.FrameLayout[1]').exists:
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                time.sleep(1)
                if self.d(resourceId="space.syncore.cockpit.map:id/tv_scale",text="1千米").exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/fragment_container_layout"]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[2]/android.widget.ImageView[2]').exists:
                    map_exist = True
                elif self.d.xpath('//*[@resource-id="space.syncore.cockpit.map:id/ib_search_btn"]/android.widget.ImageView[1]').exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_home").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_company").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_gas").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/iv_search_result_record_button_coll").exists:
                    map_exist = True
                elif self.d(resourceId="space.syncore.cockpit.map:id/ele_img").exists:
                    map_exist = True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                if self.d(resourceId="com.gxatek.cockpit.launcher:id/mile_hint_text",text="小计里程").exists:
                    car_exist=True
                elif self.d(resourceId="com.gxatek.cockpit.launcher:id/car_model_click_view").exists:
                    car_exist=True
                elif self.d(resourceId="com.gxatek.cockpit.launcher:id/power_hint_text",text="续航里程").exists:
                    car_exist=True
                self.d(resourceId="com.gxa.service.systemui:id/home").click()
                time.sleep(1)
                if self.d(resourceId="com.gxatek.cockpit.launcher:id/setting").exists:
                    wallpaper_exist=True
            if map_exist == True  and car_exist == True and wallpaper_exist==True:
                return True
            else:
                print(map_exist,car_exist,wallpaper_exist)
                return False
        except Exception as e:
            Logger.error(e)
            return False

    def systemui(self):
        "systemUI"
        try:
            status_bar = False
            tool_bar=False
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/signal_bt").click()
            time.sleep(1)
            if self.d(text="蓝牙").exists:
                status_bar = True
            elif self.d(text="网络与热点").exists:
                status_bar = True
            elif self.d(text="Apple CarPlay").exists:
                status_bar = True
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="蓝牙电话").exists:
                tool_bar=True
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="B-CALL").exists:
                tool_bar=True
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="OTA").exists:
                tool_bar=True
            elif self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="应用商店").exists:
                tool_bar=True
            if status_bar == True and tool_bar == True:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
        
    def local_video_display(self):
        "本地视频显示"
        try:
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="图片视频").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.gallery:id/back").exists(timeout=6):
                self.d(resourceId="com.gxatek.cockpit.gallery:id/back").click()
            self.d(text="USB2").click()
            if self.d(text="本机相册").exists:
                return True
            elif self.d(text="USB1").exists:
                return True
            elif self.d(text="USB2").exists:
                return True
            elif self.d(resourceId="com.gxatek.cockpit.gallery:id/title_bar_select_text",text="筛选").exists:
                return True
            elif self.d(resourceId="com.gxatek.cockpit.gallery:id/title_bar_edit").exists:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)

    def local_video(self):
        "本地视频播放"
        try:
            
            "本地视频，保证根目录下有“视频.mp4”视频"
            self.d(resourceId="com.gxa.service.systemui:id/home").click()  # 回到主页
            time.sleep(1)
            self.d(resourceId="com.gxa.service.systemui:id/all_menu").click()  # 点击menu
            time.sleep(1)
            self.d(resourceId="com.gxatek.cockpit.shortcut:id/tv_app_name", text="图片视频").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.gallery:id/back").exists(timeout=6):
                self.d(resourceId="com.gxatek.cockpit.gallery:id/back").click()
            if not self.d(text="USB2").exists:
                self.d.click(1237,534)
                self.d.click(1237,534)
                time.sleep(1)
                if self.d.xpath('//android.widget.FrameLayout[1]').exists:
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                    self.d.xpath('//android.widget.FrameLayout[1]').click()
                self.d(resourceId="com.gxatek.cockpit.gallery:id/back").click() #点击返回
            self.d(text="USB2").click()
            if self.d(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="视频").exists:
                self.d(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="视频").click()
            elif self.d(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="yuebing").exists:
                self.d(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="yuebing").click()
            else:
                self.d(scrollable=True).scroll.to(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="视频")
                self.d(resourceId="com.gxatek.cockpit.gallery:id/img_name", text="视频").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.gallery:id/start").exists(timeout=6):#判断是否有暂停按钮
                self.d.click(1237,534)
                self.d(resourceId="com.gxa.service.systemui:id/app_control_layout").click()
                return True
            elif self.d(resourceId="com.gxa.service.systemui:id/app_control_layout").exists(timeout=6):#判断是否有退出按钮
                self.d.click(1237,534)
                self.d(resourceId="com.gxa.service.systemui:id/app_control_layout").click()
                return True
            elif self.d(resourceId="com.gxatek.cockpit.gallery:id/back").exists(timeout=6):
                if not self.d(resourceId="com.gxatek.cockpit.gallery:id/back").exists(timeout=6):
                    self.d.click(1237,534)
                    self.d(resourceId="com.gxatek.cockpit.gallery:id/back").click()
                return True
            elif self.d(resourceId="com.gxatek.cockpit.gallery:id/bottom_speed",text="倍速").exists(timeout=6):
                if not self.d(resourceId="com.gxatek.cockpit.gallery:id/back").exists(timeout=6):
                    self.d.click(1237,534)
                    self.d(resourceId="com.gxatek.cockpit.gallery:id/back").click()
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
    
    def settings_display(self):
        "系统界面显示"
        try:
            display_status=0
            if not self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="开闭控制").exists:
                self.d(resourceId="com.gxa.service.systemui:id/car_setting").click()
            time.sleep(1)
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="开闭控制").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="开闭控制").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="灯光系统").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="灯光系统").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="智能座舱").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="智能座舱").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="ADiGO智能驾驶").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="ADiGO智能驾驶").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="底盘动力").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="底盘动力").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="车身附件").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="车身附件").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="系统设置").exists:
                if self.d(resourceId="com.gxatek.cockpit.car.settings:id/tv_menu_title", text="系统设置").info["enabled"] == True:#判断按钮是否可点击
                    display_status=display_status+1
            if display_status==7:
                return True
            else:
                return False
        except Exception as e:
            Logger.error(e)
            return False
    
    def adb_screencap(self):
        filename = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        screencap = "adb shell screencap -p /sdcard/" + filename + ".png"
        subprocess.Popen(screencap)
        pull = "adb pull /sdcard/"+filename+".png"+r" C:\Users\Administrator\Desktop\DB_Autotest\output"+"\\"
        subprocess.Popen(pull)
        path = r"C:\Users\Administrator\Desktop\DB_Autotest\output"+"\\"+filename + ".png"
        return path

    def send_report(self,string):
        self.dt.send_dbtest_info(db_ver="GACNE_A19_AVNT_ST_240307_1631D_D", res=string, rep_html="http://192.168.9.35:9999/index.html")

def send_reports(string):
    dt = DingTalkBot()
    dt.send_dbtest_info(db_ver="GACNE_A19_AVNT_ST_240307_1631D_D", res=string, rep_html="http://192.168.9.35:9999/index.html")

if __name__ == '__main__':
    a19 = A19devices()
    a19.online_music()
