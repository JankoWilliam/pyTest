# -*- coding: utf-8 -*-
import time
from urllib import parse, request
import hashlib
import json
import pandas as pd
import pymysql


# queryStr = '/place/v2/suggestion?query=上海创蓝文化传播有限公司&region=北京&output=json&ak=nokhtqlDUt46Nqmd0hAhuFKAslxDBN9r'
# url = parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")
#
# req = request.Request(url=url)
# res = request.urlopen(req)
# res = res.read().decode(encoding='utf-8')
#
# json_data = json.loads(res)
# print(json_data['result'][0]['uid'])

def getAddressData(company_name):
    queryStr = '/place/v2/suggestion?query=%s&region=北京&output=json&ak=nokhtqlDUt46Nqmd0hAhuFKAslxDBN9r' % company_name
    url = parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")

    req = request.Request(url=url)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    json_data = json.loads(res)

    final_result = []
    for result in json_data['result']:
        if company_name in result['name']:
            uid = result['uid']
            # print(uid)
            queryStr = '/place/v2/detail?uid=%s&output=json&scope=2&ak=nokhtqlDUt46Nqmd0hAhuFKAslxDBN9r' % uid
            url = parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")

            req = request.Request(url=url)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            json_data = json.loads(res)
            final_result.append(json_data['result'])
    return final_result


csv_data = pd.read_csv('C:\\Users\\ChuangLan\\Desktop\\company_address_acquire02.csv', encoding='gbk')
# print(csv_data['公司名'])

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='baidu_address')

start = time.perf_counter()
n = 0
for company_name in csv_data['公司名']:
    print(company_name)
    results = getAddressData(company_name)
    for result in results:
        # print(result)
        # uid
        uid = result['uid']
        # street_id
        if 'street_id' in result:
            street_id = result['street_id']
        else:
            street_id = None
        # 公司名
        name = result['name']
        # 经度
        location_lng = result['location']['lng']
        # 纬度
        location_lat = result['location']['lat']
        # 地址
        if 'address' in result:
            address = result['address']
        else:
            address = None
        # 省份
        if 'province' in result:
            province = result['province']
        else:
            province = None
        # 城市
        if 'city' in result:
            city = result['city']
        else:
            city = None
        # 地区
        if 'area' in result:
            area = result['area']
        else:
            area = None
        # 电话
        if 'telephone' in result:
            telephone = result['telephone']
        else:
            telephone = None
        try:
            db.ping(reconnect=True)
            sql = 'INSERT INTO company_baidu_address_02(uid,street_id,name,location_lng,location_lat,address,province,city,area,telephone) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            with db.cursor() as cursor:
                if cursor.execute(sql, (
                uid, street_id, name, location_lng, location_lat, address, province, city, area, telephone)):
                    print('successfel')
                    db.commit()
        except:
            print('failed')
            db.rollback()
        n = n + 1
        if n % 100 == 0:
            print("查找公司%s 家，程序运行的时间是：%s秒" % (n, time.perf_counter() - start))
db.close()
