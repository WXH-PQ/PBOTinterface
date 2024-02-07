import logging
import  os
import datetime
class Logger:
    def __init__(self,logger):

        # 创建日志对象，日志名称取logger参数的值
        self.logger = logging.getLogger(logger)
        if not self.logger.handlers:
            # 设置日志的级别
            # debug:debug级输出
            # info：info 级输出，重要信息
            # warning：warning级输出，与warn相同，警告信息
            # error：error级输出，错误信息
            # critical ：critical级输出，严重错误信息
            self.logger.setLevel(logging.DEBUG)

            # 创建一个handler写入文件
            fh = logging.FileHandler(self.log_file(), encoding='utf-8')
            fh.setLevel(logging.INFO)

            # 创建一个handler输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义输出的格式
            formatter = logging.Formatter(self.fmt())
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 添加到handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def log_file(self):
        '''日志目录'''
        current_dir = os.getcwd()
        log_dir = os.path.join(os.path.dirname(current_dir), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir,'{}.log'.format(datetime.datetime.now().strftime("%Y%m%d")))

    def fmt(self):
        return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger(logger="BasePage").getlog()
    logger.info("hello")