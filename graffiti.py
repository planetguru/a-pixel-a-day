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
#tableauDir = "/Users/clacy/Development/web/a-pixel-a-day/"
tableau = tableauDir + tableauFile
toPrint = "&YAHOO"; # use & for testing. It is all '1's

fontConfig = json.loads(open('font.json').read())
fontWidth = int(fontConfig['font']['fontWidth'])+1

#startDay = get today's date
startDay = int(time.time())/86400 # days since epoch 
today = startDay

workingDays = [1,2,3,4,5]

# maintain record of last day a commit was made
# update this whenever a commit is made 
# check this to prevent >1 commits per day

def commit():
	# update today to move forward from lastCommitDay on the turn of midnight
	today = int(time.time()/86400) + 0 

	# check lastCommitDay
	global lastCommitDay
	if today != lastCommitDay:
		print("today is "+str(today)+" lastCommitDay is "+str(lastCommitDay))
		# determine whether commit should happen today
		daysSinceStart = today - startDay
		print("days since start is "+str(daysSinceStart))
		currentCharIndex = 0  # identifies which char in the string we are at
		if( daysSinceStart > 0):   
			currentCharIndex = int(math.ceil(float(daysSinceStart)/fontWidth)) - 1
		currentChar = str(toPrint[currentCharIndex])   # eg 'E' in HELLO
		# eg on day 17, columnInChar is  17%5 + 1 (1 is sunday offset)
		columnInChar = str((daysSinceStart % 5)+1)
		global dayOfWeek
		bit = int(dayOfWeek)-1
		print ("currentCharIndex is "+str(currentCharIndex)+" so currentChar is "+currentChar+" column in day is "+columnInChar+" bit is "+str(bit))
		# only commit if the bit in this position is a 1
		pprint.pprint(fontConfig['font']['letters'][currentChar][columnInChar][bit])
		if( fontConfig['font']['letters'][currentChar][columnInChar][bit] == str(1)):
			fo=open(tableau,"a")
			fo.write("-")
			fo.close();
			os.chdir(tableauDir)
			subprocess.call(['git', 'commit', '--allow-empty', '-m', '""', 'README.md'])
			subprocess.call(['git', 'push'])

		# prevent any more commit attempts today
		lastCommitDay = today;

# start off setting lastCommitDay as yesterday to force first attempt
lastCommitDay = int(time.time()/86400) -1
global dayOfWeek
# day of week as int. Sunday is 0.
dayOfWeek = time.strftime("%w") # int value
commit()

# then drop into a loop, always checking lastCommitDay, which gets updated in the commit function
while True:
	dayOfWeek = time.strftime("%w") # int value
	if( dayOfWeek in workingDays ):
		commit()
	time.sleep(3600) 
