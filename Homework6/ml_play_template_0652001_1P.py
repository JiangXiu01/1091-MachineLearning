from games.pingpong.ml.Moduls import CSV_Read_1P
from games.pingpong.ml.Moduls import DropPointCalculator
import math
import time
import os

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

    def update(self, scene_info):
        # Make the caller to invoke reset() for the next round.
        if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
            print('GAME_2P_WIN!!!')
            Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            print(Time)
            time.sleep(1.5)
            print('Discard failed LOGs=> ' + 'ml_NORMAL_20_' + Time + '.pickle')
            os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/ml_NORMAL_20_' + Time + '.pickle')


        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
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
            CSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)
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
                Average = (Max + Min) / 2
            #---------------------------------------------------------
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
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False