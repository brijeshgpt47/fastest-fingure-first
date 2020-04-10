import sys
from termcolor import colored, cprint
import time
import pygame
import os
import subprocess
import RPi.GPIO as GPIO

#pygame.init()
def pinRefresh():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)#player no 1 button connection
	GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)#no 2
	GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_UP)#no 3
	GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)#no 3
	GPIO.add_event_detect(11,GPIO.FALLING)
	GPIO.add_event_detect(13,GPIO.FALLING)
	GPIO.add_event_detect(15,GPIO.FALLING)
	GPIO.add_event_detect(16,GPIO.FALLING)
	GPIO.setup(18,GPIO.OUT)# bulb connection for player no 1
	GPIO.setup(19,GPIO.OUT)# bulb connection for player no 2
	GPIO.setup(21,GPIO.OUT)# for 3
	GPIO.setup(23,GPIO.OUT)# for 4
	GPIO.output(18,True)
	GPIO.output(19,True)
	GPIO.output(21,True)
	GPIO.output(23,True)

def getButton(rank,timeUp,st,team1,team2,team3,team4,lockTime):
	while (timeUp < lockTime):
		if GPIO.event_detected(11):
			GPIO.remove_event_detect(11)
			GPIO.output(18,False)
			return ("		"+str(rank)+" === " + colored(team1,'red','on_white',attrs=['bold']))
			break
		if GPIO.event_detected(13):
			GPIO.remove_event_detect(13)
			GPIO.output(19,False)
			return ("		"+str(rank)+" === " + colored(team2,'blue','on_white',attrs=['bold']))
			break
		if GPIO.event_detected(15):
			GPIO.remove_event_detect(15)
			GPIO.output(21,False)
			return ("		"+str(rank)+" === " + colored(team3,'grey','on_white',attrs=['bold']))
			break
		if GPIO.event_detected(16):
			GPIO.remove_event_detect(16)
			GPIO.output(23,False)
			return ("		"+str(rank)+" === " + colored(team4,'magenta','on_white',attrs=['bold']))
			break
		countTime = time.clock()
		timeUp = countTime - st
		if (timeUp == lockTime):
			print("			TIME OUT !!!!")

def Question(timeUp,team1,team2,team3,team4,lockTime):
	pinRefresh()
	rank = 1
	period = 0
	st=time.clock()
	while (period < 4):
		team=getButton(rank,timeUp,st,team1,team2,team3,team4,lockTime)
		print (team)
		rank += 1
		period += 1

# main program
os.system('clear')

team1 = raw_input("\nEnter name of Team 1: ")
team2 = raw_input("Enter name of Team 2: ")
team3 = raw_input("Enter name of Team 3: ")
team4 = raw_input("Enter name of Team 4: ")
lockTime = input("Enter 'TimeUp' time in seconds: ")

os.system('clear')
quesNo = 0
flag = True

while(flag == True):
	pinRefresh()
	os.system('clear')
	timeUp = 0
	cprint("			QUIZ COMPETITION",'green','on_red',attrs=['bold','blink'])
	nextQue = input("	Press 1 to Start the game: ")
#	print ("\n	Test Your Indicators - Press the switches ")
	try:
		while 1:
			if (int(nextQue) != 0):
				cprint ("	QUESTION NO. - "+str(quesNo)+"\n",attrs=['underline','bold']) 
				GPIO.cleanup()
				Question(timeUp,team1,team2,team3,team4,lockTime)
				nextQue = input("\nPress 1 for next question or 0(Zero) to end the game: ")
				quesNo += 1
			if (int(nextQue) == 0):
				flag = False
				break
		GPIO.cleanup()
	except KeyboardInterrupt:
#		pinRefresh()
#		GPIO.setmode(GPIO.BOARD)
#		GPIO.setup(7,GPIO.OUT)
		quesNo += 1
		GPIO.cleanup()
