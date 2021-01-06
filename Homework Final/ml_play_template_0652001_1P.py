#from games.pingpong.ml.Moduls import CSV_Read_1P
from games.pingpong.ml.Moduls import DropPointCalculator
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
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the MLPlay is used by
               which side.
        """
        self.ball_served = False
        self.side = "1P"
        self.ServePosition = random.randrange(20,180, 5) #亂數5的倍數 發球座標
    def update(self, scene_info):
        Mode = "KNN" #KNN or RULE
        #------------------------隨機發球------------------------
        print("self.ball_served>>>> ", self.ball_served)
        if self.ball_served:
            pass
        else:
            print("self.ServePosition>>> ", self.ServePosition)
            PlatformX = scene_info["platform_1P"][0] + 20
            print("PlatformX>>> ", PlatformX)
            if PlatformX < self.ServePosition:
                return "MOVE_RIGHT"
            if PlatformX > self.ServePosition:
                return "MOVE_LEFT"
            if PlatformX == self.ServePosition:
                self.Serve = random.randint(0,2)
                print("Serve>>> ", self.Serve)
                if self.Serve == 1:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
                if self.Serve == 2:
                    self.ball_served = True
                    return "SERVE_TO_LEFT"
                else:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
        #--------------------------------------------------------
        if Mode == "RULE":
            # Make the caller to invoke reset() for the next round.
            '''
            if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
                print('GAME_2P_WIN!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                print(Time)
                time.sleep(1.5)
                print('Discard failed LOGs=> ' + 'ml_HARD_190_' + Time + '.pickle')
                os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/ml_HARD_190_' + Time + '.pickle')
                ball_speed = scene_info["ball_speed"]
                with open('./games/pingpong/ml/RULE_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    writer.writerow([Time ,ball_speed, "Lose", self.ServePosition, self.Serve])
            
            if scene_info["status"] == "GAME_1P_WIN":
                with open('./games/pingpong/ml/RULE_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    ball_speed = scene_info["ball_speed"]
                    writer.writerow([Time ,ball_speed, "WIN", self.ServePosition, self.Serve])
            '''
            #print(scene_info)
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"

            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                if scene_info["ball_speed"][0] != 0:
                    BallCoordinate_Now = scene_info["ball"]
                    ball_speed = scene_info["ball_speed"]
                    PlatformX = scene_info["platform_1P"][0] + 20
                    PlatformY = scene_info["platform_1P"][1] + 20
                    PlatformX_2P = scene_info["platform_2P"][0] + 20
                    PlatformY_2P = scene_info["platform_2P"][1] + 20
                    BallUpAndDown = ''
                    BallUpAndDown_NUM = 0
                    aid = 0 #落點x
                    hitthefall_number = 0 #撞牆次數
                    Dropt_point = [0 ,0]#預測落點座標
                    Dropt_point_cut = [0 ,415] #正常反打到我方的落點
                    Dropt_point_Forward_cut = [0 ,415] #順向切球到我方的落點
                    Dropt_point_Reverse_cut = [0 ,415] #反向切球到我方的落點
                    ball_speed_Prediction = [0,0] #預測球速
                    Reverse = 1
                    compensate_speedX = 0 #球速補償
                    Frame = scene_info['frame']
                    m = ball_speed[1] / ball_speed[0]
                    if ball_speed[1] > 0:
                        BallUpAndDown = 'Down'
                        BallUpAndDown_NUM = 0
                    else:
                        BallUpAndDown = 'Up'
                        BallUpAndDown_NUM = 1
                    #CSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)
                    #-------------------------落點判斷-------------------------
                    if BallUpAndDown == 'Down':
                        platform = 415
                        aid, hitthefall_number= DropPointCalculator.doDPC(BallCoordinate_Now, ball_speed, platform)
                        Dropt_point = [aid ,415]
                    #---------------------------------------------------------
                    #-------------------------落點預測1-------------------------
                    if BallUpAndDown == 'Up':
                        platform = 80
                        aid, hitthefall_number= DropPointCalculator.doDPC(BallCoordinate_Now, ball_speed, platform)
                        Dropt_point = [aid ,80]    #到對方板子的落點:落點預測1的輸入
                        ball_speed_Prediction[1] = -ball_speed[1]
                        platform = 415
                        if hitthefall_number == 1 or hitthefall_number == 3:
                            Reverse = -1
                        if abs(ball_speed[0]) != abs(ball_speed[1]):
                            if ball_speed[0] < 0:
                                compensate_speedX = 3
                            else:
                                compensate_speedX = -3
                        #正常反打
                        ball_speed_Prediction[0] = (ball_speed[0] + compensate_speedX) * Reverse
                        aid, hitthefall_number = DropPointCalculator.doDPC(Dropt_point, ball_speed_Prediction, platform)
                        Dropt_point_cut = [aid ,415]
                        #順向切球
                        if ball_speed[0] > 0:
                            ball_speed_Prediction[0] = ((ball_speed[0] + 3) + compensate_speedX) * Reverse
                        else:
                            ball_speed_Prediction[0] = ((ball_speed[0] - 3) + compensate_speedX) * Reverse
                        aid, hitthefall_number = DropPointCalculator.doDPC(Dropt_point, ball_speed_Prediction, platform)
                        Dropt_point_Forward_cut = [aid ,415]
                        #反向切球
                        ball_speed_Prediction[0] = (-ball_speed[0] - compensate_speedX) * Reverse
                        aid, hitthefall_number = DropPointCalculator.doDPC(Dropt_point, ball_speed_Prediction, platform)
                        Dropt_point_Reverse_cut = [aid ,415]
                    
                    #-------------------------落點預測2-----------------------
                        Max = max(Dropt_point_cut[0], Dropt_point_Forward_cut[0], Dropt_point_Reverse_cut[0])
                        Min = min(Dropt_point_cut[0], Dropt_point_Forward_cut[0], Dropt_point_Reverse_cut[0])                 
                        Mid = (Dropt_point_cut[0] + Dropt_point_Forward_cut[0] + Dropt_point_Reverse_cut[0]) / 3
                        Average = (Max + Min) / 2
                        print('avg-> ', Average, Mid)
                        if abs((PlatformY - PlatformY_2P) / ball_speed[1]) < ((Max - Average) / 5):
                            Average = (Max + Mid) / 2 
                            print('avg22-> ', Average)
                    #---------------------------------------------------------
                    #CSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM, Dropt_point[0], Dropt_point_cut[0], Dropt_point_Forward_cut[0], Dropt_point_Reverse_cut[0])
                    print('預測3個落點',Dropt_point_cut, Dropt_point_Forward_cut, Dropt_point_Reverse_cut)
                    print(BallUpAndDown, BallCoordinate_Now ,Dropt_point, ball_speed_Prediction, ball_speed, hitthefall_number, scene_info['frame'] )
                    if PlatformX > aid and BallUpAndDown == 'Down':
                        return "MOVE_LEFT"
                    if PlatformX < aid and BallUpAndDown == 'Down':
                        return "MOVE_RIGHT"
                    if BallUpAndDown == 'Up':
                        if PlatformX > Average:
                            return "MOVE_LEFT"
                        if PlatformX < Average:
                            return "MOVE_RIGHT"
                        else:
                            return "None"

        if Mode == "KNN":
            filename = "D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/2P改1P_LOG_HARD_140.sav"
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
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"
                
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                BallCoordinate_Now = scene_info["ball"]
                ball_speed = scene_info["ball_speed"]
                PlatformX_1P = scene_info["platform_1P"][0] + 20
                PlatformY_1P = scene_info["platform_1P"][1] + 20
                PlatformX_2P = scene_info["platform_2P"][0] + 20
                PlatformY_2P = scene_info["platform_2P"][1] + 20             


                input = []
                inp_temp = np.array([PlatformX_1P, PlatformY_1P, BallCoordinate_Now[0], BallCoordinate_Now[1], ball_speed[0], ball_speed[1]])

                input = inp_temp[np.newaxis, :]
                   
                move = model.predict(input)
                print("input>>> ", move)
                if move < 0:
                    return "MOVE_LEFT"
                elif move > 0:
                    return "MOVE_RIGHT"
                else:
                    return "None"

    def reset(self):
        """
        Reset the status
        """
        self.ServePosition = random.randrange(20,180, 5)
        self.ball_served = False