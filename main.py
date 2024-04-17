from demo.A19 import A19devices,send_reports
from demo.Download import Download
import uiautomator2 as u2
import pytest
import allure
import time
import os

#a19 = A19devices()
#a19.navigat()

class TestIVI:
    def setup_class(self):
        self.a19 = A19devices()
        self.download = Download()
        self.devier = u2.connect("12345678")

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
        self.a19.connect_wifi()
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
    @allure.id("test_05_bluetooth")
    @allure.title("蓝牙连接")
    @allure.description("""
        TestId:
            test_05_bluetooth
        TestTitle:
            蓝牙连接
        TestDescription:
            蓝牙连接
        TestPrecondition:
            无
        TestStep:
            1、连接蓝牙
        TestExpectation:
            1、蓝牙连接成功
                """)
    def test_05_bluetooth(self):
        result = self.a19.connect_bluetooth()
        assert result == True

if __name__ == '__main__':
    result=pytest.main(["-v", "-s", "main.py::TestIVI", '--alluredir', r'.\reports', '--clean-alluredir'])
    if result == pytest.ExitCode.OK:
        send_reports("PASS")
    else:
        send_reports("FAIL")
    os.system(r'allure serve .\reports -p 9999')
