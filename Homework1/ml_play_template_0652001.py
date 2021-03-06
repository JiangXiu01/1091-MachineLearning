"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

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

    LastTimeBallCoordinate = [0,0]
    result = 0
    m = 1
    comm.ml_ready()
    BallDirection = ''
    BallUpAndDown = ''
    BallRebound = '' #方向
    LastTimeBallCoordinateBallRebound = ''
    PlatformX = 0
    while True:
        scene_info = comm.get_scene_info()

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
        result = BallCoordinate[0] + ((395 - BallCoordinate[1]) / m)
        if result < 0:
            result = -result
        elif result > 200:
            result = result - 200
            result = 200 - result

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
        print('ballY=> ', BallCoordinate[1],'BallX=> ', BallCoordinate[0], '  PlatformX=> ', PlatformX, '  result=> ', result,'  BallRebound=> ', BallRebound)
        '''
        #4關卡:
        ######################################################################
        if PlatformX > result and BallUpAndDown == 'Down' and BallCoordinate[1] < 200:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        if PlatformX < result and BallUpAndDown == 'Down'and BallCoordinate[1] < 200:
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
        if PlatformX > result and BallUpAndDown == 'Down':
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        if PlatformX < result and BallUpAndDown == 'Down':
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