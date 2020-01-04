#coding=gbk
import numpy as np
from sklearn import preprocessing as pre_processing
from sklearn.cluster import KMeans
from hdfs.client import Client
import matplotlib.pyplot as plt

data = np.genfromtxt("C:\\Users\\ChuangLan\\Desktop\\company_info_2.txt",encoding='utf-8',dtype=np.str,delimiter="\t")


label=pre_processing.LabelEncoder()
dim01=label.fit_transform(data[:,2])

min_max_scaler = pre_processing.MinMaxScaler(feature_range=(0, 1))
dim02 = min_max_scaler.fit_transform(data[:,4].reshape(-1,1))

data_new = data[:,[12,16,20,26,28,32]]

print(np.shape(dim01))
print(dim01)
print(np.array(list(data_new)))

distortions = []
for i in range(1,11):
    km = KMeans(n_clusters = i, init = 'k-means++', n_init = 10, max_iter = 300, random_state = 0)
    km.fit(data_new)
    # km.inertia_ 获取每次聚类后误差
    distortions.append(km.inertia_)

plt.plot(range(1,11), distortions, marker = 'o')
plt.xlabel('簇数量')
plt.ylabel('误差')
plt.show()


km = KMeans(n_clusters = 3, init = 'random',n_init = 10, max_iter = 300, tol = 1e-04, random_state = 0)
y_km = km.fit_predict(data_new)
# plt.scatter(data_new[y_km == 0, 0], data_new[y_km == 0, 1], s = 50, c = 'lightgreen', marker = 's', label = '簇 1')
# plt.scatter(data_new[y_km == 1, 0], data_new[y_km == 1, 1], s = 50, c = 'orange', marker = 'o', label = '簇 2')
# plt.scatter(data_new[y_km == 2, 0], data_new[y_km == 2, 1], s = 50, c = 'lightblue', marker = 'v', label = '簇 3')
# plt.scatter(km.cluster_centers_[:,0], km.cluster_centers_[:,1], s = 250, marker = '*', c = 'red', label = '中心点')
# plt.legend()
# plt.grid()
# plt.show()
print( y_km)