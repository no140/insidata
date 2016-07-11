#!/usr/bin/env python3


import json				#parses lines into dict
import datetime 			#handles times
from collections import defaultdict	#for default dict's, not used anymore
import numpy as np			#calculates medians
import time				#for testing
import sys


#output file
f = open('../venmo_output/output_test.txt', 'w') #./venmo_output/output.txt

"""each line is a dict with timestamp, target, and actor
- each new line timestamp must be checked that falls within 60sec of max timestamp, and if >max, made as new max timestamp
- if new max, check if other timestamps are out of 60sec range and remove
- each new target/actor pair establishes a connection (if not new, update timestamp only)
- median gets updated and output
- graph updates"""

mainlist = []		#holds target, actor, datetime
dd = defaultdict(list)	#needed to get degrees from each node
degrees = []
duplicate = False
verbose = True
index = 1

print('starting...')
start_time=time.time()
with open("../venmo_input/venmo-trans.txt", 'r') as ven:
	
	try:
		firstline = json.loads(ven.readline())	
		max_time = datetime.datetime.strptime(firstline["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		mainlist.append((firstline["target"], firstline["actor"], max_time))
	except (KeyError, ValueError):
		print('problem in first line')
		sys.exit(1)
	f.write('1.00\n')
	dd[mainlist[0][1]].append(mainlist[0][0])
	dd[mainlist[0][0]].append(mainlist[0][1])
	
	for line in ven:
		verbose = False
		index+=1
		if index == 519 or index == 520:
			verbose = True
		
		if verbose == True: print (line)
		try:		
			d = json.loads(line)
		except ValueError:
			print('skipping a line')
			continue	

		#check timestamp
		try:
			new_time = datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		except KeyError:
			print('no date field')
			continue
		
		#check if duplicate
		duplicate = False
		for u,v,datatime in list(mainlist):
			if u == d["target"] and v == d["actor"]:
				if verbose == True: print('duplicate!')				
				#remove old
				mainlist.remove((u,v,datatime))
				duplicate = True

		timedelta =  new_time - max_time
		if timedelta.total_seconds() > 0:
			if verbose == True: print("new max")
			max_time = new_time
			#check to remove old entries
			#t0=time.time()
			for u,v,datatime in list(mainlist):
				timediff = datatime - max_time
				if timediff.total_seconds() < -60:
					dd[u].remove(v)		#because dd values are in a list
					dd[v].remove(u)
					#must also remove from mainlist
					mainlist.remove((u,v,datatime))
					#print('removed an edge!!!!!!')
					if len(dd.get(u)) == 0:
						dd.pop(u)
					if len(dd.get(v)) == 0:
						dd.pop(v)
					#continue
				#else: print('still in time window')
			#t1=time.time()
			#print('remove old entries time: ',t1-t0)			
			#add to graph
			try:
				mainlist.append((d["target"], d["actor"], datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")))	#add just latest pair
			except KeyError:
				print('no target or actor field')
				continue
			
			
			if duplicate == False:	#add to dd
				dd[mainlist[len(mainlist)-1][1]].append(mainlist[len(mainlist)-1][0])
				dd[mainlist[len(mainlist)-1][0]].append(mainlist[len(mainlist)-1][1])

			#calculate MEDIAN based on G.neighbors
			degrees=[len(dd[item]) for item in dd.keys()]
			f.write(str("%.2f" % np.median(degrees))+'\n')

		elif timedelta.total_seconds() < -60: 
			if verbose == True: print("out of order, ignore!!!")
			#update median
			f.write(str("%.2f" % np.median(degrees))+'\n')
		else: 
			if verbose == True: print("behind in time, but ok")
			#add to graph
			try:
				mainlist.append((d["target"], d["actor"], datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")))	#add just latest pair
			except KeyError:
				print('no target or actor field')
				continue

			if duplicate == False:	#add to dd
				dd[mainlist[len(mainlist)-1][1]].append(mainlist[len(mainlist)-1][0])
				dd[mainlist[len(mainlist)-1][0]].append(mainlist[len(mainlist)-1][1])			
			
			#t0=time.time()
			#calculate MEDIAN based on G.neighbors
			degrees=[len(dd[item]) for item in dd.keys()]
			f.write(str("%.2f" % np.median(degrees))+'\n')
			#t1=time.time()
			#print('median degree calc time: ',t1-t0)
		if verbose == True: print(degrees); print(len(degrees)); print(np.median(degrees))


f.close()		

print('total app time: ',time.time()-start_time)

#=============================functions
'''
def get_median():
	degrees=[len(G.neighbors(node)) for node in G.nodes()]
	#print(degrees) 
	#print("%.2f" % np.median(degrees))
	f.write(str("%.2f" % np.median(degrees))+'\n')
'''
#==============================OLD CODE========================================

#---- using dd :
	#pairs.append((firstline["target"], firstline["actor"]))
	#dd[pairs[0][1]].append(pairs[0][0])
	#dd[pairs[0][0]].append(pairs[0][1])

#---- in for loop:
		#print (d["target"],d["actor"])
		#pairs.append((d["target"], d["actor"]))
		#print(pairs)		
		#print(len(pairs))
		#create dictionary with multiple values
#		for target, actor in pairs:
#			dd[target].append(actor)	#since undirected, connected nodes
#			dd[actor].append(target)
		
		#dd[pairs[len(pairs)-1][1]].append(pairs[len(pairs)-1][0])	#latest addition
		#dd[pairs[len(pairs)-1][0]].append(pairs[len(pairs)-1][1])	#latest addition
#		print(dd)		
#		print('# of nodes: ',len(dd))			#indicates # nodes
#		print(dd.items())
		#print('last node added: ',dd[d["actor"]])	#last vertex added, doesnt work: pairs(len(pairs)-1)[0]

		#calculate MEDIAN, using 'dd'
#		for node in dd:
#			degrees=[len(dd[item]) for item in dd.keys()]
#		print(degrees)
		#np.set_printoptions(precision=2)
#		print("%.2f" % np.median(degrees))
#		f.write(str("%.2f" % np.median(degrees))+'\n')
