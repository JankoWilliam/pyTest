from pyspark import SparkConf, SparkContext
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

conf = SparkConf().setAppName("int").setMaster("local[*]")
sc = SparkContext(conf=conf)
user_data = sc.textFile("C:\\Users\\ChuangLan\\Desktop\\ml-100k\\u.user")
# 初步看一样数据的样子
print(user_data.first())
user_fields = user_data.map(lambda line: line.split('|'))
num_user = user_fields.map(lambda field: field[0]).count()
num_gender = user_fields.map(lambda field: field[2]).distinct().count()  # distinct用于去重，count()用于计数
num_occupation = user_fields.map(lambda field: field[3]).distinct().count()
num_zipcode = user_fields.map(lambda field: field[4]).distinct().count()
print("共有用户：%d户,性别：%d类,职业%d类,邮编：%d种" % (num_user, num_gender, num_occupation, num_zipcode))

ages = user_fields.map(lambda field: field[1])  # 返回RDD的所有元素，方便后面对age进行统计,之后就可以利用单机的一切函数了
# ages.foreach(lambda field: print(field))
# ax = sns.distplot(ages.collect())
# plt.show()

# occupations = user_fields.map(lambda field: field[3]).collect()  # 当数据不大时，我们可以用这种方法将所有元素收集起来
# ax = sns.countplot(x=occupations)
# plt.show()

occupation_count = user_fields.map(
    lambda fields: (fields[3], 1))  # 这一步先每出现一次职业就计一次数，只要对这些数字求和就可以知道各个职业出现了多少次，即得到各职业的频率分布
occupation_counts = occupation_count.reduceByKey(lambda x, y: x + y)  # 利用reduceByKey()函数对各条数据进行归并，达到统计目的
occupation_counts = occupation_counts.collect()  # 此时不用担心数据量的问题，经过前面的shuffle过程，此时数据已经被归为有限的数目了，从前面对职业个数的统计知道，现在数据只有21对，前面是职业名称，后面是对应的人数
# 下面提取出职业和对应的人数
x_label = np.array([i[0] for i in occupation_counts])
y = np.array([i[1] for i in occupation_counts])
# 我们先对统计结果进行排序以便于展现
x_label = x_label[np.argsort(y)]
y = y[np.argsort(y)]
print(x_label)
print(y)
x_pos = np.arange(len(y))  # 设置每一个条形图的中心位置，要不没办法画图，条形图传数值型的x，y进去；同时也作为xticks的中心位置，这样就实现了用字符对x轴进行标
plt.bar(x_pos, y)
plt.xticks(x_pos, x_label, rotation=30)  # xticks与xlabel是不一样，前者就跟刻度线一样的，后者只是说明x轴代表什么。
plt.show()

sc.stop()
