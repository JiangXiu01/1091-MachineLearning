from os import listdir
from os.path import isfile, isdir, join
import pickle
import time
import matplotlib.pyplot as plt

mypath = "games/pingpong/總匯log"
OutputFileNmae = "./csv/1PNORMAL.sav"
files = listdir(mypath)
data = []

for f in files:
    fullpath = join(mypath, f)
    loadFile = open(fullpath, "rb") #rb => binary mode
    data.append(pickle.load(loadFile))
    loadFile.close()

print("train: " + str(len(data)) + " logs")

frame = []
status = []
ballPosition = []
ballspeed = []
platformPosition1P = []
platformPosition2P = []
Dropt_point = []
aid = 0
for i in range(0, len(data)):
    for j in range(0, len(data[i]['ml_1P']['scene_info'])):
        '''
        ballspeedY = data[i]['ml_1P']['scene_info'][j]['ball_speed'][1]
        if ballspeedY != 0:
            frame.append(data[i]['ml_1P']['scene_info'][j]['frame'])
            status.append(data[i]['ml_1P']['scene_info'][j]['status'])
            ballPosition.append(data[i]['ml_1P']['scene_info'][j]['ball'])
            ballspeed.append(data[i]['ml_1P']['scene_info'][j]['ball_speed'])
            platformPosition1P.append(data[i]['ml_1P']['scene_info'][j]['platform_1P'])
            platformPosition2P.append(data[i]['ml_2P']['scene_info'][j]['platform_2P'])
            speedY = data[i]['ml_1P']['scene_info'][j]['ball_speed'][1]
            aid = data[i]['ml_1P']['scene_info'][j]['ball'][0] + ((80 - (data[i]['ml_1P']['scene_info'][j]['ball'][1])) / ballspeedY * data[i]['ml_1P']['scene_info'][j]['ball_speed'][0])
            if aid < 0:
                aid = -aid
            if aid > 195:
                if aid > 390:
                    aid = aid -390
                else:
                    aid = 195 - (aid - 195)
            #if speedY < 0:
                #aid = 100
            Dropt_point.append(aid)
        #print("aid>>> ", aid)
        #time.sleep(0.2)
        '''
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
plat_1P_X = plat_1P_X + 20
plat_1P_Y = np.array(platformPosition1P)[:-1, -1][:, np.newaxis] #1P板子Y


plat_1P_X_B = np.array(platformPosition1P)[:, 0][:, np.newaxis] #1P板子X
plat_1P_X_B = plat_1P_X_B + 20
#--2P--
plat_2P_X = np.array(platformPosition2P)[:-1, 0][:, np.newaxis] #1P板子X
plat_2P_X = plat_2P_X + 20
plat_2P_Y = np.array(platformPosition2P)[:-1, -1][:, np.newaxis] #1P板子Y
#------

plat_1P_X_next = plat_1P_X_B[1:, :]
instruct = (plat_1P_X_next - plat_1P_X_B[0: len(plat_1P_X_next), 0][ :, np.newaxis]) / 5
y = instruct

ball_Position_X = np.array(ballPosition)[0:-1, 0][:, np.newaxis] #0 => 球X
ball_Position_Y = np.array(ballPosition)[0:-1, -1][:, np.newaxis] #-1 => 球Y
ball_Speed_X = np.array(ballspeed)[0:-1, 0][:, np.newaxis] #球速度X
ball_Speed_Y = np.array(ballspeed)[0:-1, -1][:, np.newaxis] #球速度Y
DroptPoint = np.array(Dropt_point)[0:-1][:, np.newaxis]

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

############
#x = np.hstack((plat_1P_X, plat_1P_Y, ball_Position_X, ball_Position_Y, ball_Speed_X, ball_Speed_Y, DroptPoint))
x = np.hstack((plat_1P_X, plat_1P_Y, ball_Position_X, ball_Position_Y, ball_Speed_X, ball_Speed_Y))
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 0) #test_size => 比較 100=> 90:10測試信任度


from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression

neigh = KNeighborsClassifier(n_neighbors = 3)
neigh.fit(x_train, y_train)

print("準確程度評估(test)>> ", neigh.score(x_test,y_test))
print("準確程度評估(train)>> ", neigh.score(x_train, y_train))

y_knn = neigh.predict(x_test)

pickle.dump(neigh, open(OutputFileNmae, 'wb'))

print('KNN.sav Completed.')
