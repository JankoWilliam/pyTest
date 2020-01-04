# coding=gbk
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

X, y = make_blobs(n_samples=150,
                  n_features=2,
                  centers=3,
                  cluster_std=0.5,
                  shuffle=True,
                  random_state=0)
plt.scatter(X[:, 0],
            X[:, 1],
            c='black',
            marker='o',
            s=50
            )
plt.grid()
plt.show()

# km = KMeans(n_clusters=3,
#             init='random',
#             n_init=10,
#             max_iter=300,
#             tol=1e-04,
#             random_state=0)
# y_km = km.fit_predict(X)
# print(y_km)
distortions = []
for i in range(1,11):
    km = KMeans(n_clusters=i,
                init='k-means++',
                n_init=10,
                max_iter=300,
                random_state=0)
    km.fit(X)
    distortions.append(km.inertia_)
plt.plot(range(1,11),distortions,marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Distortion')
plt.show()


