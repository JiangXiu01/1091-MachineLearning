"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
import pickle
import numpy as np
import time
import os

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """
    #left - right => 0 - 195
    # === Here is the execution order of the loop === #
    
    Mode = "KNN" #KNN or RULE
    LastTimeBallCoordinate = [0,0]
    
    if Mode == "RULE":
        aid = 0
        m = 1
        comm.ml_ready()
        BallDirection = ''
        BallUpAndDown = ''
        BallRebound = '' #方向
        LastTimeBallCoordinateBallRebound = ''
        PlatformX = 0
        while True:
            scene_info = comm.get_scene_info()

            if scene_info.status == GameStatus.GAME_OVER: #移除失敗log檔, 以利學習
                print ('GAME OVER!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                print(Time)
                #time.sleep(1.5)
                os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame/games/arkanoid/log/' + Time + '.pickle')
            
            if scene_info.status == GameStatus.GAME_OVER or \
                scene_info.status == GameStatus.GAME_PASS:
                comm.ml_ready()
                if GameStatus.GAME_OVER:
                    print('GAME OVER!')
                continue

            BallCoordinate = scene_info.ball
            PlatformX = scene_info.platform[0] + 20
            if BallCoordinate[0] - LastTimeBallCoordinate[0] > 0:
                BallDirection = 'Right'
            else:
                BallDirection = 'Left'

            if BallCoordinate[1] - LastTimeBallCoordinate[1] > 0:
                BallUpAndDown = 'Down'
            else:
                BallUpAndDown = 'Up'

            m = (BallCoordinate[1] - LastTimeBallCoordinate[1]) / (BallCoordinate[0] - LastTimeBallCoordinate[0])
            #print(BallCoordinate[1], ' - ', LastTimeBallCoordinate[1], '  ',BallCoordinate[0], ' ',LastTimeBallCoordinate[0])
            aid = BallCoordinate[0] + ((395 - BallCoordinate[1]) / m)
            if aid < 0:
                aid = -aid
            elif aid > 200:
                aid = aid - 200
                aid = 200 - aid

            if BallUpAndDown == 'Down' and m == 1:
                BallRebound = '↘'
            elif BallUpAndDown == 'Down' and m == -1:
                BallRebound = '↙'
            elif BallUpAndDown == 'Up' and m == -1:
                BallRebound = '↗'
            elif BallUpAndDown == 'Up' and m == 1:
                BallRebound = '↖'
            else:
                BallRebound = 'Collision'
            print('ballY=> ', BallCoordinate[1],'BallX=> ', BallCoordinate[0], '  PlatformX=> ', PlatformX, '  aid=> ', aid,'  BallRebound=> ', BallRebound)
            '''
            #4關卡:
            ######################################################################
            if PlatformX > aid and BallUpAndDown == 'Down' and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if PlatformX < aid and BallUpAndDown == 'Down'and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

            if BallRebound == '↗' and BallUpAndDown == 'Up' and 280 > BallCoordinate[1] > 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if BallRebound == '↖' and BallUpAndDown == 'Up'and 280 > BallCoordinate[1] > 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

            if BallCoordinate[0] > LastTimeBallCoordinate[0] and BallCoordinate[1] > 280:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            if BallCoordinate[0] < LastTimeBallCoordinate[0] and BallCoordinate[1] > 280:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)


            if BallUpAndDown == 'Up' and PlatformX < 100 and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                if PlatformX == 100:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            if BallUpAndDown == 'Up' and PlatformX > 100 and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                if PlatformX == 100:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            ######################################################################
            '''
            
            #1~3,5關卡:
            ######################################################################
            if PlatformX > aid and BallUpAndDown == 'Down':
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            if PlatformX < aid and BallUpAndDown == 'Down':
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            if BallUpAndDown == 'Up' and PlatformX < 100 and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                if PlatformX == 100:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            if BallUpAndDown == 'Up' and PlatformX > 100 and BallCoordinate[1] < 200:
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                if PlatformX == 100:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            ######################################################################
            
            LastTimeBallCoordinate = BallCoordinate
            LastTimeBallCoordinateBallRebound = BallRebound
            
    if Mode == "KNN":
        past_ball_position = []
        comm.ml_ready()
        filename = "knn_0652001.sav"
        model = pickle.load(open(filename, 'rb')) 
        while True:

            scene_info = comm.get_scene_info()
            now_ball_position = scene_info.ball

            if len(past_ball_position) != 0:
                inp_temp = np.array([past_ball_position[0], past_ball_position[1], now_ball_position[0], now_ball_position[1], scene_info.platform[0]])
                input = inp_temp[np.newaxis, :]
                
                if scene_info.status == GameStatus.GAME_OVER: #移除失敗log檔, 以利學習
                    print ('GAME OVER!!!')
                    Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    print('Remove failed log: ' + Time + '.pickle')
                    time.sleep(1)
                    os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame/games/arkanoid/log/' + Time + '.pickle')

                if scene_info.status == GameStatus.GAME_OVER or \
                    scene_info.status == GameStatus.GAME_PASS:
                    comm.ml_ready()
                    continue
                move = model.predict(input)

                if move < 0:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif move > 0:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)    
            past_ball_position = now_ball_position