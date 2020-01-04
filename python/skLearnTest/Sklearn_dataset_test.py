# coding=gbk
import sklearn.datasets as ds
from matplotlib import pyplot

# ���Ʒ������ݼ�
data, label = ds.make_blobs(n_samples=100, n_features=2, centers=5)
# ����������ʾ
pyplot.scatter(data[:, 0], data[:, 1], c=label)
pyplot.show()