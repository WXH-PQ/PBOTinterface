import time
import uuid
import sys
from time import sleep

sys.path.append('../')
from resources.interfaces import reportforms, interactive
from utils.excelOperate import get_params
from utils.logger import Logger
from utils.date_format import date_format
from  utils.sqlOperate import mysql
import os
from utils.readconfig import read_config
import allure
import pytest

def get_simplify_report():
    # 获取当天的精简报表内容
    day = date_format('day')
    mouth = date_format('mouth')
    response = reportforms(day,mouth)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(response)
    # 将报表接口数据转化为list
    l = list(response.split("\n"))

    #定义实际结果的list,list里面存放和期望结果一样结构的词典case
    case_simplify_actual = []
    # 切分表头
    ll = list(list(l[0].split(",")))
    # 除了第一个是表头信息，剩余的遍历解析成词典
    for i in range(1,len(l)-1):
          dic = {}
          l3 = list(l[i].split(","))
          for j in range(0,len(l3)):
                key = ll[j].strip("\r")
                dic[key] = l3[j].strip("\t").strip("\t\r")
          case_simplify_actual.append(dic)
    return case_simplify_actual

logger = Logger(logger="Reportforms").getlog()
current_dir = os.getcwd()
filename = os.path.join(os.path.dirname(current_dir), 'testcases',read_config("CASE_NAME","reportforms"))
# 获取期望精简报表结果
case_simplify = get_params(filename,'精简报表')
# 获取实际精简报表结果
#case_simplify_actual = get_simplify_report()
UUID = str(uuid.uuid4())



@allure.feature("报表内容")
class Testreportforms:
    @pytest.fixture(scope='module',autouse=True)
    def setup_class(self):
        logger.info("报表导出模块测试开始")
        logger.info("检查当日是否已有数据，如果有则清除")
        sql = "SELECT COUNT(*) from al_job_" + date_format('mouth') + " WHERE start_time > '" + date_format('day') + " 00:00:00'; "
        m = mysql(read_config('MYSQL','DB_HOST'),read_config('MYSQL','DB_PORT'),read_config('MYSQL','DB_USER'),read_config('MYSQL','DB_PASSWORD'),read_config('MYSQL','AI_JOB_DATABASE'))
        result = m.sqlOperate(sql)
        if result[0]['COUNT(*)'] != 0:
            # 有需要清理的数据
            logger.info("清理旧数据")
            m2 = mysql(read_config('MYSQL','DB_HOST'),read_config('MYSQL','DB_PORT'),read_config('MYSQL','DB_USER'),read_config('MYSQL','DB_PASSWORD'),read_config('MYSQL','AI_JOB_DATABASE'))
            sql2 = "DELETE  from al_job_" + date_format('mouth') + " WHERE start_time > '" + date_format('day') + " 00:00:00'; "
            m2.sqlDelete(sql2)

        logger.info("产生测试数据")
        case = get_params(filename,'交互用例')
        for i in case:
            i['call_id'] = i['call_id'] + UUID
            interactive(i)
        logger.info("产生测试数据完成")
        time.sleep(5)

        yield
        logger.info("报表导出模块测试结束")

    @allure.title("精简报表导出内容正确")
    @pytest.mark.parametrize('case',[(case_simplify)])
    def est_001(self,case):
        # 获取实际报表内容
        case_actual = get_simplify_report()
        # case 是精简报表的期望数据，每行为一个case
        # 修改统计日期为当天
        for i in range(0,len(case)):
            case[i]['统计日期'] = str(date_format('day'))
            case[i]['通话ID'] = case[i]['通话ID'] + UUID
            logger.info("期望报表内容")
            logger.info(case[i])
            logger.info("实际报表内容")
            logger.info(case_actual[i])

            for key in  case[i].keys():
                if key == '外呼时间' or key == '接听时间' or key == '挂机时间' or key == '通话时长':
                    assert case_actual[i][key] != ''
                else:
                    assert case_actual[i][key] == case[i][key]