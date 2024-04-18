from demo.A19 import A19devices,send_reports
from demo.Download import Download
import uiautomator2 as u2
import pytest
import allure
import time
import os

#a19 = A19devices()
#test = a19.local_video()
#print(test)
class TestIVI:
    def setup_class(self):
        self.a19 = A19devices()
        self.download = Download()
        self.devier = u2.connect("192.168.7.81:5555")
    def teardown_class(self):
        print("后置条件")
    @allure.id("test_01_vison")
    @allure.title("版本检查")
    @allure.description("""
        TestId:
            test_01_vison
        TestTitle:
            版本检查
        TestDescription:
            USB升级完成后检查版本
        TestPrecondition:
            无
        TestStep:
            1、查看设置-系统通用-系统版本
        TestExpectation:
            1、版本升级成功
                """)
    def test_01_vison(self):
        """
        DB版本检查
        """
        #self.download.get_uupfile()
        #self.a19.A19UsbUpdata()
        #self.download.usb_to_adb()
        actual = self.a19.check_version()
        expect = self.download.expect_vison()
        assert expect in actual
    @allure.id("test_02_wifi")
    @allure.title("wifi连接")
    @allure.description("""
        TestId:
            test_02_wifi
        TestTitle:
            wifi连接
        TestDescription:
            wifi连接
        TestPrecondition:
            无
        TestStep:
            1、点击连接菜单,连接wifi
            2、打开爱奇艺播放视频
        TestExpectation:
            1、wifi连接成功
            2、视频播放正常
                """)
    def test_02_wifi(self):
        """
        wifi连接
        """
        self.a19
        result =self.a19.open_iqiyi()
        assert result == True
    @allure.id("test_03_navigat")
    @allure.title("模拟导航")
    @allure.description("""
        TestId:
            test_03_navigat
        TestTitle:
            模拟导航
        TestDescription:
            模拟导航
        TestPrecondition:
            无
        TestStep:
            1、点击连接菜单,连接wifi
            2、开启模拟导航
        TestExpectation:
            1、wifi连接成功
            2、开始模拟导航
                """)
    def test_03_navigat(self):
        """
        模拟导航
        """
        self.a19.map_activate()
        result =self.a19.navigat()
        assert result == True
    @allure.id("test_04_online_emusic")
    @allure.title("音乐播放")
    @allure.description("""
        TestId:
            test_04_online_emusic
        TestTitle:
            音乐播放
        TestDescription:
            音乐播放
        TestPrecondition:
            无
        TestStep:
            1、点击连接菜单,连接wifi
            2、播放音乐
        TestExpectation:
            1、wifi连接成功
            2、开始播放音乐
                """)
    def test_04_online_emusic(self):
        """
        音乐播放
        """
        result = self.a19.online_music()
        assert result == True
    @allure.id("test_05_usbmusic_display")
    @allure.title("本地音乐显示")
    @allure.description("""
        TestId:
            test_05_usbmusic_display
        TestTitle:
            本地音乐显示
        TestDescription:
            本地音乐显示
        TestPrecondition:
            USB2.0连接U盘
        TestStep:
            1、进入本地音乐
        TestExpectation:
            1、本地音乐正常显示
                """)
    def test_05_usbmusic_display(self):
        result = self.a19.local_music_display()
        assert result == True
    @allure.id("test_06_usbmusic")
    @allure.title("播放本地音乐")
    @allure.description("""
        TestId:
            test_06_usbmusic
        TestTitle:
            播放本地音乐
        TestDescription:
            播放本地音乐
        TestPrecondition:
            USB2.0连接U盘
        TestStep:
            1、播放本地音乐
        TestExpectation:
            1、本地音乐正常播放
                """)
    def test_06_usbmusic(self):
        result = self.a19.local_music()
        assert result == True
    @allure.id("test_07_open_close_bluetooth")
    @allure.title("开启关闭蓝牙")
    @allure.description("""
        TestId:
            test_07_open_close_bluetooth
        TestTitle:
            开启关闭蓝牙
        TestDescription:
            开启关闭蓝牙
        TestPrecondition:
            无
        TestStep:
            1、开启蓝牙
            2、关闭蓝牙
        TestExpectation:
            1、蓝牙开启成功
            2、蓝牙关闭成功
                """)
    def test_07_open_close_bluetooth(self):
        result = self.a19.open_close_bluetooth()
        assert result == True
    @allure.id("test_08_connect_bluetooth")
    @allure.title("连接蓝牙")
    @allure.description("""
        TestId:
            test_08_connect_bluetooth
        TestTitle:
            连接蓝牙
        TestDescription:
            连接蓝牙
        TestPrecondition:
            1、周边存在蓝牙名为test,且已经连接过此蓝牙设备
        TestStep:
            1、连接test蓝牙设备
        TestExpectation:
            1、蓝牙连接成功
                """)
    def test_08_connect_bluetooth(self):
        result = self.a19.connect_bluetooth()
        assert result == True
    @allure.id("test_09_laucher")
    @allure.title("laucher启动")
    @allure.description("""
        TestId:
            test_09_laucher
        TestTitle:
            laucher启动
        TestDescription:
            laucher启动
        TestPrecondition:
            无
        TestStep:
            1、查看laucher界面显示
        TestExpectation:
            1、laucher界面显示正常
                """)
    def test_09_laucher(self):
        result = self.a19.laucher()
        assert result == True
    @allure.id("test_10_systemui")
    @allure.title("systemui验证")
    @allure.description("""
        TestId:
            test_10_systemui
        TestTitle:
            systemui验证
        TestDescription:
            systemui验证
        TestPrecondition:
            1、回到主页
        TestStep:
            1、点击状态栏蓝牙图标
            2、点击工具栏allmenu图标
        TestExpectation:
            1、蓝牙图标可点击
            2、显示allmenu界面
                """)
    def test_10_systemui(self):
        result = self.a19.systemui()
        assert result == True
    @allure.id("test_11_usbvideo_display")
    @allure.title("本地视频显示")
    @allure.description("""
        TestId:
            test_11_usbvideo_display
        TestTitle:
            本地视频显示
        TestDescription:
            本地视频显示
        TestPrecondition:
            1、USB2.0连接U盘
        TestStep:
            1、本地视频显示
        TestExpectation:
            1、本地视频界面显示正常
                """)
    def test_11_usbvideo_display(self):
        result = self.a19.local_video_display()
        assert result == True
    @allure.id("test_12_usbvideo")
    @allure.title("播放本地视频")
    @allure.description("""
        TestId:
            test_12_usbvideo
        TestTitle:
            播放本地视频
        TestDescription:
            播放本地视频
        TestPrecondition:
            1、USB2.0连接U盘,且U盘有名字未“视频.mp4”的视频
        TestStep:
            1、播放本地视频
        TestExpectation:
            1、本地视频正常播放
                """)
    def test_12_usbvideo(self):
        result = self.a19.local_video()
        assert result == True
    @allure.id("test_13_settings")
    @allure.title("系统设置")
    @allure.description("""
        TestId:
            test_13_settings
        TestTitle:
            系统设置
        TestDescription:
            系统设置
        TestPrecondition:
            无
        TestStep:
            1、进入系统设置
        TestExpectation:
            1、系统设置显示无异常
                """)
    def test_13_settings(self):
        result = self.a19.settings_display()
        assert result == True

if __name__ == '__main__':
    
    result=pytest.main(["-v", "-s", "main.py::TestIVI", '--alluredir', r'.\reports', '--clean-alluredir'])
    if result == pytest.ExitCode.OK:
        send_reports("PASS")
    else:
        send_reports("FAIL")
    os.system(r'allure serve .\reports -p 9999')
