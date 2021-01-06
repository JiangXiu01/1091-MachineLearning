import math


def doDPC(BallCoordinate_Now, ball_speed, platform):
    aid = 0
    m = 1
    remainder_left = 0
    remainder_right = 0
    remainder_195 = 195 % ball_speed[0]
    hitthefall_number = 0 #撞牆次數
    if ball_speed[1] != 0 or ball_speed[0] != 0:
        m = ball_speed[1] / ball_speed[0]
        aid = BallCoordinate_Now[0] + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
        # print(aid, math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]))
    if aid < 0: #落點預測1 -左邊碰牆
        remainder_left = BallCoordinate_Now[0] % ball_speed[0]
        if aid < -195: #撞第二次牆
            remainder_left = remainder_left + remainder_195
            # print(remainder_left)
            if aid < -390: #撞第三次牆
                remainder_left = remainder_left + remainder_195
                aid = BallCoordinate_Now[0] - remainder_left + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
                aid = -aid
                aid = aid - 390
                hitthefall_number = 3
                # print('aid_-390-->',aid)
            else:
                aid = BallCoordinate_Now[0] - remainder_left + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
                aid = -aid
                aid = aid - 195
                aid = 195 - aid
                hitthefall_number = 2
                # print('aid_-195-->',aid)
        else:
            aid = BallCoordinate_Now[0] - remainder_left + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
            aid = -aid
            hitthefall_number = 1
            # print('aid_-0-->',aid ,remainder_left )
    if aid > 195: #落點預測1 -右邊碰牆
        if ((195 - BallCoordinate_Now[0]) % ball_speed[0]) == 0: #若餘數為0 直接定義餘數=0
            remainder_right = 0
        else:
            remainder_right = ball_speed[0] - ((195 - BallCoordinate_Now[0]) % ball_speed[0])
        if remainder_195 == 0: #若餘數為0 直接定義餘數=0
            remainder_195 = ball_speed[0]
        if aid > 390: #撞第二次牆
            remainder_right = remainder_right + (ball_speed[0] - remainder_195)
            if aid > 585: #撞第三次牆
                remainder_right = remainder_right + (ball_speed[0] - remainder_195)
                aid = BallCoordinate_Now[0] - remainder_right + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
                aid = aid - 585
                aid = 195 - aid
                hitthefall_number = 3
                # print('aid_585-->',aid)
            else:
                aid = BallCoordinate_Now[0] - remainder_right + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
                aid = aid - 390
                hitthefall_number = 2
                # print('aid_390-->',aid)
        else:
            aid = BallCoordinate_Now[0] - remainder_right + (math.ceil((platform - BallCoordinate_Now[1]) / ball_speed[1]) * ball_speed[0])
            aid = aid - 195
            aid = 195 - aid
            hitthefall_number = 1
            # print('aid_195-->',aid,remainder_right)
    return aid, hitthefall_number