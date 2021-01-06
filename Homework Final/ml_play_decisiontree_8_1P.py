"""
The template of the script for the machine learning process in game pingpong
"""
import math
import pickle
import numpy as np
# import decisiontree
class MLPlay:
	def __init__(self, side):	   
	
		self.ball_served = False
		self.side = side
		filename1 = "D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-pingpong-master/my_tree_1P_new.sav"
		self.model = pickle.load(open(filename1,'rb'))
		self.cmd_1P =  "NONE"
		self.ball_location = [0,0]		
	def update(self,scene_info): 
		self.side == "1P"
		# ball_location = [0,0]
		if scene_info["status"] != "GAME_ALIVE":
			return "RESET"

		if not self.ball_served:
			self.ball_served = True
			return "SERVE_TO_LEFT"
	
	
	# 3. Start an endless loop
		if self.side == "1P":
			while True:
				last_ball_location = self.ball_location
			
				self.ball_location = scene_info["ball"]				   
				if scene_info["status"] == "GAME_1P_WIN" or \
					scene_info["status"] == "GAME_2P_WIN":
				# Some updating or reseting code here
					
					continue
				if(int(last_ball_location[1]) - int(self.ball_location[1]) < 0):
					# go to down
					if(int(last_ball_location[0]) - int(self.ball_location[0]) < 0):
						   #go RD
						LRUP = 2
					else:
						LRUP = 1
							#go LD
				else:
					#upping
					if(int(last_ball_location[0]) - int(self.ball_location[0]) < 0):
						   #go RU
						LRUP = 4
					else:
						LRUP = 3
							#go LU
				# print(last_ball_location)
				# print(self.ball_location)
				# print(LRUP)
				inp_temp = [scene_info["ball"][0],scene_info["ball"][1],LRUP, \
								 (200 - int(scene_info["ball"][0]))]

				move = str(self.model.classify_test(inp_temp))
				# print(move)
				try:
					ans = move[1:3]
					ans = int(ans) *10
				except:
					ans = move[1:2]
					ans = int(ans) *10
				# print("1P ANS = {}".format(ans))
				if(scene_info["platform_1P"][0] +20 > ans):
					self.cmd_1P = "MOVE_LEFT"
					return self.cmd_1P
				elif(scene_info["platform_1P"][0] +20 < ans):
					self.cmd_1P = "MOVE_RIGHT"
					return self.cmd_1P
				else:
					self.cmd_1P = "NONE"
					return self.cmd_1P
		# else:	 

				
		#	  while True:
		#		  last_ball_location = ball_location				
		#		  ball_location = scene_info["ball"]
			
		#		  if scene_info["status"] == "GAME_1P_WIN" or \
		#			  scene_info["status"] == "GAME_2P_WIN":
		#		  # Some updating or reseting code here
				
		#			  continue
		#		  if(int(last_ball_location[1]) - int(ball_location[1]) > 0):
		#			  # go to up
					
		#			  if(int(last_ball_location[0]) - int(ball_location[0]) > 0):
		#					 #go LU
		#				  LRUP = 1
		#			  else:
		#				  LRUP = 2
		#					  #go RU
		#		  else:
		#			  #down
		#			  if(int(last_ball_location[0]) - int(ball_location[0]) > 0):
		#					 #go LD
		#				  LRUP = 3
		#			  else:
		#				  LRUP = 4
		#					  #go RD	   
				
		#		  inp_temp = [scene_info["ball"][0],scene_info["ball"][1],LRUP, \
		#						   (200 - int(scene_info["ball"][0]))]
		#		  move = str(self.model_2P.classify_test(inp_temp))
		#		  # print(move)
		#		  try:
		#			  ans = move[1:3]
		#			  # print(ans)
		#			  ans = int(ans) *10
		#		  except:
		#			  ans = move[1:2]
		#			  ans = int(ans) *10
		#		  if(ans<50 and scene_info.ball_speed == 21 ):
				
		#			  ans += 10
		#		  # print("2P ANS = {}".format(ans))
		#		  if(scene_info["platform_2P"][0] +20 > ans):

		#			  self.cmd_2P = "MOVE_LEFT"
		#			  # print("2P_LEFT")
		#			  return self.cmd_2P
		#		  elif(scene_info["platform_2P"][0] +20 < ans):
		#			  self.cmd_2P = "MOVE_RIGHT"
		#			  # print("2P_RIGHT")
		#			  return self.cmd_2P
		#		  else:
		#			  self.cmd_2P = "NONE"
		#			  # print("2P_NONE")
		#			  return self.cmd_2P
	
	def reset(self):
		"""
		Reset the status
		"""
		self.ball_served = False
