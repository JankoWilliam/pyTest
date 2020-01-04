# -*- coding: utf-8 -*-
import time
from urllib import parse, request
import hashlib
import json
import pymysql

key = "c6819a2ce5b667f364e8ef732d42f9c3"


# 获取url
def get_url(search, num):
    """
    :param search: 搜索内容，地点、公司名、uid
    :param num: 请求索引，0：公司名称搜索、1：地理编码 ，通过地址获取经纬度信息地点详情检索服务
    :return: 合法的高德地图url请求
    """

    # 以get请求为例http://restapi.amap.com/v3/geocode/geo?key=您的key&address=深圳市福田区深南中路1002号新闻大厦1506
    queryStrs = []
    queryStrs.append('/v3/place/text?key=%s&keywords=%s&types=公司&offset=20&page=1&extensions=all' % (key , search))  # 0 公司名称搜索
    queryStrs.append('/v3/geocode/geo?key=%s&address=%s' % (key , search))  # 1 地理编码 ，通过地址获取经纬度信息

    return parse.quote("http://restapi.amap.com" + queryStrs[num], safe="/:=&?#+!$,;'@()*[]")

# 获取request请求json格式数据
def get_request_json_data(url):
    req = request.Request(url=url)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    json_data = json.loads(res)
    return json_data

# 挑选结果最优项1
def gaode_geocodes_choose_best(address, json_data):
    result = None
    for geocode in json_data['geocodes']:
        if len(geocode['formatted_address']) > 5:  # 数据返回地点长度大于5
            # if address in geocode['formatted_address'] or geocode['formatted_address'] in address:  # 数据返回公司名称要么全量包含待获取公司名称或被全量包含
            result = geocode
            if address == geocode['formatted_address']:
                break
    return result

# 挑选结果最优项2
def gaode_pois_choose_best(company, json_data):
    result = None
    for poi in json_data['pois']:
        if len(poi['name']) > 5:  # 数据返回公司名称长度大于5
            if company in poi['name'] or poi['name'] in company:  # 数据返回公司名称要么全量包含待获取公司名称或被全量包含
                result = poi
                if company == poi['name']:
                    break
    return result


# def address_acquire_from_CSV(file_path) :
#     csv_data = pd.read_csv(file_path, encoding='gbk')
#     for index, row in csv_data.iterrows() :
#         # print(row['公司名称'] + "," + str(row['招聘地址']) + "," + str(row['工商地址']))
#         company_name = row['公司名称']
#         zp_address = row['招聘地址']
#         gs_address = row['工商地址']
#         # 按招聘地址获取经纬度信息

# 通过招聘地址\公司名称（无招聘地址）\工商地址（无招聘地址、无法通过公司名称获取） 获取地图经纬度
def address_acquire_from_Mysql():
    # 1.连接到mysql数据库
    conn_read = pymysql.connect(host='localhost', user='root', password='123456', db='baidu_address', charset='utf8')
    conn_write = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='baidu_address')
    # localhost连接本地数据库 user 用户名 password 密码 db数据库名称 charset 数据库编码格式
    # 2.创建游标对象
    cursor = pymysql.cursors.SSCursor(conn_read)
    # 3.组装sql语句 需要查询的MySQL语句
    sql = "select * from company_address_source_repaired_1 where id = 2157 "
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
            zp_address = str(row["zp_address"]).replace(u'\xa0', u' ')
            gs_address = row["gs_address"]
            status = -1
            use_address = ''
            lng = ''
            lat = ''
            # 按招聘地址获取经纬度信息
            if zp_address is not None and zp_address.strip() != '' and zp_address.strip() != 'None' and len(
                    zp_address.strip()) > 5:
                url = get_url(zp_address, 1)
                json_data = get_request_json_data(url)
                # status = json_data['status']
                infocode = json_data['infocode']
                if infocode == '10000' and json_data['status'] == '1':  # 状态未1，正常
                    if 'count' in json_data and int(json_data['count']) > 0:
                        result = gaode_geocodes_choose_best(zp_address, json_data)
                        if result is not None:
                            lng = str(result['location']).split(",")[0]
                            lat = str(result['location']).split(",")[1]
                            use_address = zp_address
                            status = '1'
                elif infocode == '10001':
                    raise Exception("key不正确或过期", 10001)
                elif infocode == '10003':
                    raise Exception("访问已超出日访问量", 10003)
                elif infocode == '10004':
                    raise Exception("单位时间内访问过于频繁", 10004)
            # 按照公司名称获取经纬度信息
            if status != '1' and company_name is not None and company_name.strip() != '' and company_name.strip() != 'None':
                url = get_url(company_name, 0)
                json_data = get_request_json_data(url)
                # status = json_data['status']
                infocode = json_data['infocode']
                if infocode == '10000' and json_data['status'] == '1':  # 状态未1，正常
                    if 'count' in json_data and int(json_data['count']) > 0:
                        result = gaode_pois_choose_best(company_name, json_data)
                        if result is not None and str(result['address']) != "[]" :
                            lng = str(result['location']).split(",")[0]
                            lat = str(result['location']).split(",")[1]
                            use_address = result['pname']+result['cityname']+result['adname']+str(result['address'])
                            status = '1'

                elif infocode == '10001':
                    raise Exception("key不正确或过期", 10001)
                elif infocode == '10003':
                    raise Exception("访问已超出日访问量", 10003)
                elif infocode == '10004':
                    raise Exception("单位时间内访问过于频繁", 10004)
            # 按照工商地址获取经纬度信息
            if status != '1' and gs_address is not None and gs_address.strip() != '' and gs_address.strip() != 'None':
                url = get_url(gs_address, 1)
                print(url)
                json_data = get_request_json_data(url)
                infocode = json_data['infocode']
                # status = json_data['status']
                use_address = gs_address
                if infocode == '10000' and json_data['status'] == '1':  # 状态未1，正常
                    if 'count' in json_data and int(json_data['count']) > 0:
                        result = gaode_geocodes_choose_best(zp_address, json_data)
                        if result is not None:
                            lng = str(result['location']).split(",")[0]
                            lat = str(result['location']).split(",")[1]
                            # use_address = gs_address
                            use_address = result['formatted_address']
                        else :
                            status = -1
                    else:
                        status = -1
                elif infocode == '10001':
                    raise Exception("key不正确或过期", 10001)
                elif infocode == '10003':
                    raise Exception("访问已超出日访问量", 10003)
                elif infocode == '10004':
                    raise Exception("单位时间内访问过于频繁", 10004)
            try:
                conn_write.ping(reconnect=True)
                sql = "INSERT INTO company_address_acquired_gaode_repaired(company_name,use_address,status,location_lng," \
                      "location_lat,create_time) values(%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%S')) "
                with conn_write.cursor() as cursor_w:
                    # if cursor_w.execute(sql, (
                    #         company_name, use_address, status, lng, lat,
                    #         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))):
                    #     conn_write.commit()
                        print('successful:' + str(id) + "," + company_name+ ","  + use_address + "," + lng + "," + lat + ";" + "  " + str(status))
            except Exception as err:  # 数据库错误。
                print('failed:' + str(id) + "," + company_name + ";" + str(err))
                conn_write.rollback()
        except ConnectionResetError as err:  # [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            print('failed:' + str(id) + "," + company_name + ";" + str(err))
    # except Exception as err :
    #     print("Stop:"+str(id)+","+company_name+";"+"err:"+str(err))

# 通过百度地图获取的地址直接获取高德经纬度
def address_acquire_from_Mysql_baiduaddress():
    # 1.连接到mysql数据库
    conn_read = pymysql.connect(host='localhost', user='root', password='123456', db='baidu_address', charset='utf8')
    conn_write = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='baidu_address')
    # localhost连接本地数据库 user 用户名 password 密码 db数据库名称 charset 数据库编码格式
    # 2.创建游标对象
    cursor = pymysql.cursors.SSCursor(conn_read)
    # 3.组装sql语句 需要查询的MySQL语句
    sql = "select * from company_address_acquired_baidu_repaired where id > 0 "
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
            # 按百度地址获取经纬度信息
            if use_address is not None and use_address.strip() != '' and use_address.strip() != 'None' and len(use_address.strip()) > 5:
                url = get_url(use_address, 1)
                json_data = get_request_json_data(url)
                status = json_data['status']
                infocode = json_data['infocode']
                if infocode == '10000' and status == '1':  # 状态未1，正常
                    if 'count' in json_data and int(json_data['count']) > 0:
                        result = gaode_geocodes_choose_best(use_address, json_data)
                        if result is not None:
                            lng = str(result['location']).split(",")[0]
                            lat = str(result['location']).split(",")[1]
                            # use_address = zp_address
                        else :
                            status = -1
                elif infocode == '10001':
                    raise Exception("key不正确或过期", 10001)
                elif infocode == '10003':
                    raise Exception("访问已超出日访问量", 10003)
                elif infocode == '10004':
                    raise Exception("单位时间内访问过于频繁", 10004)
            try:
                conn_write.ping(reconnect=True)
                sql = "INSERT INTO company_address_acquired_gaode_distinct(company_name,use_address,status,location_lng," \
                      "location_lat,create_time) values(%s,%s,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%S')) "
                with conn_write.cursor() as cursor_w:
                    if cursor_w.execute(sql, (
                            company_name, use_address, status, lng, lat,
                            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))):
                        print('successful:' + str(id) + "," + company_name + ";" + "  " + str(status))
                        conn_write.commit()
            except Exception as err:  # 数据库错误。
                print('failed:' + str(id) + "," + company_name + ";" + str(err))
                conn_write.rollback()
        except ConnectionResetError as err:  # [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            print('failed:' + str(id) + "," + company_name + ";" + str(err))
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
    # print(getAddressData("佛山桑托瑞健康科技有限公司"))
    # print(get_url("梅园路77号2408室", 3, 'white'))
    address_acquire_from_Mysql_baiduaddress()
    pass
