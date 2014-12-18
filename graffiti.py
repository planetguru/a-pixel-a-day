#!/usr/bin/python

# A Pixel A Day
# @TODO - commit should register current position to enable restart
# first step would then be a git pull and seek to current bit position

import json
import time
import math
import sys
import subprocess
import os
import pprint

tableauFile = "tableau.txt"
tableauDir = "/export/a-pixel-a-day/" 
tableauDir = "/Users/clacy/Development/web/a-pixel-a-day/"
tableau = tableauDir + tableauFile
toPrint = "&YAHOO" # use & for testing. 

# prepare a basic log file
f = open('/tmp/pad-log.txt', 'a')
f.write("\nscript has started")
f.close()

workingDays = [1,2,3,4,5]

fontConfig = json.loads(open('font.json').read())
fontWidth = int(fontConfig['font']['fontWidth'])+1

startDay = int(time.time())/86400 # days since epoch where 86400 is no. seconds in a day
#startDay = int(time.time())/60 # minute-long days since epoch where 86400 is no. seconds in a day

def commit():
	today = int(time.time()/86400) + 0 

	global lastCommitDay
	logmessage("\ntoday is "+str(today)+" lastCommitDay is "+str(lastCommitDay))
	if today != lastCommitDay:
		# determine which letter I'm on
		day = today-sd

		# pixcol is the physical column on the display screen
		pixcol = day/7
		f = day%7
		if(f > 0):
			pixcol=pixcol+1

		# figure out which character in the printed string we are on today
		charindex = pixcol/5
		b = pixcol%5
		if(b==0 and charindex>0):
			charindex=charindex-1

		# determine which column of the letter spec from font definition
		if(b==0):
			col=5
		else:
			col=b

		# cast col to string
		col = str(col)
		# determine which bit of col
		if(f==0):
			bit = 6
		else:
			bit = f-1

		# determine whether or not to commit
		currentChar = str(toPrint[charindex])
		logmessage("col is "+str(col)+" bit is "+str(bit))
		logmessage("charindex "+str(charindex)+" gives CHARACTER "+currentChar+": "+str(fontConfig['font']['letters'][currentChar][col]))
		if(fontConfig['font']['letters'][currentChar][col][bit] ==str(1)):
			logmessage("\nabout to commit")

		n=5
		while n>0:
			modifyfile()
			commitandpush()
		else:
			logmessage("\nnot committing this time ")

		# prevent any more commit attempts today
		lastCommitDay = today

def commitandpush():
	subprocess.call(['git', 'commit', '--allow-empty', '-m', '""', 'README.md'])
	subprocess.call(['git', 'push'])
	logmessage("\npush to repo done")
	n=n-1

def logmessage(message):
	f = open('/tmp/pad-log.txt', 'a')
	f.write("\n"+message)
	f.close()
	
def modifyfile():
	os.chdir(tableauDir)
	fo=open(tableau,"a")
	fo.write("-")
	fo.close()
	
# start off setting lastCommitDay as yesterday to force first attempt
lastCommitDay = int(time.time()/86400) -1
global dow

# day of week as int. Sunday is 0.
dow = int(time.strftime("%w")) # int value
global sd

sd = int(startDay) - int(dow)
if( int(dow) in workingDays ):
	commit()
	logmessage("\nfirst commit is done - about to enter while loop")
else:
	logmessage("day of week "+str(dow)+" not in workingdays")

# then drop into a loop, always checking lastCommitDay, which gets updated in the commit function
while True:
	logmessage("\nlast commit day is "+str(lastCommitDay)+" day of week is "+str(dow))
	if( int(dow) in workingDays ):
		f.write("\nabout to enter commit function. ")
		commit()
	else:
		logmessage("\nday of week is not in workingdays, so sleeping")
	f.close()
	time.sleep(3600) 
