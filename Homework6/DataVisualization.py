from matplotlib import pyplot as plt
import numpy as np
import csv

BallCoordinateX_1P = []
BallCoordinateY_1P = []
BallCoordinateX_2P = []
BallCoordinateY_2P = []
PlatCoordinate_1P = []
PlatCoordinate_2P = []
#-----------------BallCoordinate_1P-----------------
with open("./1P_Log.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        BallCoordinateX_1P.append(int(row[1]))  #從csv讀取的資料是str型別
        BallCoordinateY_1P.append(int(row[2]))
        PlatCoordinate_1P.append(int(row[6]))
        
#畫折線圖
plt.subplot(2, 3, 1)
plt.scatter(BallCoordinateX_1P, BallCoordinateY_1P) #label='Ball coordinates'
plt.xlabel('Ball X')
plt.ylabel('Ball Y')
plt.title('BallCoordinate_1P')
plt.legend()

plt.subplot(2, 3, 2)
plt.scatter(PlatCoordinate_1P, BallCoordinateX_1P)
plt.xlabel('Plat X')
plt.ylabel('Ball X')
plt.title('PlatCoordinateX-BallCoordinateX_1P')
plt.legend()

plt.subplot(2, 3, 3)
plt.scatter(PlatCoordinate_1P, BallCoordinateY_1P)
plt.xlabel('Plat X')
plt.ylabel('Ball Y')
plt.title('BallCoordinateY-PlatCoordinateX_1P')
plt.legend()
#---------------------------------------------------
#-----------------BallCoordinate_2P-----------------
with open("./2P_Log.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        BallCoordinateX_2P.append(int(row[1]))  #從csv讀取的資料是str型別
        BallCoordinateY_2P.append(int(row[2]))
        PlatCoordinate_2P.append(int(row[6]))
#畫折線圖
plt.subplot(2, 3, 4)
plt.scatter(BallCoordinateX_2P, BallCoordinateY_2P, label='Ball coordinates')
plt.xlabel('Ball X')
plt.ylabel('Ball Y')
plt.title('BallCoordinate_2P')

plt.subplot(2, 3, 5)
plt.scatter(PlatCoordinate_2P, BallCoordinateX_2P)
plt.xlabel('Plat X')
plt.ylabel('Ball X')
plt.title('PlatCoordinateX-BallCoordinateX_2P')
plt.legend()

plt.subplot(2, 3, 6)
plt.scatter(PlatCoordinate_2P, BallCoordinateY_2P)
plt.xlabel('Plat X')
plt.ylabel('Ball Y')
plt.title('BallCoordinateY-PlatCoordinateX_2P')
plt.legend()
#----------------------------------------------------

plt.show()