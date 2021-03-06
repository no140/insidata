#!/usr/bin/env python3


import networkx as nx
import matplotlib.pyplot as plt
#import igraph
import graph_tool.all as gt
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
main_list = []
index_list = []
degrees=[]
dd = defaultdict(list)

#G=nx.Graph()
g=gt.Graph(directed=False)

#np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
#float_formatter = lambda x: "%.2f" % x
#np.set_printoptions(formatter={'float_kind':float_formatter})

with open("../data-gen/venmo-trans.txt", 'r') as ven:
	firstline = json.loads(ven.readline())	
	#max_time = datetime.datetime.strptime(json.loads(ven.readline())["created_time"], "%Y-%m-%dT%H:%M:%SZ")
	max_time = datetime.datetime.strptime(firstline["created_time"], "%Y-%m-%dT%H:%M:%SZ")
	#print (type(max_time))
	#pairs.append((firstline["target"], firstline["actor"]))
	main_list.append((firstline["actor"],firstline["target"],max_time))
	index_list.append((2*len(main_list)-1, 2*len(main_list)))
	f.write('1.00\n')
	#dd[pairs[0][1]].append(pairs[0][0])
	#dd[pairs[0][0]].append(pairs[0][1])
	#print(len(dd))
	g.add_edge(index_list[0][0], index_list[0][1], add_missing=True)

#	G.add_edge(firstline["target"], firstline["actor"], time=max_time)
#	nx.draw(G)
#	plt.show()	#initial plot

#--------------------------------------------------------------------------------------
	for line in ven:
		#print(type(line))
		print (line)
		d = json.loads(line)
		#print(type(d))
		for v in g.vertices():
		    print(v)
		for e in g.edges():
		    print(e)
#--------------------------------------------------------------------------------------
		#check timestamp
		#print (d["created_time"])
		new_time = datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ")
		timedelta =  new_time - max_time
#		print (timedelta.total_seconds())
		if timedelta.total_seconds() > 0:
			print("new max")
			max_time = new_time

			#check to remove old entries
			counter=0
			for u,v,datatime in list(main_list):
				#print(type(datatime))
				timediff = datatime - max_time
				if timediff.total_seconds() < -60:
					g.remove_edge(g.edge(index_list[counter][0],index_list[counter][1]))
					print('removed an edge!!!!!!')
					if g.vertex(index_list[counter][0]).out_degree() == 0:
						g.remove_vertex(index_list[counter][0])
					if g.vertex(index_list[counter][1]).out_degree() == 0:
						g.remove_vertex(index_list[counter][1])
					#index_list[counter][0] = 0
					#index_list[counter][1] = 0
					#continue
				else: 
					print('still in time window')
					counter+=1
			#add new info to list
			main_list.append((d["actor"],d["target"],new_time))
			index_list.append((2*len(main_list)-1, 2*len(main_list)))
			#add new info to graph
			g.add_edge(index_list[len(index_list)-1][0], index_list[len(index_list)-1][1], add_missing=True)
			gt.graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="test.png")
			#calculate MEDIAN based on graph-tools
			degrees=[node.out_degree() for node in g.vertices()]
			print(degrees) 
			print("%.2f" % np.median(degrees))
			f.write(str("%.2f" % np.median(degrees))+'\n')
		
		elif timedelta.total_seconds() < -60: 
			print("out of order, ignore!!!")
			#still must update median - same as before
			f.write(str("%.2f" % np.median(degrees))+'\n')
		else: 
			print("behind in time, but ok")
			#add new info to graph

			#update median
			

#-----------------------------------------------------------------------------------------
		#times.append(d["created_time"])
		#print (d["target"],d["actor"])
		pairs.append((d["target"], d["actor"]))
		#print(pairs)		
		#print(len(pairs))
		#create dictionary with multiple values
		#for target, actor in pairs:
		#	dd[target].append(actor)	#since undirected, connected nodes
		#	dd[actor].append(target)
		
		#dd[pairs[len(pairs)-1][1]].append(pairs[len(pairs)-1][0])	#latest addition
		#dd[pairs[len(pairs)-1][0]].append(pairs[len(pairs)-1][1])	#latest addition
		#print(dd)		
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
#		G.add_edge(d["target"], d["actor"], time=datetime.datetime.strptime(d["created_time"], "%Y-%m-%dT%H:%M:%SZ"))	#add just latest pair
#		print(G.number_of_nodes())
#		print(G.number_of_edges())
#		print('#of connections to latest node: ', len(G.neighbors(d["actor"])))
		#print(all_pairs_node_connectivity(G))
#		nx.draw(G)
		#plt.show()
#		plt.savefig("netwk_test.png")

		#print(pairs[len(pairs)-1][0])

#-------------------------------------------------------------------------------
		#graph-tool
		#str(pairs[len(pairs)-1][0]) = g.add_vertex()
		#str(pairs[len(pairs)-1][1]) = g.add_vertex()
		
		#for node, item in dd.items():
#		for actor, target in main_list:
#			g.add_edge(dd.keys().index(node), dd.keys().index(item), add_missing=True)
#		graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(200, 200), output="test.png")
#		print(d["target"].out_degree())

#-------------------------------------------------------------------------------
		#calculate MEDIAN, using 'dd'
#		for node in dd:
#			degrees=[len(dd[item]) for item in dd.keys()]
#		print(degrees)
		#np.set_printoptions(precision=2)
#		print("%.2f" % np.median(degrees))
#		f.write(str("%.2f" % np.median(degrees))+'\n')

		#calculate MEDIAN based on G.neighbors
		#for node in G.nodes():
#		degrees=[len(G.neighbors(node)) for node in G.nodes()]
#		print(degrees) 
#		print("%.2f" % np.median(degrees))
#		f.write(str("%.2f" % np.median(degrees))+'\n')


		




f.close()		
