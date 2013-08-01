#!/usr/bin/python

# A Pixel A Day

import json
import time
import math

toPrint = "GRAFITTI"

fontConfig = json.loads(open('font.json').read())
fontWidth = int(fontConfig['font']['fontWidth'])+1

#startDay = get today's date
startDay = int(time.time())/86400 # as days since epoch
daysOfWorkingWeek=[2,3,4,5,6]

# maintain record of last day a commit was made
# update this whenever a commit is made 
# check this to prevent >1 commits per day

lastCommitDay = (int(time.time())/86400)-1


commit();

while True:
	commit()
	time.sleep(3600)   # 1 hour

def commit:
	dayOfWeek = time.strftime("%w") # int value
	today = int(time.time())/86400

	# check lastCommitDay
	if( today == lastCommitDay ){
		continue
	}elif( dayOfWeek == 1 || dayOfWeek == 7){
		# don't commit on monday or sunday 
		# todo - make this fontConfig (fontHeight) aware
		continue;
	}else{
		# determine whether commit should happen today
		daysSinceStart = today - startDay
		currentChar = daysSinceStart / fontWidth	
		currentChar = math.ceil(currentChar) # daysSinceStart: 1->1, 2->1, 3->1, 4->1, 5->1, 6->2
						     # daysSinceStart: 32->7 33->7 34->7 35->8 36->8 37->8
		currentChar = toPrint[currentChar]   # say, 'R' in GRAFFITI
		columnInDay = daysSinceStart - ((currentChar-1)*5)
		if( fontConfig['font']['letters'][currentChar][columnInDay] == 1){
			subprocess.call()
		}

		# prevent any more commit attempts today
		lastCommitDay = today;
	}


#canStart = true

#for day in firstChar[cols][1]   #firstChar->cols['1'] as day
#	if day == 0
#		keep going
#	
#		if day < dayOfWeek
#			keep going
#		
#print "today's date is ",startDay
