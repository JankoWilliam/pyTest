# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup

User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
headers = {'User-Agent':User_Agent}
r = requests.get('http://seputu.com/',headers=headers)
# print(r.text)
soup = BeautifulSoup(r.text,'html.parser')
content = []
for mulu in  soup.find_all(class_='mulu'):
    h2 = mulu.find('h2')
    if h2!=None:
        h2_title = h2.string
        list = []
        for a in mulu.find(class_='box').find_all('a'):
            href = a.get('href')
            box_title = a.get('title')
            # print(href,box_title)
            list.append({'href':href,'box_title':box_title})
        content.append({'title':h2_title,'content':list})
with open('seputu.json','w') as fp :
    json.dump(content,fp=fp,indent=4)
