from utils import get_params
import  os
from utils import *


filename = 'D:\\ruanjian\pycharm\PBOTinterface\\testcases\datafilter.xls'
cases = get_params(filename,'数据筛选用例')
print(cases)