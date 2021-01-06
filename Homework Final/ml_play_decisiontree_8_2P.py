"""
The template of the script for the machine learning process in game pingpong
"""
import math
import pickle
import numpy as np
import random
# import decisiontree

class MLPlay:
    def __init__(self, side):        
        self.ball_served = False
        self.side = side        
        filename = 'D:/※NKFUST/00-學期科目資料/109 academic year/MLGame-master/my_tree_2P_new.sav'
        self.model_2P = pickle.load(open(filename,'rb'))
        self.cmd_2P = "NONE"
        self.ball_location = [0,0]
        self.ServePosition = random.randrange(20,180, 5)
        
    def update(self,scene_info):       
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
        self.side == "2P"
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
    
    

        if self.side == "2P":  

                
            while True:
                last_ball_location = self.ball_location                
                self.ball_location = scene_info["ball"]
            
                if scene_info["status"] == "GAME_1P_WIN" or \
                    scene_info["status"] == "GAME_2P_WIN":
                # Some updating or reseting code here
                
                    continue
                if(int(last_ball_location[1]) - int(self.ball_location[1]) > 0):
                    # go to up
                    
                    if(int(last_ball_location[0]) - int(self.ball_location[0]) > 0):
                           #go LU
                        LRUP = 1
                    else:
                        LRUP = 2
                            #go RU
                else:
                    #down
                    if(int(last_ball_location[0]) - int(self.ball_location[0]) > 0):
                           #go LD
                        LRUP = 3
                    else:
                        LRUP = 4
                            #go RD       
                
                inp_temp = [scene_info["ball"][0],scene_info["ball"][1],LRUP, \
                                 (200 - int(scene_info["ball"][0]))]
                move = str(self.model_2P.classify_test(inp_temp))
                
                print(move)
                try:
                    ans = move[1:3]
                    # print(ans)
                    ans = int(ans) *10
                except:
                    ans = move[1:2]
                    ans = int(ans) *10
                if(ans<50 and abs(scene_info["ball_speed"][1]) >= 21 ):
                
                    ans += 10
                if(scene_info["platform_2P"][0] +20 > ans):
                    # print("2P_LEFT")
                    return "MOVE_LEFT"
                elif(scene_info["platform_2P"][0] +20 < ans):
                    # print("2P_RIGHT")
                    return "MOVE_RIGHT"
                else:
                    # print("2P_NONE")
                    return "NONE"
                    

    def reset(self):
        """
        Reset the status
        """
        self.ServePosition = random.randrange(20,180, 5)
        self.ball_served = False
