from os import listdir
from os.path import isfile, isdir, join
import pickle
import time
import matplotlib.pyplot as plt

mypath = "games/pingpong/總匯log" #欲讀入LOG檔目錄
OutputFileNmae = "./csv/1PNORMAL.sav" #輸出SAV位置
files = listdir(mypath)
data = [] #檔案目錄下的檔案

#------------------讀取log樣本------------------
for f in files:
    fullpath = join(mypath, f)
    loadFile = open(fullpath, "rb") #rb => binary mode
    data.append(pickle.load(loadFile)) #存放目錄下所有檔案
    loadFile.close()

print("train: " + str(len(data)) + " logs")

frame = [] #log => Frame
status = [] #log => 狀態
ballPosition = [] #log => 球位置
ballspeed = [] #log => 球速度
platformPosition1P = [] #log => 1P板位置
platformPosition2P = [] #log => 2P板位置

for i in range(0, len(data)):
    for j in range(0, len(data[i]['ml_1P']['scene_info'])):
        frame.append(data[i]['ml_1P']['scene_info'][j]['frame'])
        status.append(data[i]['ml_1P']['scene_info'][j]['status'])
        ballPosition.append(data[i]['ml_1P']['scene_info'][j]['ball'])
        ballspeed.append(data[i]['ml_1P']['scene_info'][j]['ball_speed'])
        platformPosition1P.append(data[i]['ml_1P']['scene_info'][j]['platform_1P'])
        platformPosition2P.append(data[i]['ml_2P']['scene_info'][j]['platform_2P'])
        
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

#--1P--
plat_1P_X = np.array(platformPosition1P)[:-1, 0][:, np.newaxis] #1P板子X
plat_1P_X = plat_1P_X + 20 #計算版寬用
plat_1P_Y = np.array(platformPosition1P)[:-1, -1][:, np.newaxis] #1P板子Y

plat_1P_X_B = np.array(platformPosition1P)[:, 0][:, np.newaxis] #1P板子X
plat_1P_X_B = plat_1P_X_B + 20 #計算版寬用
#--2P--
plat_2P_X = np.array(platformPosition2P)[:-1, 0][:, np.newaxis] #1P板子X
plat_2P_X = plat_2P_X + 20 #計算版寬用
plat_2P_Y = np.array(platformPosition2P)[:-1, -1][:, np.newaxis] #1P板子Y
#------

plat_1P_X_next = plat_1P_X_B[1:, :] #1P下一筆資料
instruct = (plat_1P_X_next - plat_1P_X_B[0: len(plat_1P_X_next), 0][ :, np.newaxis]) / 5 #板子移動計算
y = instruct

ball_Position_X = np.array(ballPosition)[0:-1, 0][:, np.newaxis] #0 => 球X
ball_Position_Y = np.array(ballPosition)[0:-1, -1][:, np.newaxis] #-1 => 球Y
ball_Speed_X = np.array(ballspeed)[0:-1, 0][:, np.newaxis] #球速度X
ball_Speed_Y = np.array(ballspeed)[0:-1, -1][:, np.newaxis] #球速度Y
DroptPoint = np.array(Dropt_point)[0:-1][:, np.newaxis]

#Debug用, 用於查看資料陣列長度
'''
print("plat_1P_X長度>> ", len(plat_1P_X))
print("plat_1P_Y長度>> ", len(plat_1P_Y))
print("plat_2P_X長度>> ", len(plat_2P_X))
print("plat_2P_Y長度>> ", len(plat_2P_Y))
print("ball_Position_X長度>> ", len(ball_Position_X))
print("ball_Position_Y長度>> ", len(ball_Position_Y))
print("ball_Speed_X長度>> ", len(ball_Speed_X))
print("ball_Speed_Y長度>> ", len(ball_Speed_Y))
print("instruct長度>> ", len(instruct))
print("DroptPoint長度>> ", len(DroptPoint))
'''

#x = np.hstack((plat_1P_X, plat_1P_Y, ball_Position_X, ball_Position_Y, ball_Speed_X, ball_Speed_Y, DroptPoint))
x = np.hstack((plat_1P_X, plat_1P_Y, ball_Position_X, ball_Position_Y, ball_Speed_X, ball_Speed_Y)) #採用的樣本
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 0) #test_size => 比較 100=> 90:10測試信任度

#------------------sklearn產生模型------------------
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression

neigh = KNeighborsClassifier(n_neighbors = 3) #k值 = 3
neigh.fit(x_train, y_train) #將資料做訓練

print("準確程度評估(test)>> ", neigh.score(x_test,y_test))
print("準確程度評估(train)>> ", neigh.score(x_train, y_train))

y_knn = neigh.predict(x_test)

pickle.dump(neigh, open(OutputFileNmae, 'wb'))

print('KNN.sav Completed.')
