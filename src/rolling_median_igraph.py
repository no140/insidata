#!/usr/bin/env python3


#import networkx as nx
import matplotlib.pyplot as plt
import igraph
#import graph_tool.all as gt
import json
import datetime 
from collections import defaultdict
import numpy as np

#ven = open(./venmo_input/venmo_trans.txt, 'r')
#ven.readline()

f = open('../venmo_output/output.txt', 'w')

#each line is a dict with timestamp, target, and actor
#each new line timestamp must be checked that falls within 60sec of max timestamp, and if >max, made as new max timestamp
#if new max, check if min timestamp is out of 60sec range on new max timestamp
#each new target/actor pair establishes a connection (if not new, update timestamp only)
#median gets updated and output
#graph updates

times = []
pairs = []
dd = defaultdict(list)

G=nx.Graph()
#g=gt.Graph(directed=False)

#np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
#float_formatter = lambda x: "%.2f" % x
#np.set_printoptions(formatter={'float_kind':float_formatter})

with open("../data-gen/venmo-trans.txt", 'r') as ven:
	firstline = json.loads(ven.readline())	
	#max_time = datetime.datetime.strptime(json.loads(ven.readline())["created_time"], "%Y-%m-%dT%H:%M:%SZ")
	max_time = datetime.datetime.strptime(firstline["created_time"], "%Y-%m-%dT%H:%M:%SZ")
	#print (type(max_time))
	#pairs.append((firstline["target"], firstline["actor"]))
	f.write('1.00\n')
	#dd[pairs[0][1]].append(pairs[0][0])
	#dd[pairs[0][0]].append(pairs[0][1])
	G.add_edge(firstline["target"], firstline["actor"], time=max_time)
	#G.edge[firstline["target"],firstline["actor"]]['weight'] = 4
	nx.draw(G)
	plt.show()	#initial plot
	for line in ven:
		#print(type(line))
		print (line)
		d = json.loads(line)
		#print(type(d))

		#check timestamp
		#print (d["created_time"])
		new_time = datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		timedelta =  new_time - max_time
		print (timedelta.total_seconds())
		if timedelta.total_seconds() > 0:
			print("new max")
			max_time = new_time
			#check to remove old entries
			for u,v,datatime in list(G.edges_iter(data='time')):
				#print(type(datatime))
				timediff = datatime - max_time
				if timediff.total_seconds() < -60:
					G.remove_edge(u,v)
					print('removed an edge!!!!!!')
					if len(G.neighbors(u)) == 0:
						G.remove_node(u)
					if len(G.neighbors(v)) == 0:
						G.remove_node(v)
					#continue
				else: print('still in time window')

		elif timedelta.total_seconds() < -60: 
			print("out of order, ignore!!!")
		else: print("behind in time, but ok")
		#times.append(d["created_time"])
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
		#i = iter(pairs)		for lists
		#connects = dict(zip(i, i))	for lists	
		#connects = dict(pairs)		#for tuples
		#print(connects)
		#print(len(connects))		#indicates how many nodes

		#graph EDGES

		#networkx
		#G.add_edge(d["target"], d["actor"])
		#G.add_edges_from(pairs)		#add all pairs
		G.add_edge(d["target"], d["actor"], time=datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ"))	#add just latest pair
		print(G.number_of_nodes())
		print(G.number_of_edges())
		print('#of connections to latest node: ', len(G.neighbors(d["actor"])))
		#print(all_pairs_node_connectivity(G))
		nx.draw(G)
		#plt.show()
		plt.savefig("netwk_test.png")

		#print(pairs[len(pairs)-1][0])

		#graph-tool
		#str(pairs[len(pairs)-1][0]) = g.add_vertex()
		#str(pairs[len(pairs)-1][1]) = g.add_vertex()
#		for node in connects:
#			e=g.add_edge(node, pairs[len(pairs)-1][1], add_missing=True)
#		graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="test.png")
#		print(d["target"].out_degree())

		#calculate MEDIAN, using 'dd'
#		for node in dd:
#			degrees=[len(dd[item]) for item in dd.keys()]
#		print(degrees)
		#np.set_printoptions(precision=2)
#		print("%.2f" % np.median(degrees))
#		f.write(str("%.2f" % np.median(degrees))+'\n')

		#calculate MEDIAN based on G.neighbors
		#for node in G.nodes():
		degrees=[len(G.neighbors(node)) for node in G.nodes()]
		print(degrees) 
		print("%.2f" % np.median(degrees))
		f.write(str("%.2f" % np.median(degrees))+'\n')

		




f.close()		
