# coding=gbk
from hdfs.client import Client
import numpy as np

client = Client("http://hadoop01:50070", root='/')
print(client.list('/'))

filepath = "/user/fzp/add3.txt"

# client.download(filepath, "C:\\Users\\ChuangLan\\Desktop", overwrite=False)
data = np.genfromtxt("C:\\Users\\ChuangLan\\Desktop\\add3.txt",encoding='utf-8',dtype=np.str,delimiter=",")

# with client.read(filepath) as fs:
#     content = fs.read()
#     print(content.decode())
print(data)