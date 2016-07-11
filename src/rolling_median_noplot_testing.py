#!/usr/bin/env python3


import json				#parses lines into dict
import datetime 			#handles times
from collections import defaultdict	#for default dict's, not used anymore
import numpy as np			#calculates medians
import time				#for testing
import sys


#output file
f = open('../venmo_output/output_testing.txt', 'w') #./venmo_output/output.txt

"""
- each line is a dict with timestamp, target, and actor (no pandas to hold all data; list/dict is only as big as amount of data within 60 seconds)
- each new line timestamp must be checked that falls within 60sec of max timestamp, and if >max, made as new max timestamp
- if new max, check if other timestamps are out of 60sec range and remove
- each new target/actor pair establishes a connection (if not new, update timestamp only)
- median gets updated and output
- graph updates
"""

mainlist = []		#holds target, actor, datetime
dd = defaultdict(list)	#needed to get degrees from each node
degrees = []
duplicate = False

#--------functions
#def add_to_dd(actor, target):
#	dd[actor].append(target)
#	dd[target].append(actor)

def check_duplicate(target, actor):
	for u,v,datatime in list(mainlist):
		if u == target and v == actor:
			#remove old
			mainlist.remove((u,v,datatime))
			#remove_fr_main((u,v,datatime))		#attempt to optimize
			duplicate = True
			#print('duplicated')
			return duplicate
	duplicate = False
	return duplicate

def check_times(max_time):
	for u,v,datatime in list(mainlist):
		timediff = datatime - max_time
		if timediff.total_seconds() < -60:
			dd[u].remove(v)		#because dd values are in a list
			dd[v].remove(u)
			#must also remove from mainlist
			#mainlist.remove((u,v,datatime))
			remove_fr_main((u,v,datatime))
			#print('removed an edge!!!!!!')
			if len(dd.get(u)) == 0:
				dd.pop(u)
				#print('removed node')
			if len(dd.get(v)) == 0:
				dd.pop(v)
				#print('removed node')
#-----------------

#print('starting...')
start_time=time.time()
with open("../venmo_input/venmo-trans.txt", 'r') as ven:

	append_to_main = mainlist.append		#attempt to optimize
	remove_fr_main = mainlist.remove		#attempt to optimize
	try:
		firstline = json.loads(ven.readline())	
		max_time = datetime.datetime.strptime(firstline["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		#mainlist.append((firstline["target"], firstline["actor"], max_time))
		append_to_main((firstline["target"], firstline["actor"], max_time)) #optimize
	except (KeyError, ValueError):
		print('problem in first line')
		sys.exit(1)
	f.write('1.00\n')
	dd[mainlist[0][1]].append(mainlist[0][0])
	dd[mainlist[0][0]].append(mainlist[0][1])
	
	for line in ven:
		#print (line)	

		#check line, timestamp, fields
		try:
			d = json.loads(line)			
			new_time = datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")
			target = d["target"]
			actor = d["actor"]
		except (KeyError, ValueError):
			print('missing field, skipping line')
			continue
			
		#check if DUPLICATE?
		duplicate = False
		duplicate = check_duplicate(d["target"], d["actor"])
		'''for u,v,datatime in list(mainlist):
			if u == d["target"] and v == d["actor"]:
				#remove old
				#mainlist.remove((u,v,datatime))
				remove_fr_main((u,v,datatime))		#attempt to optimize
				duplicate = True'''

		timedelta =  new_time - max_time
		#check TIME in WINDOW?
		if timedelta.total_seconds() > 0:
			#print("new max")
			max_time = new_time
			#check to REMOVE OLD entries
			#t0=time.time()
			check_times(max_time)
			'''for u,v,datatime in list(mainlist):
				timediff = datatime - max_time
				if timediff.total_seconds() < -60:
					dd[u].remove(v)		#because dd values are in a list
					dd[v].remove(u)
					#must also remove from mainlist
					#mainlist.remove((u,v,datatime))
					remove_fr_main((u,v,datatime))
					#print('removed an edge!!!!!!')
					if len(dd.get(u)) == 0:
						dd.pop(u)
						#print('removed node')
					if len(dd.get(v)) == 0:
						dd.pop(v)
						#print('removed node')
					#continue
				#else: print('still in time window')'''
			#t1=time.time()
			#print('remove old entries time: ',t1-t0)			
			
			#add to graph
			append_to_main((d["target"], d["actor"], datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")))	#optimize vs mainlist.append
			
			
			if duplicate == False:	#add latest to dd
				#add_to_dd(d["actor"],d["target"])
				dd[d["actor"]].append(d["target"])
				dd[d["target"]].append(d["actor"])
				degrees=[len(dd[item]) for item in dd.keys()]
				f.write(str("%.2f" % np.median(degrees))+'\n')
			else:	#just write last median
				#print('just writing last median')
				f.write(str("%.2f" % np.median(degrees))+'\n')

		elif timedelta.total_seconds() < -60: 
			#print("out of order, ignore!!!")
			#update median only
			degrees=[len(dd[item]) for item in dd.keys()]	#need to recalc if degrees empty
			f.write(str("%.2f" % np.median(degrees))+'\n')
		else: 
			#print("behind in time, but ok")
			#add to graph
			append_to_main((d["target"], d["actor"], datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")))	#optimize vs mainlist.append


			if duplicate == False:	#add latest to dd, and write median
				#add_to_dd(d["actor"],d["target"])
				dd[d["actor"]].append(d["target"])
				dd[d["target"]].append(d["actor"])
				#t0=time.time()
				#calculate MEDIAN based on dd
				degrees=[len(dd[item]) for item in dd.keys()]
				f.write(str("%.2f" % np.median(degrees))+'\n')
				#print('median degree write time: ',time.time()-t0)
			else:	#just write last median
				#print('just writing last median')
				f.write(str("%.2f" % np.median(degrees))+'\n')
		#print(degrees)	


f.close()		

print('total app time: ',time.time()-start_time)
