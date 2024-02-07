import pymysql
from utils.logger import Logger
from utils.readconfig import read_config

logger = Logger(logger="sqlOperate").getlog()

class mysql():
    def __init__(self,host,port,user,password,database):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = database
        # 打开数据库链接
        self.conn = pymysql.connect(host=self.host,port=int(self.port),user=user,password=self.password,database=self.database,charset='utf8mb4',autocommit=True,cursorclass=pymysql.cursors.DictCursor)
        # 创建数据库光标
        self.cursor = self.conn.cursor()

    def sqlOperate(self,sql):
        # 执行查询sql语句
        try:
            self.cursor.execute(sql)
            logger.info("数据库操作成功")
            # 获取所有记录列表
            results = self.cursor.fetchall()

            # 发生错误时间回滚
            self.conn.rollback()
            # 关闭数据库链接
            self.conn.close()
            return results

        except Exception as e:
            logger.error("数据库执行失败，失败原因：")
            logger.error(e)


    def sqlDelete(self,sql):
        # 执行删除sql
        try:
            self.cursor.execute(sql)
            logger.info("数据库操作成功")
            # 发生错误时间回滚
            self.conn.rollback()
            # 关闭数据库链接
            self.conn.close()

        except Exception as e:
            logger.error("数据库执行失败，失败原因：")
            logger.error(e)




