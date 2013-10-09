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

tableauFile = "README.md"
tableauDir = "/export/tableau/" #/Users/clacy/Development/web/tableau/"
tableau = tableauDir + tableauFile
toPrint = "&BOO"; # use & for testing. It is all '1's

fontConfig = json.loads(open('font.json').read())
fontWidth = int(fontConfig['font']['fontWidth'])+1

#startDay = get today's date
startDay = (int(time.time())/86400) # days since epoch 
daysOfWorkingWeek=[2,3,4,5,6]

# maintain record of last day a commit was made
# update this whenever a commit is made 
# check this to prevent >1 commits per day

def commit(lastCommitDay):
	dayOfWeek = time.strftime("%w") # int value
	today = int(time.time())/86400

	# check lastCommitDay
	if today != lastCommitDay and dayOfWeek != 1 and dayOfWeek != 7:
		print("today is "+str(today)+" lastCommitDay is "+str(lastCommitDay))
		# determine whether commit should happen today
		daysSinceStart = today - startDay
		currentChar = float(daysSinceStart) / float(fontWidth)
		currentCharIndex = int(math.ceil(currentChar)) 
		currentChar = str(toPrint[currentCharIndex])   # say, 'R' in GRAFFITI
		columnInDay = str(daysSinceStart - ((currentCharIndex-1)*5)-1) # -1 because the column names are not zero-based
		bit = int(dayOfWeek)-1
		# only commit if the bit in this position is a 1
		print(" bool is "+fontConfig['font']['letters'][currentChar][columnInDay][bit]+" for col "+columnInDay)
		if( fontConfig['font']['letters'][currentChar][columnInDay][bit] == str(1)):
			fo=open(tableau,"a")
			fo.write("-")
			fo.close();
			os.chdir(tableauDir)
			subprocess.call(['git', 'commit', '--allow-empty', '-m', '""', 'README.md'])
			subprocess.call(['git', 'push'])

		# prevent any more commit attempts today
		lastCommitDay = today;

lastCommitDay = (int(time.time())/86400)-1
commit(lastCommitDay)

while True:
	commit(lastCommitDay)
	time.sleep(3600) 
