#!/usr/bin/python

import random

lab_matrix=[]
crossroads=[]
def sum_position(x,y):
	return [sum(i) for i in zip(x,y)]

def set_lab_matrix(position,value):
	global lab_matrix
	lab_matrix[position[0]][position[1]]=value

def get_lab_matrix(position):
	return lab_matrix[position[0]][position[1]]

def print_labyrinth(x):
	x = zip(*x[::1])
	print '\033[41m\b','  ' * (len(x[0])+2),'\033[49m\b'
	for i in x:
		print '\033[41m\b','  ',
		for j in i:
			if j==0 or j==2:
				print '\033[40m\b',
			elif j==1:
				print '\033[49m\b',
			print ' ','\033[49m\b',
		print '\033[41m\b',' ','\033[49m\b'
	print '\033[41m\b','  ' * (len(x[0])+2),'\033[49m\b'
	print '\033[49m\b',

def next_way(cur_pos):
	exit_is_near=False
	next_alt = [(-1,0),(1,0),(0,-1),(0,1)]
	next_pos = [sum_position(pos,cur_pos) for pos in next_alt]
	possible_next_pos = [pos for pos in next_pos if \
						pos[0]<=len(lab_matrix)-1 and \
						pos[1]<=len(lab_matrix[pos[0]])-1 and \
						get_lab_matrix(pos)==0]
	next_pos=[]
	for pos in possible_next_pos:
		tmp=0
		for pos_alt in next_alt:
			tmp_pos=sum_position(pos,pos_alt)
			if tmp_pos[0]<=len(lab_matrix)-1 and tmp_pos[1]<=len(lab_matrix[tmp_pos[0]])-1:
				if get_lab_matrix(tmp_pos)==1:
					tmp+=1
				if get_lab_matrix(tmp_pos)==3:
					tmp=0
					next_pos=[pos]
					break
		if tmp==1:
			next_pos.append(pos)
	if len(next_pos)>1:
		crossroads.append(cur_pos)
	if len(next_pos)==0:
		if cur_pos in crossroads:
			crossroads.remove(cur_pos)
		if len(crossroads)>0:
			return crossroads[0]
		else:
			return (-1,-1)
	if exit_is_near:
		next_pos=sorted(next_pos,key=lambda x: x[0]+x[1], reverse=True)[0]
	else:
		next_pos=random.choice(next_pos)
	return next_pos

def gen_labyrinth(x_size,y_size):
	global lab_matrix
	lab_matrix=[[0]*y_size for i in range(0,x_size)]
	for i,array in enumerate(lab_matrix):
		for j,integer in enumerate(array):
			if i==0 or j==0:
				set_lab_matrix([i,j],2)
			elif i==len(lab_matrix)-1 or j==len(lab_matrix[i])-1:
				set_lab_matrix([i,j],2)
	set_lab_matrix(start,1)
	set_lab_matrix(end,3)
	current_position = start
	finished=False
	i=0
	while finished==False:
		current_position=next_way(current_position)
		if current_position==end:
			finished=True
		elif current_position[0]<0:
			finished=True
		else:
			set_lab_matrix(current_position,1)
	return lab_matrix

X_SIZE=25
Y_SIZE=25
import time
error_count=0
for i in range(0,1000):
	start=(0,random.randint(1,X_SIZE-2))
	end=(Y_SIZE-1,random.randint(1,Y_SIZE-2))
	labyrinth = gen_labyrinth(X_SIZE,Y_SIZE)
	if get_lab_matrix(sum_position(end,(-1,0)))==0:
		error_count+=1
print "Error percent: %f" %(float(error_count)/1000)  
	#print '\033[%iA\r' %(Y_SIZE+3)


