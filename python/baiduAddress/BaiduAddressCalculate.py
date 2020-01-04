# -*- coding: utf-8 -*-
import time
from datetime import datetime
from urllib import parse, request
import hashlib
import json
import pandas as pd
import pymysql
import math
import pymysql

aks = {
    'white': 'nokhtqlDUt46Nqmd0hAhuFKAslxDBN9r',  # IP白名单AK fzp
    # 'white': 'biI7A8RpQgMDbVuZfKXOuKk5T6qYNvqh',  # IP白名单AK zy
    # 'white': 'W6scnymCAh3iB8jQAmu2KcTtno01TXcB',  # IP白名单AK lhj
       'sn': 'vYKPbe7qKEW2G6Mpdft7q2eQgolUjkGS'}  # sn方式AK
sk_sn = '1mAsEcD208mSrRCmxIPodhqLid7ZDxe3'  # sn方式SK

# 获取url
def get_url (search, num, ak_type) :
    """
    :param search: 搜索内容，地点、公司名、uid
    :param num: 请求索引，0：地点检索、1：地点提示、2：地点详情检索服务
    :param ak_type: ak类型，white：IP百名单方式、sn：sn校验方式
    :return: 合法的百度地图url请求
    """

    ak = aks[ak_type]
    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=你的ak
    queryStrs = []
    queryStrs.append('/place/v2/search?query=%s&tag=公司&region=全国&city_limit=true&output=json&ak=%s' % (search, ak)) #0 地点检索
    queryStrs.append('/place/v2/suggestion?query=%s&region=全国&output=json&ak=%s' % (search, ak)) #1 地点提示
    queryStrs.append('/place/v2/detail?uid=%s&output=json&scope=2&ak=%s' %(search, ak))  #2 地点详情检索服务,通过uid获取地点详情，这里的search为uid
    queryStrs.append('/geocoding/v3/?address=%s&output=json&ak=%s' %(search, ak)) #3地理编码 ，通过地址获取经纬度信息

    if ak_type == 'sn':
        # sn方式检验
        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = parse.quote(queryStrs[num], safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上yoursk
        rawStr = encodedStr + sk_sn
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
        url = parse.quote("http://api.map.baidu.com" + queryStrs[num] + "&sn=" + sn , safe="/:=&?#+!$,;'@()*[]")
    else:
        # IP白名单方式
        url = parse.quote("http://api.map.baidu.com" + queryStrs[num] , safe="/:=&?#+!$,;'@()*[]")
    return url

# 根据公司名称获取地图经纬度信息
def getAddressData(company_name):
    url = get_url(company_name, 1 , 'white') #1 地点提示，获取uid
    req = request.Request(url=url)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    json_data = json.loads(res)
    final_result = None
    status = json_data['status']
    if status == 0 :    # 数据返回状态必须正常且有数据
        for result in json_data['result']: # 数据返回须包含result
            if len(result['name']) > 5 :   # 数据返回公司名须长度大于5
                if company_name in result['name'] or result['name'] in company_name: # 数据返回公司名称要么全量包含待获取公司名称或被全量包含
                    if 'uid' in result and result['uid'] != '': #
                        uid = result['uid']
                        # print(uid)
                        url = get_url(uid, 2 , 'white') #2 地点详情检索服务,通过uid获取地点详情

                        req = request.Request(url=url)
                        res = request.urlopen(req)
                        res = res.read().decode(encoding='utf-8')
                        json_data = json.loads(res)
                        if json_data['status'] == 0 :
                            final_result = json_data['result']
                            if company_name == result['name'] :
                                break
    elif status == 4 :
        raise Exception("Quota Failure:	配额校验失败",4) # 服务当日调用次数已超限
    elif status == 301 :
        raise Exception("永久配额超限，限制访问",301) # 服务当日调用次数已超限
    elif status == 302 :
        raise Exception("天配额超限，限制访问",302) # 服务当日调用次数已超限
    else :
        return None
    return final_result

# def address_acquire_from_CSV(file_path) :
#     csv_data = pd.read_csv(file_path, encoding='gbk')
#     for index, row in csv_data.iterrows() :
#         # print(row['公司名称'] + "," + str(row['招聘地址']) + "," + str(row['工商地址']))
#         company_name = row['公司名称']
#         zp_address = row['招聘地址']
#         gs_address = row['工商地址']
#         # 按招聘地址获取经纬度信息

# 通过招聘地址\公司名称（无招聘地址）\工商地址（无招聘地址、无法通过公司名称获取） 获取地图经纬度
def address_acquire_from_Mysql() :
    # 1.连接到mysql数据库
    conn_read = pymysql.connect(host='localhost', user='root', password='123456', db='baidu_address', charset='utf8')
    conn_write = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='baidu_address')
    # localhost连接本地数据库 user 用户名 password 密码 db数据库名称 charset 数据库编码格式
    # 2.创建游标对象
    cursor = pymysql.cursors.SSCursor(conn_read)
    # 3.组装sql语句 需要查询的MySQL语句
    sql = "select * from company_address_source_repaired_1 where id = 142946 "
    # 4.执行sql语句
    cursor.execute(sql)

    num = 0
    # try:
    while True:
        try:
            row = cursor.fetchone()
            if not row:
                break
            id = row[0]
            company_name = row[1]
            zp_address = str(row[2]).replace(u'\xa0',u' ')
            gs_address = row[3]
            status = -1
            use_address = ''
            lng = ''
            lat = ''
            # 按招聘地址获取经纬度信息
            if zp_address != None and zp_address.strip() != '' and zp_address.strip() != 'None' and len(zp_address.strip()) > 5:
                url = get_url(zp_address, 3 , 'white')
                req = request.Request(url=url)
                res = request.urlopen(req)
                res = res.read().decode(encoding='utf-8')
                json_data = json.loads(res)
                status = json_data['status']

                if status == 0 :
                    result = json_data['result']
                    lng = result['location']['lng']
                    lat = result['location']['lat']
                    use_address = zp_address
                elif status == 4:
                    raise Exception("Quota Failure:	配额校验失败", 4)  # 服务当日调用次数已超限
                elif status == 301:
                    raise Exception("永久配额超限，限制访问", 301)  # 服务当日调用次数已超限
                elif status == 302:
                    raise Exception("天配额超限，限制访问", 302)  # 服务当日调用次数已超限
            # 按照公司名称获取经纬度信息
            if status!= 0 and company_name != None and company_name.strip()!= '' and company_name.strip()!= 'None' :
                result = getAddressData(company_name)
                if result != None :
                    lng = result['location']['lng']
                    lat = result['location']['lat']
                    use_address = result['address']
                    status = 0
            # 按照工商地址获取经纬度信息
            if status!= 0 and gs_address != None and gs_address.strip()!= '' and gs_address.strip()!= 'None' :
                url = get_url(gs_address, 3, 'white')
                req = request.Request(url=url)
                res = request.urlopen(req)
                res = res.read().decode(encoding='utf-8')
                json_data = json.loads(res)
                status = json_data['status']
                if status == 0:
                    result = json_data['result']
                    lng = result['location']['lng']
                    lat = result['location']['lat']
                    use_address = gs_address
                elif status == 4:
                    raise Exception("Quota Failure:	配额校验失败", 4)  # 服务当日调用次数已超限
                elif status == 301:
                    raise Exception("永久配额超限，限制访问", 301)  # 服务当日调用次数已超限
                elif status == 302:
                    raise Exception("天配额超限，限制访问", 302)  # 服务当日调用次数已超限
            try:
                conn_write.ping(reconnect=True)
                sql = "INSERT INTO company_address_acquired_baidu(company_name,use_address,status,location_lng,location_lat,create_time) values(%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%S'))"
                with conn_write.cursor() as cursor_w:
                    if cursor_w.execute(sql, (
                    company_name, use_address, status, lng, lat , time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))):

                        print('successful:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"  + "  "+ str(status))
                        conn_write.commit()
            except Exception as err: #  数据库错误。
                print('failed inside:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"+str(err))
                conn_write.rollback()
        except ConnectionResetError as err: #  [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            print('failed outside:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"+str(err))
    # except Exception as err :
    #     print("Stop:"+str(id)+","+company_name+";"+"err:"+str(err))

# 通过地址直接获取百度经纬度
def address_acquire_from_Mysql_address() :
    # 1.连接到mysql数据库
    conn_read = pymysql.connect(host='localhost', user='root', password='123456', db='baidu_address', charset='utf8')
    conn_write = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='baidu_address')
    # localhost连接本地数据库 user 用户名 password 密码 db数据库名称 charset 数据库编码格式
    # 2.创建游标对象
    cursor = pymysql.cursors.SSCursor(conn_read)
    # 3.组装sql语句 需要查询的MySQL语句
    sql = "select * from company_address_acquired_gaode_repaired where id > 1 "
    # 4.执行sql语句
    cursor.execute(sql)
    desc = [x[0] for x in cursor.description]
    num = 0
    # try:
    while True:
        try:
            row = cursor.fetchone()
            if not row:
                break
            row = dict(zip(desc,row))
            id = row["id"]
            company_name = row["company_name"]
            use_address = str(row["use_address"]).replace(u'\xa0', u' ')
            status = -1
            lng = ''
            lat = ''
            # 按招聘地址获取经纬度信息
            if use_address != None and use_address.strip() != '' and use_address.strip() != 'None' and len(use_address.strip()) > 5:
                url = get_url(use_address, 3 , 'white')
                req = request.Request(url=url)
                res = request.urlopen(req)
                res = res.read().decode(encoding='utf-8')
                json_data = json.loads(res)
                status = json_data['status']

                if status == 0 :
                    result = json_data['result']
                    lng = result['location']['lng']
                    lat = result['location']['lat']
                elif status == 4:
                    raise Exception("Quota Failure:	配额校验失败", 4)  # 服务当日调用次数已超限
                elif status == 301:
                    raise Exception("永久配额超限，限制访问", 301)  # 服务当日调用次数已超限
                elif status == 302:
                    raise Exception("天配额超限，限制访问", 302)  # 服务当日调用次数已超限
            try:
                conn_write.ping(reconnect=True)
                sql = "INSERT INTO company_address_acquired_baidu(company_name,use_address,status,location_lng,location_lat,create_time) values(%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%S'))"
                with conn_write.cursor() as cursor_w:
                    if cursor_w.execute(sql, (
                    company_name, use_address, status, lng, lat , time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))):

                        print('successful:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"  + "  "+ str(status))
                        conn_write.commit()
            except Exception as err: #  数据库错误。
                print('failed inside:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"+str(err))
                conn_write.rollback()
        except ConnectionResetError as err: #  [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            print('failed outside:' + str(id)+","+company_name.encode('GBK','ignore').decode('GBk')+";"+str(err))
    # except Exception as err :
    #     print("Stop:"+str(id)+","+company_name+";"+"err:"+str(err))

if __name__ == '__main__':
    # url='http://api.map.baidu.com/place/v2/search?query=%E4%B8%8A%E6%B5%B7%E4%BC%97%E5%A4%9A%E7%BE%8E%E7%BD%91%E7%BB%9C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&region=%E4%B8%8A%E6%B5%B7&city_limit=true&output=json&ak=nokhtqlDUt46Nqmd0hAhuFKAslxDBN9r&callback=showLocation'
    # print(getAddressData("上海浦东新区张江郭守敬路498号"))
    # url = get_url("上海浦东新区张江郭守敬路498号", 3 , 'white')
    # req = request.Request(url=url)
    # res = request.urlopen(req)
    # res = res.read()
    # print(res.decode(encoding='utf-8'))
    address_acquire_from_Mysql_address()
    # print(getAddressData("佛山桑托瑞健康科技有限公司"))
    # print(get_url("梅园路77号2408室", 3, 'white'))