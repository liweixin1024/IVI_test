import os
from Log import Logger
from configparser import ConfigParser

try:
    conn = ConfigParser()
    file_path = os.path.join(os.path.abspath('.'),'config/config.ini')
    conn.read(file_path)
    if not os.path.exists(file_path):
        Logger.error("Profile does not exist")
    Logger.info("Successfully read configuration file")
except Exception as e:
    Logger.error("Failed to read configuration file:%s"%(e))

remote_img_address = {
    "A13YIP":"",
    "A8EIP":"",
    "A21IP":"",
    "A18VIP":"",
    "A13Yaddress":"",
    "A8Eaddress":"",
    "A21address":"",
    "A18Vaddress":"",
    "username":"",
    "password":"",
}
local_img_address = {
    "A13Yzipfileaddress":"",
    "A8Ezipfileaddress":"",
    "A21zipfileaddress":"",
    "A18Vzipfileaddress":"",
    "A13Yunzipfileaddress":"",
    "A8Eunzipfileaddress":"",
    "A21unzipfileaddress":"",
    "A18Vunzipfileaddress":"",
}
adb_push_address = {
    "A13Yaddress":"",
    "A8Eaddress":"",
    "A21address":"",
    "A18Vaddress":"",
}
com_serial_info = {
    "A13Yport":"",
    "A8Eport":"",
    "A21port":"",
    "A18Vport":"",
    "A13Ybaud":"",
    "A8Ebaud":"",
    "A21baud":"",
    "A18Vbaud":"",
}
car_devices_name = {
    "A13Ydevices":"",
    "A8Edevices":"",
    "A21devices":"",
    "A18Vdevices":"",
}

remote_img_address["A13YIP"] = conn.get('remote_img_address',"A13YIP")
remote_img_address["A8EIP"] = conn.get('remote_img_address',"A8EIP")
remote_img_address["A21IP"] = conn.get('remote_img_address',"A21IP")
remote_img_address["A18VIP"] = conn.get('remote_img_address',"A18VIP")
remote_img_address["A13Yaddress"] = conn.get('remote_img_address',"A13Yaddress")
remote_img_address["A8Eaddress"] = conn.get('remote_img_address',"A8Eaddress")
remote_img_address["A21address"] = conn.get('remote_img_address',"A21address")
remote_img_address["A18Vaddress"] = conn.get('remote_img_address',"A18Vaddress")
remote_img_address["username"] = conn.get('remote_img_address',"username")
remote_img_address["password"] = conn.get('remote_img_address',"password")
local_img_address["A13Yzipfileaddress"] = conn.get('local_img_address',"A13Yzipfileaddress")
local_img_address["A8Ezipfileaddress"] = conn.get('local_img_address',"A8Ezipfileaddress")
local_img_address["A21zipfileaddress"] = conn.get('local_img_address',"A21zipfileaddress")
local_img_address["A18Vzipfileaddress"] = conn.get('local_img_address',"A18Vzipfileaddress")
local_img_address["A18Vunzipfileaddress"] = conn.get('local_img_address',"A18Vunzipfileaddress")
local_img_address["A8Eunzipfileaddress"] = conn.get('local_img_address',"A8Eunzipfileaddress")
local_img_address["A21unzipfileaddress"] = conn.get('local_img_address',"A21unzipfileaddress")
local_img_address["A18Vunzipfileaddress"] = conn.get('local_img_address',"A18Vunzipfileaddress")
adb_push_address["A13Yaddress"] = conn.get('adb_push_address',"A13Yaddress")
adb_push_address["A8Eaddress"] = conn.get('adb_push_address',"A8Eaddress")
adb_push_address["A21address"] = conn.get('adb_push_address',"A21address")
adb_push_address["A18Vaddress"] = conn.get('adb_push_address',"A18Vaddress")
com_serial_info["A13Yport"] = conn.get('com_serial_info',"A13Yport")
com_serial_info["A8Eport"] = conn.get('com_serial_info',"A8Eport")
com_serial_info["A21port"] = conn.get('com_serial_info',"A21port")
com_serial_info["A18Vport"] = conn.get('com_serial_info',"A18Vport")
com_serial_info["A13Ybaud"] = conn.get('com_serial_info',"A13Ybaud")
com_serial_info["A8Ebaud"] = conn.get('com_serial_info',"A8Ebaud")
com_serial_info["A21baud"] = conn.get('com_serial_info',"A21baud")
com_serial_info["A18Vbaud"] = conn.get('com_serial_info',"A18Vbaud")
car_devices_name["A13Ydevices"] = conn.get('car_devices_name',"A13Ydevices")
car_devices_name["A8Edevices"] = conn.get('car_devices_name',"A8Edevices")
car_devices_name["A21devices"] = conn.get('car_devices_name',"A21devices")
car_devices_name["A18Vdevices"] = conn.get('car_devices_name',"A18Vdevices")
Logger.info(remote_img_address)
Logger.info(local_img_address)
Logger.info(adb_push_address)
Logger.info(com_serial_info)
Logger.info(car_devices_name)