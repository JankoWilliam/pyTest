# -*- coding:utf-8*-
import os
import os.path
import time
time1=time.time()
##########################合并同一个文件夹下多个txt################
def MergeTxt(filepath,outfile):
  k = open(outfile, 'a+')
  for parent, dirnames, filenames in os.walk(filepath):
    for filepath in filenames:
      txtPath = os.path.join(parent, filepath) # txtpath就是所有文件夹的路径
      if os.path.splitext(txtPath)[1] == ".txt": #判断是否是txt文件
          f = open(txtPath, encoding='gbk')
          ##########换行写入##################
          print(txtPath)
          k.write(f.read()+"\n")
  k.close()
  print ("finished")
if __name__ == '__main__':
  filepath="C:\\002_chuanglan\\000_data\\mobile_20190904\\mobile\data"
  outfile="C:\\002_chuanglan\\000_data\\mobile_20190904\\mobile.txt"
  MergeTxt(filepath,outfile)
  time2 = time.time()
  print (u'总共耗时：' + str(time2 - time1) + 's')