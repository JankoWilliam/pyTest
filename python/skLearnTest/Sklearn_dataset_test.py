# coding=gbk
import sklearn.datasets as ds
from matplotlib import pyplot

# 自制分类数据集
data, label = ds.make_blobs(n_samples=100, n_features=2, centers=5)
# 绘制样本显示
pyplot.scatter(data[:, 0], data[:, 1], c=label)
pyplot.show()