# coding=gbk
# �������ݼ���sklearn�����ڶ����ݼ�
from sklearn import datasets
# �����ݷ�Ϊ���Լ���ѵ����
from sklearn.model_selection import train_test_split
# �����ڽ��㷽ʽѵ������
from sklearn.neighbors import KNeighborsClassifier

# ݺβ������
iris = datasets.load_iris()
# ��������
iris_x = iris.data

# print(iris_x)
print('�����������ȣ�', len(iris_x))
# Ŀ��ֵ
iris_y = iris.target
print('Ŀ��ֵ��', iris_y)
# ����train_test_split����ѵ�����Ͳ��Լ��ֿ���test_sizeռ30%
x_train, x_test, y_train, y_test = train_test_split(iris_x, iris_y, test_size=0.3)

# ����ѵ������
knn = KNeighborsClassifier()
# �������������ݽ���ѵ��
knn.fit(x_train, y_train)

params = knn.get_params()
print('params:', params)

score = knn.score(x_test, y_test)
print('Ԥ��÷�:%s' % score)

# Ԥ�����ݣ�Ԥ������ֵ
print('Ԥ������ֵ��', knn.predict(x_test))
print('ʵ������ֵ��', y_test)
