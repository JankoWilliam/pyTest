# coding=gbk
# 引入数据集，sklearn包含众多数据集
from sklearn import datasets
# 将数据分为测试集和训练集
from sklearn.model_selection import train_test_split
# 利用邻近点方式训练数据
from sklearn.neighbors import KNeighborsClassifier

# 莺尾花数据
iris = datasets.load_iris()
# 特征变量
iris_x = iris.data

# print(iris_x)
print('特征变量长度：', len(iris_x))
# 目标值
iris_y = iris.target
print('目标值：', iris_y)
# 利用train_test_split进行训练集和测试集分开，test_size占30%
x_train, x_test, y_train, y_test = train_test_split(iris_x, iris_y, test_size=0.3)

# 引入训练方法
knn = KNeighborsClassifier()
# 进行填充测试数据进行训练
knn.fit(x_train, y_train)

params = knn.get_params()
print('params:', params)

score = knn.score(x_test, y_test)
print('预测得分:%s' % score)

# 预测数据，预测特征值
print('预测特征值：', knn.predict(x_test))
print('实际特征值：', y_test)
