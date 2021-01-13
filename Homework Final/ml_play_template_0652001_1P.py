from games.pingpong.ml.Moduls import CSV_Read_1P
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
        # self.ServePosition = random.randrange(20,180, 5) #亂數5的倍數, 隨機發球用, 板子亂數位置
    def update(self, scene_info):
        Mode = "KNN" #KNN or RULE or Dt
        
        #------------------------隨機發球------------------------
        '''
        #print("self.ball_served>>>> ", self.ball_served)
        if self.ball_served:
            pass
        else:
            #print("self.ServePosition>>> ", self.ServePosition)
            PlatformX = scene_info["platform_1P"][0] + 20
            #print("PlatformX>>> ", PlatformX)
            if PlatformX < self.ServePosition:
                return "MOVE_RIGHT"
            if PlatformX > self.ServePosition:
                return "MOVE_LEFT"
            if PlatformX == self.ServePosition:
                self.Serve = random.randint(0,2)
                #print("Serve>>> ", self.Serve)
                if self.Serve == 1:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
                if self.Serve == 2:
                    self.ball_served = True
                    return "SERVE_TO_LEFT"
                else:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
        '''
        #--------------------------------------------------------
        #------------------------Decisiontree--------------------
        if Mode == "Dt":
            filename = "D:./csv/my_tree_1P_new.sav"
            model = pickle.load(open(filename,'rb'))
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"

            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
        
            # 3. Start an endless loop
            while True:
                ball_speed = scene_info["ball_speed"]
                BallCoordinate_Now = scene_info["ball"]
                if ball_speed[1] > 0: #go to down
                    if ball_speed[0] < 0: #go RD
                        LRUP = 2
                    else: #go LD
                        LRUP = 1
                else: #go to up
                    if ball_speed[0] < 0: #go RU
                        LRUP = 4
                    else: #go LU
                        LRUP = 3
                        
                inp_temp = [BallCoordinate_Now[0],BallCoordinate_Now[1],LRUP, \
                                 (200 - BallCoordinate_Now[0])]

                move = str(model.classify_test(inp_temp))
                try:
                    aid = move[1:3]
                    aid = int(aid) *10
                except:
                    aid = move[1:2]
                    aid = int(aid) *10
                if(scene_info["platform_1P"][0] +20 > aid):
                    return "MOVE_LEFT"
                elif(scene_info["platform_1P"][0] +20 < aid):
                    return "MOVE_RIGHT"
                else:
                    return "NONE"        
        #--------------------------------------------------------
        #------------------------RULEBASE------------------------
        if Mode == "RULE":
            if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
                print('GAME_2P_WIN!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) #取得當前時間
                print(Time)
                time.sleep(1.5) #Delay1.5 sec, 防止log寫出太慢
                #print('Discard failed LOGs=> ' + 'ml_NORMAL_20_' + Time + '.pickle')
                os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/ml_NORMAL_50_' + Time + '.pickle') #移除log
                ball_speed = scene_info["ball_speed"]
                with open('./games/pingpong/ml/RULE_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加 #寫出CSV, 可視化用
                    writer = csv.writer(csvfile)
                    writer.writerow([Time ,ball_speed, "Lose", self.ServePosition, self.Serve])
            '''
            if scene_info["status"] == "GAME_1P_WIN":
                with open('./games/pingpong/ml/RULE_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    ball_speed = scene_info["ball_speed"]
                    writer.writerow([Time ,ball_speed, "WIN", self.ServePosition, self.Serve])
            '''
            #遊戲狀態預設設定
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else: #主程式
                if scene_info["ball_speed"][0] != 0: #debug用, 球尚未發出時速度會是0, 防止aid計算錯誤
                    BallCoordinate_Now = scene_info["ball"] #當前球位置
                    ball_speed = scene_info["ball_speed"] #當前球速
                    PlatformX = scene_info["platform_1P"][0] + 20 #1P板子X
                    PlatformY = scene_info["platform_1P"][1] + 20 #1P板子Y
                    PlatformX_2P = scene_info["platform_2P"][0] + 20 #2P板子X
                    PlatformY_2P = scene_info["platform_2P"][1] + 20 #2P板子Y
                    BallUpAndDown = '' #球狀態: up/down
                    BallUpAndDown_NUM = 0 #球狀態 up =>1, down =>0
                    aid = 0 #落點x
                    hitthefall_number = 0 #撞牆次數
                    Dropt_point = [0 ,0]#預測落點座標
                    Dropt_point_cut = [0 ,415] #正常反打到我方的落點
                    Dropt_point_Forward_cut = [0 ,415] #順向切球到我方的落點
                    Dropt_point_Reverse_cut = [0 ,415] #反向切球到我方的落點
                    ball_speed_Prediction = [0,0] #預測球速
                    Reverse = 1
                    compensate_speedX = 0 #球速補償
                    Frame = scene_info['frame'] #當前frame
                    m = ball_speed[1] / ball_speed[0] #斜率
                    
                    #判斷球為往上or落下
                    if ball_speed[1] > 0:
                        BallUpAndDown = 'Down'
                        BallUpAndDown_NUM = 0
                    else:
                        BallUpAndDown = 'Up'
                        BallUpAndDown_NUM = 1
                    #xxCSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)
                    #-------------------------落點判斷-------------------------
                    if BallUpAndDown == 'Down':
                        platform = 415
                        aid, hitthefall_number= DropPointCalculator.doDPC(BallCoordinate_Now, ball_speed, platform) #DropPointCalculator模組
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
                    #用於判斷對方即球前的三種擊球方式的落點位置
                        Max = max(Dropt_point_cut[0], Dropt_point_Forward_cut[0], Dropt_point_Reverse_cut[0])
                        Min = min(Dropt_point_cut[0], Dropt_point_Forward_cut[0], Dropt_point_Reverse_cut[0]) 
                        if Max == Dropt_point_cut[0]:
                            if Min == Dropt_point_Forward_cut[0]:
                                Mid = Dropt_point_Reverse_cut[0]
                            elif Min == Dropt_point_Reverse_cut[0]:
                                Mid = Dropt_point_Forward_cut[0]
                        elif Max == Dropt_point_Forward_cut[0]:
                            if Min == Dropt_point_Reverse_cut[0]:
                                Mid = Dropt_point_cut[0]
                            elif Min == Dropt_point_cut[0]:
                                Mid = Dropt_point_Reverse_cut[0]
                        else:
                            if Min == Dropt_point_Forward_cut[0]:
                                Mid = Dropt_point_cut[0]
                            elif Min == Dropt_point_cut[0]:
                                Mid = Dropt_point_Forward_cut[0]
                        Average = (Max + Min) / 2
                        print('avg-> ', Average, Mid)
                        if abs((PlatformY - PlatformY_2P) / ball_speed[1]) < ((Max - Average) / 5):
                            Average = (Max + Mid) / 2 
                            print('avg22-> ', Average)
                    #---------------------------------------------------------
                    #CSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM, Dropt_point[0]) #可視化用, 蒐集特徵
                    print('預測3個落點',Dropt_point_cut, Dropt_point_Forward_cut, Dropt_point_Reverse_cut)
                    print(BallUpAndDown, BallCoordinate_Now ,Dropt_point, ball_speed_Prediction, ball_speed, hitthefall_number, scene_info['frame'] )
                    
                    #-------------------------板子控制-----------------------
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

        #------------------------KNN------------------------
        if Mode == "KNN":
            filename = "D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/csv/1P的50總匯三明治.sav" #sav路徑
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
            if scene_info["status"] != "GAME_ALIVE": #判斷球狀態
                return "RESET"
                
            if not self.ball_served:
                self.Serve = random.randint(0,2) #亂數取0~2
                #print("Serve>>> ", self.Serve)
                if self.Serve == 1:
                    self.ball_served = True #設定球狀態
                    return "SERVE_TO_RIGHT" #往右發球
                if self.Serve == 2:
                    self.ball_served = True
                    return "SERVE_TO_LEFT" #往左發球
                else:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT" #往右發球
            else:
                BallCoordinate_Now = scene_info["ball"] #球當前位置
                ball_speed = scene_info["ball_speed"] #當前球速度
                PlatformX_1P = scene_info["platform_1P"][0] + 20 #當前1P板子 X
                PlatformY_1P = scene_info["platform_1P"][1] + 20 #當前1P板子 Y
                PlatformX_2P = scene_info["platform_2P"][0] + 20 #當前2P板子 X
                PlatformY_2P = scene_info["platform_2P"][1] + 20 #當前2P板子 Y        
                aid = 0 #用於計算落點值
                
                if ball_speed[0] != 0: #防Bug用, 未發球時球會是0
                    m = ball_speed[1] / ball_speed[0] #斜率
                    aid = BallCoordinate_Now[0] + ((420 - BallCoordinate_Now[1]) / ball_speed[1] * ball_speed[0]) #計算球落點
                    
                    #判斷打到牆壁後
                    if aid < 0:
                        aid = -aid
                    if aid > 195:
                        if aid > 390:
                            aid = aid -390
                        else:
                            aid = 195 - (aid - 195)
                            
                    #knn測試用, 擊球後讓值為100
                    if ball_speed[1] < 0:
                        aid = 100

                input = [] #輸入給knn模型之陣列
                inp_temp = np.array([PlatformX_1P, PlatformY_1P, BallCoordinate_Now[0], BallCoordinate_Now[1], ball_speed[0], ball_speed[1]]) #特徵: 1P板子X, 2P板子Y, 球當前X, 球當前Y, 球速X, 球速Y
                input = inp_temp[np.newaxis, :] #增加維度
                move = model.predict(input) #模型運算解果
                #print("input>>> ", move)
                
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
        self.ServePosition = random.randrange(20,180, 5) #隨機發球用, 板子亂數位置
        self.ball_served = False