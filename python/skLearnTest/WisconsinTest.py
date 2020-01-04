# coding=GBK
import pandas as pd
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data',
                 header=None)
print(df)
x = df.loc[:, 2:].values
y = df.loc[:, 1].values
le = LabelEncoder()
y = le.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

# 通过流水线将StandardScaler、PCA，以及LogisticRegression对象串联起来：
pipe_lr = Pipeline([
    ('scl',StandardScaler()),
    ('pca',PCA(n_components=2)),
    ('clf',LogisticRegression(random_state=1))
])
pipe_lr.fit(x_train,y_train)
print('Test Accuracy : %.3f' %pipe_lr.score(x_test,y_test))

