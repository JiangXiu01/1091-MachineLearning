from games.pingpong.ml.Moduls import CSV_Read_1P
import math
import time
import os
import pickle
import numpy as np
import csv
import random
"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        self.ball_served = False
        self.side = "2P"
        self.ball_location = [0,0]

        filename = "D:./csv/dicisiontree_2P.sav"
        self.model_2P = pickle.load(open(filename,'rb'))
    def update(self, scene_info):
        Mode = "RULE" #KNN or Dt or RULE
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        #------------------------Decisiontree--------------------
        if Mode == "Dt": #decisiontree
            if self.side == "2P":
                while True:
                    ball_speed = scene_info["ball_speed"]
                    BallCoordinate_Now = scene_info["ball"]

                    if scene_info["status"] == "GAME_1P_WIN" or \
                        scene_info["status"] == "GAME_2P_WIN":
                    # Some updating or reseting code here

                        continue
                    if ball_speed[1] < 0: #球往上
                        if ball_speed[0] < 0: #球往左上
                            LRUP = 1
                        else: #球往右上
                            LRUP = 2
                    else: #球往下
                        if ball_speed[0] < 0: #球往左下
                            LRUP = 3
                        else: #球往右下
                            LRUP = 4

                    inp_temp = [BallCoordinate_Now[0],BallCoordinate_Now[1],LRUP, \
                                     (195 - BallCoordinate_Now[0])]
                    move = str(self.model_2P.classify_test(inp_temp))

                    try:
                        aid = move[1:3]
                        # print(aid)
                        aid = int(aid) *10
                    except:
                        aid = move[1:2]
                        aid = int(aid) *10
                    if(aid<50 and abs(scene_info["ball_speed"][1]) >= 21 ):
                        aid += 10

                    if(scene_info["platform_2P"][0] +20 > aid):
                        return "MOVE_LEFT"
                    elif(scene_info["platform_2P"][0] +20 < aid):
                        return "MOVE_RIGHT"
                    else:
                        return "NONE"
        #--------------------------------------------------------
        #------------------------KNN-----------------------------
        if Mode == "KNN":
            filename = "D:/高科大學校/機器學習/MLGame-master8.01/MLGame-master/csv/2P的50總匯log.sav"
            model = pickle.load(open(filename, 'rb'))
            '''
            if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
                print('GAME_2P_WIN!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                print(Time)
                time.sleep(1)
                print('Discard failed LOGs=> ' + 'ml_NORMAL_30_' + Time + '.pickle')
                os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/ml_NORMAL_30_' + Time + '.pickle')
                ball_speed = scene_info["ball_speed"]
                with open('./games/pingpong/ml/Knn_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    writer.writerow([Time ,ball_speed, "Lose", self.ServePosition, self.Serve])
            if scene_info["status"] == "GAME_1P_WIN":
                with open('./games/pingpong/ml/Knn_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    ball_speed = scene_info["ball_speed"]
                    writer.writerow([Time ,ball_speed, "WIN", self.ServePosition, self.Serve])
            '''
            BallCoordinate_Now = scene_info["ball"]
            ball_speed = scene_info["ball_speed"]
            PlatformX_1P = scene_info["platform_1P"][0] + 20
            PlatformY_1P = scene_info["platform_1P"][1] + 20
            PlatformX_2P = scene_info["platform_2P"][0] + 20
            PlatformY_2P = scene_info["platform_2P"][1] + 20
            aid = 0
            if ball_speed[0] != 0:
                m = ball_speed[1] / ball_speed[0]
                aid = BallCoordinate_Now[0] + ((BallCoordinate_Now[1] - 80) / -m)

                if aid < 0:
                    aid = -aid
                if aid > 195:
                    if aid > 390:
                        aid = aid -390
                    else:
                        aid = 195 - (aid - 195)


            input = []
            inp_temp = np.array([PlatformX_2P, PlatformY_2P, BallCoordinate_Now[0], BallCoordinate_Now[1], ball_speed[0], ball_speed[1]])

            input = inp_temp[np.newaxis, :]

            move = model.predict(input)
            print("input>>> ", move)
            if move < 0:
                return "MOVE_LEFT"
            elif move > 0:
                return "MOVE_RIGHT"
            else:
                return "None"
        #--------------------------------------------------------
        #------------------------RULEBASE------------------------
        if Mode == "RULE":
            BallCoordinate_Now = scene_info["ball"]
            ball_speed = scene_info["ball_speed"]
            BallCoordinate_Last = (BallCoordinate_Now[0] + ball_speed[0] , BallCoordinate_Now[1] + ball_speed[1])
            PlatformX = scene_info["platform_2P"][0] + 20
            BallUpAndDown = ''
            aid = 0
            m = 1

            if BallCoordinate_Now[0] - BallCoordinate_Last[0] != 0:
                m = ball_speed[1] / ball_speed[0]
                aid = BallCoordinate_Now[0] + ((BallCoordinate_Now[1] - 80) / -m)

            if aid < 0:
                aid = -aid
            elif aid > 200:
                aid = aid - 200
                aid = 200 - aid

            if BallCoordinate_Now[1] - BallCoordinate_Last[1] > 0:
                BallUpAndDown = 'Down'
            else:
                BallUpAndDown = 'Up'

            if BallUpAndDown == 'Down' and PlatformX > aid :
                return "MOVE_LEFT"
            if BallUpAndDown == 'Down' and PlatformX < aid :
                return "MOVE_RIGHT"

            if BallUpAndDown == 'Up' and PlatformX < 100:
                return "MOVE_RIGHT"

            if BallUpAndDown == 'Up' and PlatformX > 100:
                return "MOVE_LEFT"

            if BallUpAndDown == 'Up' and PlatformX == 100:
                return "NONE"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False