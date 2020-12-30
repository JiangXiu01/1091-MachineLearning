import pickle
import random
from os import listdir
from os.path import isfile, isdir, join
import csv


mypath = "D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/"
files = listdir(mypath)
with open('./Log.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['frame', 'status', 'ball', 'ball_speed', 'platform_1P', 'platform_2P'])
    
    for LogFile in files:
        LOGFILE = mypath + "/" + LogFile 
        
        with open(LOGFILE, "rb") as f:
            p = pickle.load(f)

        print("Record format version:", p["record_format_version"])
        for ml_name in p.keys():
            if ml_name == "record_format_version":
                continue
            target_record = p[ml_name]
            random_id = random.randrange(len(target_record["scene_info"]))
            print("Scene information:", target_record["scene_info"][random_id])
            #print("Command:", target_record["command"][random_id])           
