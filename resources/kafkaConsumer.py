import json
from kafka3 import KafkaConsumer
from utils.sqlOperate import *
from utils.logger import Logger

logger = Logger(logger="kafkaConsumer").getlog()
consumer = KafkaConsumer('audiolistening_push',bootstrap_servers='192.168.128.93:9092',group_id='autotest1',auto_offset_reset='latest',enable_auto_commit=True)
consumer1 = KafkaConsumer('audiolistening_push',bootstrap_servers='10.54.0.28:9092',group_id='autotest1',auto_offset_reset='latest',enable_auto_commit=True)
consumer2 = KafkaConsumer('audiolistening_push',bootstrap_servers='10.54.0.32:9092',group_id='autotest1',auto_offset_reset='latest',enable_auto_commit=True)

def datapush(value):
    if value['event'] == 'TB_AICALL_CALL_D':
        logger.info("收到通话计费数据：")
        logger.info(value)
        v = []
        for k in value.keys():
            v.append(str(value[k]))
            a = tuple(v)

        sql = "INSERT INTO aicall_call_D "  + \
              " (event,statis_date,start_time,end_time,call_id,entrance_id,task_type,task_id,pd_name,prov_code,call_sor_id," \
              "call_dst_id,inter_number,region_id,suilu_region_id,business_res,business_type,sense_name,sample_id,is_artificial," \
              "is_send_sms,sms_content,route_value,trans_type,panoramic_oss_url,is_gray)  VALUES " + str(a)

    if value['event'] == 'TB_AICALL_INTER_D':
        logger.info("收到轮次计费数据：")
        logger.info(value)
        v = []
        for k in value.keys():
            v.append(str(value[k]))
            a = tuple(v)
        sql = "INSERT INTO aicall_inter_D "  + \
              " (event,statis_date,call_id,entrance_id,pd_name,prov_code,begin_time,finish_time,inaction,outaction,inter_idx," \
              "model_type,commun_id,business_name,flow_type,flow_result_type,crs_result,crs_res_time,is_timeout,is_slient," \
              "is_nomatch,prompt_text,prompt_type,prompt_wav,prompt_txt,rec_oss_url,is_gray)  VALUES " + str(a)

    logger.info(sql)
    m = mysql(read_config('KAFKA','DB_HOST'),read_config('KAFKA','DB_PORT'),read_config('KAFKA','DB_USER'),read_config('KAFKA','DB_PASSWORD'),read_config('KAFKA','DB_DATABASE'))
    m.sqlOperate(sql)

try:
    res = consumer.poll(10)
    consumer.seek_to_end()
    for msg in consumer:
        value = json.loads(msg.value.decode('utf-8'))
        datapush(value)

    res = consumer1.poll(10)
    consumer1.seek_to_end()
    for msg in consumer1:
        value = json.loads(msg.value.decode('utf-8'))
        datapush(value)

    res = consumer2.poll(10)
    consumer2.seek_to_end()
    for msg in consumer2:
        value = json.loads(msg.value.decode('utf-8'))
        datapush(value)

except KeyboardInterrupt:
    pass

finally:
    consumer.close()