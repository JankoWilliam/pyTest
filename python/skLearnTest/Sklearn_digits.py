# coding=GBK
import matplotlib.pyplot as plt

from sklearn.datasets import load_digits

# 手写数字集
digits = load_digits()
print(digits.data.shape)
print(digits.target.shape)
print(digits.images.shape)

# plt.matshow(digits.images[8])
# plt.show()
plt.subplot(221) # 第一行的左图
plt.subplot(222) # 第一行的右图
plt.subplot(212) # 第二整行
plt.show()

