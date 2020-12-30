import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import csv


'''
data = np.random.rand(100, 2)
print("data=>", data)
#生成一個隨機資料,樣本大小為100, 特徵數為2(這裡因為要畫二維圖,所以就將特徵設為2,至於三維怎麼畫?
#後續看有沒有機會研究,當然你也可以試著降維到2維畫圖也行)
'''

np1 = np.genfromtxt('./1P_Log_20-13.csv', delimiter=',')
print(np1)

estimator = KMeans(n_clusters = 3)#構造聚類器,構造一個聚類數為3的聚類器
estimator.fit(np1)#聚類
label_pred = estimator.labels_ #獲取聚類標籤
centroids = estimator.cluster_centers_ #獲取聚類中心
inertia = estimator.inertia_ # 獲取聚類準則的總和
mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr'] #這裡'or'代表中的'o'代表畫圈,'r'代表顏色為紅色,後面的依次類推
color = 0
j = 0

for i in label_pred:
    plt.plot([np1[j:j+1,0]], [np1[j:j+1,1]], mark[i], markersize = 5)
    j +=1
plt.show()