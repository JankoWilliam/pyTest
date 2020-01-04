import numpy as np
import matplotlib.pyplot as plt

alist = [4, 5, 7, 1, 3, 7, 4, 9, 4, 2]  # 也可以是ndarray类型
blist = [8, 3, 6, 1, 0, 4, 5, 9, 2, 7]

t_plt, = plt.plot(np.arange(1, len(alist) + 1), alist, 'r')
v_plt, = plt.plot(np.arange(1, len(alist) + 1), blist)

plt.title('Model Loss')  # 图的标题

plt.xlabel('epoch')  # x轴的名称
plt.ylabel('loss')  # y轴的名称

plt.legend((t_plt, v_plt), ('train', 'validation'))  # 标注同一张图上的两组数据
plt.show()

