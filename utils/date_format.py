# -*- coding=utf-8 -*-
import datetime
import time


def date_format(day):
    t = ""
    if day == "now":
        t = time.strftime("%Y%m%d%H:%M:%S",time.localtime())
    if day == "day":
        t = time.strftime("%Y-%m-%d",time.localtime())
    if day == "mouth":
        t = time.strftime("%Y%m", time.localtime())
    if day == "now-1":
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t


val = date_format('day') + ' 00:00:00'
print(val )

