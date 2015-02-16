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
#tableauDir = "/Users/clacy/Development/web/a-pixel-a-day/"
tableauDir = "/export/a-pixel-a-day/"
tableau = tableauDir + tableauFile
toPrint = "ZYAHOO!" # use & for testing. 

workingDays = [1,2,3,4,5]

fontConfig = json.loads(open(tableauDir+'font.json').read())
fontWidth = int(fontConfig['font']['fontWidth'])+1

# determine no. of lines in file
def file_len(fname):
	i=-1
        with open(fname) as f:
              for i, l in enumerate(f):
                    pass
        return i + 1

	f.close()

def commit():
	today = int(time.time()/86400) + 0 

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
	logmessage("col is "+col+" bit is "+str(bit))
	logmessage("charindex "+str(charindex)+" gives CHARACTER "+currentChar+": "+str(fontConfig['font']['letters'][currentChar][col]))
	if(fontConfig['font']['letters'][currentChar][col][bit] ==str(1)):
		logmessage("\nabout to commit")

		n=5
		while n>0:
			modifyfile()
			commitandpush()
			n=n-1
	else:
		logmessage("\nnot committing this time ")


def commitandpush():
	subprocess.call(['git', 'commit', '--allow-empty', '-m', '""', 'README.md'])
	subprocess.call(['git', 'push'])
	logmessage("\npush to repo done")

def logmessage(message):
	f = open('/tmp/pad-log.txt', 'a')
	f.write("\n"+message)
	f.close()
	
def modifyfile():
	os.chdir(tableauDir)
	fo=open(tableau,"a")
	fo.write("-")
	fo.close()


#if > 0 lines in tableau, this is not the first day. Read start time from file
flen = file_len(tableau)
if flen > 0:
        f = open(tableau)
        startTime = int(f.readline())

else:
	startTime = int(time.time())  # write start time to file - it's now
	f = open(tableau)
        with open(tableau, 'a') as tab:
              tab.write(str(startTime)+"\n\n")

startDay = startTime/86400 # days since epoch where 86400 is no. seconds in a day
dow = int(time.strftime("%w")) # day of week as int. Sunday is 0

global sd
sd = int(startDay) - int(dow)

if( int(dow) in workingDays ):
	commit()
else:
	logmessage("day of week "+str(dow)+" not in workingdays")
