import csv


def doWrite(Frame, BallX, BallY, m, ball_speedX,  ball_speedY, PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM):
     with open('./1P_Log.csv', 'a+', newline='') as csvfile: #a+ => 追加
        writer = csv.writer(csvfile)
        writer.writerow([Frame, BallX, BallY, m, ball_speedX, ball_speedY, PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM])