from DB_Autotest.demo.A19 import A19devices
from DB_Autotest.demo.Download import Download
import uiautomator2 as u2
import pytest
import allure
import time
import os


class TestIVI:
    def setup_class(self):
        self.a19 = A19devices()
        self.download = Download()
        self.devier = u2.connect("12345678")

    def teardown_class(self):
        print("后置条件")

    def test_01_vison(self):
        """
        DB版本检查
        """
        # self.download.get_uupfile()
        self.a19.A19UsbUpdata()
        self.download.usb_to_adb()
        actual = self.a19.check_version()
        expect = self.download.expect_vison()
        assert expect in actual

    def test_02_wifi(self):
        """
        wifi连接
        """
        self.a19.connect_wifi()
        self.a19.open_iqiyi()
        assert True


    def test_03_navigat(self):
        """
        模拟导航
        """
        self.a19.map_activate()
        self.a19.navigat()
        assert True

    def test_04_onlin_emusic(self):
        """
        在线音乐
        """
        self.a19.online_music()
        assert True



if __name__ == '__main__':
    pytest.main(["-v", "-s", "main.py::TestIVI", '--alluredir', r'.\reports', '--clean-alluredir'])
    os.system(r'allure serve .\reports')
