import math

def doAttack(aid, ball_speed, PlatformX_2P, BallUpAndDown, BallCoordinate_Now):

    if (ball_speed[1] != 0 or ball_speed[0] != 0) and BallUpAndDown == 'Down':
    
        #正常方式擊球落點計算
        m_Normal = ball_speed[1] / ball_speed[0]
        aid_Normal = BallCoordinate_Now[0] + (math.ceil((415 - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
        print("doAttack==>", aid, math.ceil((415 - BallCoordinate_Now[1]) / ball_speed[1]))
        