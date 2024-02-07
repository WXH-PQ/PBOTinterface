from utils.readconfig import read_config
import sys
sys.path.append('../')
dic = {'event': 'TB_AICALL_CALL_D', 'statis_date': '20231206', 'start_time': 1701850375000, 'end_time': 1701851157000,
       'call_id': 'b3112c26-87d1-40ae-97fe-c0ee29e31c46', 'entrance_id': '098', 'task_type': 2, 'task_id': '1',
       'pd_name': 'pq', 'prov_code': '100', 'call_sor_id': '10086', 'call_dst_id': '15037616713', 'inter_number': 13,
       'region_id': 'sc', 'suilu_region_id': 'sc', 'business_res': '1', 'business_type': 1, 'sense_name': '098',
       'sample_id': '1', 'is_artificial': '0', 'is_send_sms': '1',
       'sms_content': '【xx淘宝店】尊敬的xx，值xx当天，所有商品8折优惠，凡是消费的超过xx客户即可凭小票到一楼服务台免费抽奖一次，'
                      'xx、xx等礼品等你来拿！回T退订尊敬的xx，值xx当天，所有商品8折优惠，凡是消费的超过xx客户即可凭小票到一楼服务台免费抽奖一次，xx、xx等礼品等你来拿！'
                      '回T退订尊敬的xx，值xx当天，所有商品8折优惠，凡是消费的超过xx客户即可凭小票到一楼服务台免费抽奖一次，xx、xx等礼品等你来拿！回T退订',
       'route_value': '', 'trans_type': '', 'panoramic_oss_url': '', 'is_gray': 0}

keys = []
v = []

for k in  dic.keys():
    keys.append(k)
    v.append(str(dic[k]))
    a = tuple(v)

print(keys)
print(a)
sql = "INSERT INTO  database "  + \
               " (event,statis_date,start_time,end_time,call_id,entrance_id,task_type,task_id,pd_name,prov_code,call_sor_id," \
              "call_dst_id,inter_number,region_id,suilu_region_id,business_res,business_type,sense_name,sample_id,is_artificial," \
           "is_send_sms,sms_content,route_value,trans_type,panoramic_oss_url,is_gray)  VALUES " + str(a)

print(sql)
