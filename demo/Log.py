import os
import time
import logging

class Log:

    def __init__(self):
        # 第一步，创建一个logger
        logfilename = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        self.logger = logging.getLogger(logfilename)  # file_name为多个logger的区分唯一性
        self.logger.setLevel(logging.DEBUG)  # Log等级总开关
        # 如果已经有handler，则用追加模式，否则直接覆盖
        mode = 'a' if self.logger.handlers else 'w'
        # 第二步，创建handler，用于写入日志文件和屏幕输出
        #log_path = os.getcwd() + '/'
        logfile = 'C:/Users/Administrator/Desktop/DB_Autotest/log/' + logfilename + '.log'
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
