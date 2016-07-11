#!/usr/bin/env python3

import networkx as nx			#edge graphs
import matplotlib.pyplot as plt		#drawing graphs
import json				#parses lines into dict
import datetime 			#handles times
#from collections import defaultdict	#for default dict's, not used anymore
import numpy as np			#calculates medians
import time				#for testing
import sys

#ven = open(./venmo_input/venmo_trans.txt, 'r')
#ven.readline()

#output file
f = open('./venmo_output/output.txt', 'w') #./venmo_output/output.txt

"""each line is a dict with timestamp, target, and actor
- each new line timestamp must be checked that falls within 60sec of max timestamp, and if >max, made as new max timestamp
- if new max, check if other timestamps are out of 60sec range and remove
- each new target/actor pair establishes a connection (if not new, update timestamp only)
- median gets updated and output
- graph updates"""

pairs = []
#dd = defaultdict(list)
degrees = []
new_max=False
faster_plot = False	#only speeds up by a few percent and not as pretty.

options = {
 'with_labels': False,
 'node_color': 'black',
 'node_size': 100,
 'linewidths': 0,
 'line_color': 'grey',
 'width': 0.5,
}
colors=['grey', 'black', 'brown', 'blue', 'green', 'yellow', 'orange', 'red', 'pink', 'purple']
G=nx.Graph()
#G=nx.lobster_graph()
#G=nx.draw_circular(G, **options)

print('starting...')
start_time=time.time()
with open("./venmo_input/venmo-trans.txt", 'r') as ven:
	
	try:
		firstline = json.loads(ven.readline())	
		max_time = datetime.datetime.strptime(firstline["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		G.add_edge(firstline["target"], firstline["actor"], time=max_time)
	except (KeyError, ValueError):
		print('problem in first line')
		#print >> sys.stderr, "Exception: %s" % str(e)
		sys.exit(1)
	f.write('1.00\n')
	plt.ion()	
	#plt.figure(figsize=(8,8))
	#nx.draw(G, node_size=float(G.degree(v) for v in G))
	plt.title("transactions")
	#nx.draw_spring(G, **options)
	nx.draw(G, width=2.5, node_size=15.0)	
	plt.show()	#initial plot
	
	for line in ven:
		#print (line)
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
		timedelta =  new_time - max_time
		#print (timedelta.total_seconds())
		if timedelta.total_seconds() > 0:
			#print("new max")
			#new_max=True
			max_time = new_time
			#check to remove old entries
			t0=time.time()
			for u,v,datatime in list(G.edges_iter(data='time')):
				timediff = datatime - max_time
				if timediff.total_seconds() < -60:
					G.remove_edge(u,v)
					#print('removed an edge!!!!!!')
					if len(G.neighbors(u)) == 0:
						G.remove_node(u)
					if len(G.neighbors(v)) == 0:
						G.remove_node(v)
					#continue
					#plt.gcf().clear()
				#else: print('still in time window')
			#t1=time.time()
			#print('remove old entries time: ',t1-t0)			
			#add to graph
			try:
				G.add_edge(d["target"], d["actor"], time=datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ"))	#add just latest pair
			except KeyError:
				print('no target or actor field')
				continue
			#check if duplicate --networkx doc says doesn't duplicate
			#for u,v,datatime in list(G.edges_iter()):
			#	if u == 

			#calculate MEDIAN based on G.neighbors
			degrees=[len(G.neighbors(node)) for node in G.nodes()]
			f.write(str("%.2f" % np.median(degrees))+'\n')

		elif timedelta.total_seconds() < -60: 
			#print("out of order, ignore!!!")
			#update median
			f.write(str("%.2f" % np.median(degrees))+'\n')
		else: 
			#print("behind in time, but ok")
			#add to graph
			try:
				G.add_edge(d["target"], d["actor"], time=datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ"))	#add just latest pair
			except KeyError:
				print('no target or actor field')
				continue
			#t0=time.time()
			#calculate MEDIAN based on G.neighbors
			degrees=[len(G.neighbors(node)) for node in G.nodes()]
			f.write(str("%.2f" % np.median(degrees))+'\n')
			#t1=time.time()
			#print('median degree calc time: ',t1-t0)
			
		#graph EDGES
		#networkx
		#G.add_edge(d["target"], d["actor"])
		#G.add_edges_from(pairs)		#add all pairs
		#G.add_edge(d["target"], d["actor"], time=datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ"))	#add just latest pair
		#print(G.number_of_nodes())
		#print(G.number_of_edges())
		#print('#of connections to latest node: ', len(G.neighbors(d["actor"])))
		#print(all_pairs_node_connectivity(G))
		
		#graph_time=time.time()
#		if new_max == True:
		if faster_plot == False:
			plt.gcf().clear()
			pos = nx.shell_layout(G)
			#edges = G.edges()
			#colors = [G[u][v]['color'] for u,v in edges]
			#weights = [G[u][v]['weight'] for u,v in edges]
			#nx.draw(G, pos, edges=edges, edge_color=colors, width=weights)
			#node_colors = ["blue" if n in shortestPath else "red" for n in G.nodes()]
			node_sizes = [15*len(G.neighbors(n)) for n in G.nodes()]
			#node_colors = [colors[n] for n in node_sizes]
			nx.draw_networkx_nodes(G, pos=pos, node_size=node_sizes)#, node_color=node_colors)
			#edge widths and colors should be based on timestamp > newer is bigger
			#scale to number of total transactions
			num_nodes = len(G.nodes())
			scale = 20*(pow(1.0025,num_nodes)+0.01*num_nodes)#gives good range to 300 nodes...
			edge_widths = [(60-((max_time-G[u][v]['time']).total_seconds()))/scale for u,v, in G.edges()]

			#justgraph_time=time.time()
			nx.draw_networkx_edges(G, pos=pos, width=edge_widths)
			#nx.draw_shell(G, **options)
			plt.show()
			#print('just graph time: ',time.time()-justgraph_time)
#			new_max=False
		else:	#don't recalculate everything?
			plt.gcf().clear()
			#nx.draw(G, nx.shell_layout(G), node_size=15.0)
			nx.draw_networkx_nodes(G, nx.shell_layout(G), node_size=15.0)
			nx.draw_networkx_edges(G, nx.shell_layout(G))
			plt.show()

		#print('update graph time: ',time.time()-graph_time)
""" testing graphical output
		if len(G.nodes()) >= 25:
			if len(G.nodes()) == 25:
				plt.savefig("netwk_test_"+str(len(G.nodes()))+".png")
				#plt.gcf().clear()
		if len(G.nodes()) >= 50:
			if len(G.nodes()) == 50:
				plt.savefig("netwk_test_"+str(len(G.nodes()))+".png")
				#plt.gcf().clear()
			elif len(G.nodes()) >= 100:
				if len(G.nodes()) == 100:
					plt.savefig("netwk_test_"+str(len(G.nodes()))+".png")
					#plt.gcf().clear()
				elif len(G.nodes()) >= 200:
					if len(G.nodes()) == 200:
						plt.savefig("netwk_test_"+str(len(G.nodes()))+".png")
						#plt.gcf().clear()
					elif len(G.nodes()) >= 300:	#325 already too high
						if len(G.nodes()) == 300:
							plt.savefig("netwk_test_"+str(len(G.nodes()))+".png")
							#plt.gcf().clear() """


plt.savefig("netwk_test.png")

f.close()		

print('total app time: ',time.time()-start_time)

#=============================functions
def get_median():
	degrees=[len(G.neighbors(node)) for node in G.nodes()]
	#print(degrees) 
	#print("%.2f" % np.median(degrees))
	f.write(str("%.2f" % np.median(degrees))+'\n')

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
