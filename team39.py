import random
import sys
import numpy
import copy
import datetime
# put in board [ old_move[0]%4 ] [ old_move[1]%4 ]
class Team39:
	def __init__(self):
		self.alpha=-10000000000000
		self.beta=10000000000000
		self.dict={}
		self.limit = datetime.timedelta(seconds = 15.4)
		self.start = 0
		self.bonus = 0

	def convert1(self, board):
		a=[[[[0 for i in range(4)]for j in range(4)]for k in range(4)]for l in range(4)]
		for i in range(16):
			for j in range(16):
				a[i//4][j//4][i%4][j%4] = board[i][j]
		return a

	def move(self, board, old_move, flag):
		z=self.convert1(board.board_status)
		# new board => old_move%4
		# old board => old_move//4
		x = old_move[0]%4
		y = old_move[1]%4
		k=0
		self.start=datetime.datetime.utcnow()
		depth = 3
		board_copy = copy.deepcopy(board)
		while(datetime.datetime.utcnow() - self.start < self.limit):
			alpha = -10000000000000
			beta = 10000000000000
			temp=self.minimax(True, 0, depth, z, board_copy, old_move, alpha, beta, flag, (-1, -1))
			if(temp['value']!=-1):
				k=temp
			depth+=1

		print k
		return k['best_answer']		
		#return cells[random.randrange(len(cells))]


	def minimax(self, check_max, k, n, board, boardclass, old_move, alpha, beta, flag, best_answer):
		#printboard(board)
		#print flag
		if datetime.datetime.utcnow() - self.start > self.limit:
			return {'value':-1,'best_answer':(-1,-1)}
		if flag=='x':
			antiflag='o'
		else:
			antiflag='x'

		leaf_state = boardclass.find_terminal_state()
		if(leaf_state[1]=='WON'):
			if(leaf_state[0]==flag):
				return {'value':100000000,'best_answer': old_move}
			elif(leaf_state[0]==antiflag):
				return {'value':-100000000,'best_answer': old_move}


		wins = [[1,0,0,0,1,0,0,0,0,0,0,0],
				[1,0,0,0,0,1,0,0,1,0,0,0],
				[1,0,0,0,0,0,1,0,0,1,0,0],
				[1,0,0,0,0,0,0,1,0,0,0,0],
				[0,1,0,0,1,0,0,0,1,0,0,0],
				[0,1,0,0,0,1,0,0,0,1,1,0],
				[0,1,0,0,0,0,1,0,1,0,0,1],
				[0,1,0,0,0,0,0,1,0,1,0,0],
				[0,0,1,0,1,0,0,0,0,0,1,0],
				[0,0,1,0,0,1,0,0,1,0,0,1],
				[0,0,1,0,0,0,1,0,0,1,1,0],
				[0,0,1,0,0,0,0,1,0,0,0,1],
				[0,0,0,1,1,0,0,0,0,0,0,0],
				[0,0,0,1,0,1,0,0,0,0,1,0],
				[0,0,0,1,0,0,1,0,0,0,0,1],
				[0,0,0,1,0,0,0,1,0,0,0,0]]

		opp=self.makeopp(board, flag, antiflag, wins)
		myp=self.makemyp(board, flag, antiflag, wins)
		megaopp=self.makemega_opp(opp, myp, board, wins)
		megamyp=self.makemega_myp(opp, myp, wins)
		block_status = self.make_blockstatus(opp, myp, board, flag, antiflag)



		if self.checkempty(board):
			#print("checkwin: ", checkwin(board)) 
			ans = self.maincost(opp, myp, megaopp, megamyp, board, block_status, flag, antiflag)
			return {'value':ans, 'best_answer':old_move}

		if(k==n):
			ans = self.maincost(opp, myp, megaopp, megamyp, board, block_status, flag, antiflag)
			return {'value':ans, 'best_answer':old_move}

		else:
			empty = boardclass.find_valid_move_cells(old_move)
			random.shuffle(empty)

			if(len(empty)==0):
				ans = self.maincost(opp, myp, megaopp, megamyp, board, block_status, flag, antiflag)
				return {'value':ans, 'best_answer':old_move}
	#minimizing
			if not(check_max):
				for i in empty:
					#square[i]=1
					return_value=boardclass.update(old_move, i, antiflag)
					board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]=antiflag
					if(return_value[1]==True and self.bonus==0):
						self.bonus = 1
						ans = self.minimax(False, k+1, n, board, boardclass, i, alpha, beta, flag, best_answer)
					else:
						if(self.bonus==1): self.bonus = 0
						ans = self.minimax(True, k+1, n, board, boardclass, i, alpha, beta, flag, best_answer)
					if datetime.datetime.utcnow() - self.start > self.limit:
						boardclass.board_status[i[0]][i[1]]='-'
						boardclass.block_status[i[0]//4][i[1]//4]='-'
						board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]='-'	
						return {'value':-1,'best_answer':(-1, -1)}

					if(ans['value']<beta):
						beta = ans['value']
						best_answer = i

					boardclass.board_status[i[0]][i[1]]='-'
					boardclass.block_status[i[0]//4][i[1]//4]='-'
					board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]='-'
					
					if beta <= alpha:break
				return {'value':beta,'best_answer':best_answer}
	#maximizing
			elif check_max:
				for i in empty:
					return_value=boardclass.update(old_move, i, flag)
					board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]=flag
					if(return_value[1]==True and self.bonus==0):
						self.bonus = 1
						ans = self.minimax(True, k+1, n, board, boardclass, i, alpha, beta, flag, best_answer)
					else:
						if(self.bonus==1): self.bonus = 0
						ans=self.minimax(False, k+1, n, board, boardclass, i, alpha, beta, flag, best_answer)
					if datetime.datetime.utcnow() - self.start > self.limit:
						boardclass.board_status[i[0]][i[1]]='-'
						boardclass.block_status[i[0]//4][i[1]//4]='-'
						board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]='-'
						return {'value':-1,'best_answer':(-1, -1)}
					
					if(ans['value']>alpha):
						alpha = ans['value']
						best_answer = i

					boardclass.board_status[i[0]][i[1]]='-'
					boardclass.block_status[i[0]//4][i[1]//4]='-'
					board[i[0]//4][i[1]//4][i[0]%4][i[1]%4]='-'
					
					if beta <= alpha:break
				return {'value':alpha,'best_answer':best_answer}
				 

	def calc_board_utility(self, myp, opp, board, flag, antiflag):
		demo_block = tuple([tuple(board[i]) for i in range(4)])
		if(demo_block, flag) in self.dict:
			return self.dict[(demo_block, flag)]

		ans = 0

	# adding values according to position priority
		if(board[1][1]==flag): ans+=2
		if(board[1][2]==flag): ans+=2
		if(board[2][1]==flag): ans+=2
		if(board[2][2]==flag): ans+=2

		if(board[0][1]==flag): ans+=1
		if(board[0][2]==flag): ans+=1
		if(board[1][0]==flag): ans+=1
		if(board[2][0]==flag): ans+=1
		if(board[3][1]==flag): ans+=1
		if(board[3][2]==flag): ans+=1
		if(board[1][3]==flag): ans+=1
		if(board[2][3]==flag): ans+=1

		if(board[1][1]==antiflag): ans-=2
		if(board[1][2]==antiflag): ans-=2
		if(board[2][1]==antiflag): ans-=2
		if(board[2][2]==antiflag): ans-=2

		if(board[0][1]==antiflag): ans-=1
		if(board[0][2]==antiflag): ans-=1
		if(board[1][0]==antiflag): ans-=1
		if(board[2][0]==antiflag): ans-=1
		if(board[3][1]==antiflag): ans-=1
		if(board[3][2]==antiflag): ans-=1
		if(board[1][3]==antiflag): ans-=1
		if(board[2][3]==antiflag): ans-=1

		for i in range(12):
			if(myp[i]==4 and opp[i]==0): ans+=2500
			if(myp[i]==3 and opp[i]==0): ans+=500
			#if(myp[i]==3 and opp[i]==1): ans-=5
			if(myp[i]==2 and opp[i]==0): ans+=100
			if(myp[i]==1 and opp[i]==0): ans+=20
			if(myp[i]==0 and opp[i]==4): ans-=2500
			if(myp[i]==0 and opp[i]==3): ans-=500
			if(myp[i]==1 and opp[i]==3): ans+=5
			#if(myp[i]==1 and opp[i]==2): ans+=2
			#if(myp[i]==1 and opp[i]==1): ans+=2
			if(myp[i]==0 and opp[i]==2): ans-=100
			if(myp[i]==0 and opp[i]==1): ans-=20

		self.dict[(demo_block, flag)] = ans
		return ans

	def makeopp(self, board, flag, antiflag, wins):
		opp = [[0 for i in range(12)] for j in range(16)]
		for i in range(4):
			for j in range(4):
				for k in range(4):
					for l in range(4):
						if(board[i][j][k][l]!='-' and board[i][j][k][l]==antiflag):
							opp[4*i+j]=numpy.array(opp[4*i+j])+numpy.array(wins[4*k+l])
		return opp

	def makemyp(self, board, flag, antiflag, wins):
		myp = [[0 for i in range(12)] for j in range(16)]
		for i in range(4):
			for j in range(4):
				for k in range(4):
					for l in range(4):
						if(board[i][j][k][l]!='-' and board[i][j][k][l]==flag):
							myp[4*i+j]=numpy.array(myp[4*i+j])+numpy.array(wins[4*k+l])
		return myp

	def makemega_opp(self, opp, myp, board, wins):
		megaopp = [0 for i in range(12)]
		for i in range(16):
			if(self.checkfinish(board[i//4][i%4]) and not(self.checkwin(board[i//4][i%4]))):
				megaopp=numpy.array(megaopp)+numpy.array(wins[i])
				continue
			for j in range(12):
				if(opp[i][j]==4 and myp[i][j]==0):
					megaopp=numpy.array(megaopp)+numpy.array(wins[i])
					break
		return megaopp

	def make_blockstatus(self, opp, myp, board, flag, antiflag):
		block_status = [['-' for i in range(4)] for j in range(4)]
		for i in range(16):
			if(self.checkfinish(board[i//4][i%4]) and not(self.checkwin(board[i//4][i%4]))):
				block_status[i//4][i%4]='d'
				continue
			for j in range(12):
				if(opp[i][j]==4 and myp[i][j]==0):
					block_status[i//4][i%4]=antiflag
					break

		for i in range(16):
			for j in range(12):
				if(myp[i][j]==4 and opp[i][j]==0):
					block_status[i//4][i%4]=flag
					break

		return block_status

	def makemega_myp(self, opp, myp, wins):
		megamyp = [0 for i in range(12)]
		for i in range(16):
			for j in range(12):
				if(myp[i][j]==4 and opp[i][j]==0):
					megamyp=numpy.array(megamyp)+numpy.array(wins[i])
					break
		return megamyp


	def maincost(self, opp, myp, megaopp, megamyp, board, block_status, flag, antiflag):
		priority = 0
		temp_main=200*self.cost(megamyp, megaopp, block_status, flag, antiflag)
		priority+=temp_main
		#print block_status
		#print temp_main
		for i in range(4):
			for j in range(4):
				if(block_status[i][j]=='-'):
					temp_ans=self.cost(myp[4*i+j], opp[4*i+j], board[i][j], flag, antiflag)
					priority+=temp_ans
				elif(block_status[i][j]==flag):
					priority+=5000
				elif(block_status[i][j]==antiflag):
					priority-=5000
		#print tsum
		return priority

	def cost(self, myp, opp, board, flag, antiflag):
		#print "priority: ", priority
		return self.calc_board_utility(myp, opp, board, flag, antiflag)

	def find_available(self, board):
		a=[]
		for i in range(4):
			for j in range(4):
				if(not(self.sub_win(board, (i, j)) or self.sub_finish(board, (i, j)))):
					a.append(4*i+j)
		return a

	def sub_win(self, board, old_move):
		x = old_move[0]%4
		y = old_move[1]%4
		#print board[x][y]
		return self.checkwin(board[x][y])

	def sub_finish(self, board, old_move):
		x = old_move[0]%4
		y = old_move[1]%4
		for i in range(4):
			if '-' in board[x][y][i]:
				return 0
		return 1

	def checkfinish(self, board):
		for i in range(4):
			if '-' in board[i]:
				return 0
		return 1

	def checkempty(self, board):
		for i in range(4):
			for j in range(4):
				for k in range(4):
					if '-' in board[i][j][k]:
						return 0
		return 1

	def checkmainwin(self, board, old_move):
		for i in range(4):
			for j in range(4):
				if(not(self.checkwin(board[i][j])) and not(self.checkfinish(board[i][j]))):
					return 0
		return 1

	def checkwin(self, board):
		if(board[0][0]!="-" and board[0][0]==board[0][1] and board[0][0]==board[0][2] and board[0][0]==board[0][3]):
			#print("row 1")
			return 1
		if(board[1][0]!="-" and board[1][0]==board[1][1] and board[1][0]==board[1][2] and board[1][0]==board[1][3]):
			#print("row 2")
			return 1
		if(board[2][0]!="-" and board[2][0]==board[2][1] and board[2][0]==board[2][2] and board[2][0]==board[2][3]):
			#print("row 3")
			return 1
		if(board[3][0]!="-" and board[3][0]==board[3][1] and board[3][0]==board[3][2] and board[3][0]==board[3][3]):
			#print("row 4")
			return 1
		if(board[0][0]!="-" and board[0][0]==board[1][0] and board[0][0]==board[2][0] and board[0][0]==board[3][0]):
			#print("col 1")
			return 1
		if(board[0][1]!="-" and board[0][1]==board[1][1] and board[0][1]==board[2][1] and board[0][1]==board[3][1]):
			#print("col 2")
			return 1
		if(board[0][2]!="-" and board[0][2]==board[1][2] and board[0][2]==board[2][2] and board[0][2]==board[3][2]):
			#print("col 3")
			return 1
		if(board[0][3]!="-" and board[0][3]==board[1][3] and board[0][3]==board[2][3] and board[0][3]==board[3][3]):
			#print("col 4")
			return 1
		if(board[0][1]!="-" and board[0][1]==board[1][0] and board[0][1]==board[2][1] and board[0][1]==board[1][2]):
			#print("tl diamond")
			return 1
		if(board[0][2]!="-" and board[0][2]==board[1][1] and board[0][2]==board[2][2] and board[0][2]==board[1][3]):
			#print("tr diamond")
			return 1
		if(board[1][2]!="-" and board[1][2]==board[2][1] and board[1][2]==board[3][2] and board[1][2]==board[2][3]):
			#print("br diamond")
			return 1
		if(board[1][1]!="-" and board[1][1]==board[2][0] and board[1][1]==board[3][1] and board[1][1]==board[2][2]):
			#print("bl diamond")
			return 1
		# if(board[1][1]!="-" and board[1][1]==board[1][1] and board[0][0]==board[2][2]):
		# 	return 1
		# if(board[2][1]!="-" and board[2][1]==board[1][1] and board[2][1]==board[0][2]):
		# 	return 1
		else: return 0