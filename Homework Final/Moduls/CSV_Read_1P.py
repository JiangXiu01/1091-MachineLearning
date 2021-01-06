import csv


def doWrite(Frame, BallX, BallY, m, ball_speedX,  ball_speedY, PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM, Dropt_point, Dropt_point_cut, Dropt_point_Forward_cut,Dropt_point_Reverse_cut):
     with open('./1P_Log.csv', 'a+', newline='') as csvfile: #a+ => 追加
        writer = csv.writer(csvfile)
        writer.writerow([Frame, BallX, BallY, m, ball_speedX, ball_speedY, PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM, Dropt_point, Dropt_point_cut, Dropt_point_Forward_cut,Dropt_point_Reverse_cut])