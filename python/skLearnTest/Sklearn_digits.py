# coding=GBK
import matplotlib.pyplot as plt

from sklearn.datasets import load_digits

# ��д���ּ�
digits = load_digits()
print(digits.data.shape)
print(digits.target.shape)
print(digits.images.shape)

# plt.matshow(digits.images[8])
# plt.show()
plt.subplot(221) # ��һ�е���ͼ
plt.subplot(222) # ��һ�е���ͼ
plt.subplot(212) # �ڶ�����
plt.show()

