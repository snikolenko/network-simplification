import networkx as nx
import random
import sys
import numpy as np
from datetime import datetime,time,date,timedelta

DEST_INT = 100000
LARGE_INT = 1000000

def my_print(s):
    print "[" + str(datetime.now()) + "] " + s

def cap(G, e):
	return G.edge[e[0]][e[1]]['capacity']

def full_cap(G):
	return np.sum([G.edge[u][v]['capacity'] for u,v in G.edges_iter() if u>=0 and v<DEST_INT])

def full_cap_multi(G):
	return np.sum([d['capacity'] for u,v,k,d in G.edges_iter(keys=True,data=True) if u>=0 and v<DEST_INT])

def full_cap_all(G):
	return np.sum([G.edge[u][v]['capacity'] for u,v in G.edges_iter()])

def full_cap_multi_all(G):
	return np.sum([d['capacity'] for u,v,k,d in G.edges_iter(keys=True,data=True)])

def num_nodes(G):
	return len([n for n in G.nodes() if n>=0 and n<DEST_INT])

def num_edges(G):
	return len([(u,v) for (u,v) in G.edges() if u>=0 and v<DEST_INT])

def read_graph(in_fname):
	Gfull=nx.DiGraph(nodetype=int)
	with open(in_fname) as f:
		for line in f:
			arr = line.strip().split()
			if len(arr) == 3:
				src,dst,wei = int(arr[0]), int(arr[1]), int(arr[2])
				Gfull.add_edge(src, dst, capacity=wei, weight=1)
	return Gfull

def read_and_fix_graph(in_fname, max_capacity, num_sources, num_destinations):
	Gfull=nx.DiGraph(nodetype=int)
	with open(in_fname) as f:
		f.readline()
		for line in f:
			arr = line.strip().split()
			if len(arr) == 3:
				src,dst,wei = int(arr[0]), int(arr[1]), int(arr[2])
				wei = random.randint(10, max_capacity+10)
				Gfull.add_edge(src, dst, capacity=wei, weight=1)

	## add sources and destinations
	last_node = Gfull.number_of_nodes()-1
	for n in xrange(num_sources):
		Gfull.add_node(-n-1)
		for e in xrange(3):
			Gfull.add_edge(-n-1, random.randint(0, 5), capacity=10*max_capacity, weight=1)
	for n in xrange(num_destinations):
		Gfull.add_node(DEST_INT+n)
		for e in xrange(3):
			Gfull.add_edge(last_node-random.randint(0, 5), DEST_INT+n, capacity=10*max_capacity, weight=1)

	## break cycles
	do_run = True
	while do_run:
		try:
			c = nx.find_cycle(Gfull)
			for e in c:
				if e[0] > e[1]:
					c = Gfull[e[0]][e[1]]['capacity']
					Gfull.remove_edge(e[0], e[1])
					if Gfull.out_degree(e[0]) == 0:
						Gfull.add_edge(e[0], random.randint(e[0]+1, last_node), capacity=c)
					if Gfull.in_degree(e[1]) == 0:
						Gfull.add_edge(random.randint(0, e[1]-1), e[1], capacity=c)
		except:
			do_run = False
	return Gfull

def WPP(Gfull):
	## WPP
	do_wpp = True
	num_wpp_applied = 0
	G = Gfull.copy()
	while do_wpp:
		do_wpp = False
		for u,v in G.edges_iter():
			if u >= 0 and v < DEST_INT:
				c = cap(G, (u,v))
				I_e = np.sum([ cap(G, e_in) for e_in in G.in_edges(u) ])
				if c > I_e:
					G[u][v]['capacity'] = min(c, I_e)
					do_wpp = True
				O_e = np.sum([ cap(G, e_out) for e_out in G.out_edges(v) ])
				if c > O_e:
					G[u][v]['capacity'] = min(c, O_e)
					do_wpp = True
				if do_wpp:
					num_wpp_applied += 1
					break
	return G,num_wpp_applied, full_cap(G)

def DAGOPT(Gfull):
	## DAG-OPT
	do_dagopt = True
	num_dagopt_applied = 0
	G = Gfull.copy()
	while do_dagopt:
		do_dagopt = False
		for u,v in G.edges_iter():
			if u >= 0 and v < DEST_INT:
				GG = nx.DiGraph(nodetype=int)
				anc_set = nx.ancestors(G, u).union( set([u]) )
				desc_set = nx.descendants(G, v).union( set([v]) )
				GG.add_nodes_from([(n, G.node[n]) for n in anc_set])
				GG.add_nodes_from([(n, G.node[n]) for n in desc_set])
				GG.add_edge(u, v, G.edge[u][v])
				GG.add_edges_from([ (uu, vv, G.edge[uu][vv]) for uu,vv in G.edges(anc_set) if uu in anc_set and vv in anc_set ])
				GG.add_edges_from([ (uu, vv, G.edge[uu][vv]) for uu,vv in G.edges(desc_set) if uu in desc_set and vv in desc_set ])
				GG.add_node(-LARGE_INT)
				GG.add_node(LARGE_INT)
				GG.add_edges_from([ (-LARGE_INT, n) for n in GG.nodes() if n < 0])
				GG.add_edges_from([ (n, LARGE_INT) for n in GG.nodes() if n > DEST_INT])
				flowValue, flowDict = nx.maximum_flow(GG, -LARGE_INT, LARGE_INT)
				if flowValue < G.edge[u][v]['capacity']:
					# my_print('Maxflow capacity is smaller! Was %d now %d' % (G.edge[u][v]['capacity'], flowValue))
					G[u][v]['capacity'] = flowValue
					num_dagopt_applied += 1
					do_dagopt = True
					break
	return G,num_dagopt_applied, full_cap(G)


def routing_equivalent_multi(G_input):
	G = G_input.copy()
	num_routeeq_applied = 0
	do_routeeq = True
	# my_print('%d' % full_cap_multi(G))
	while do_routeeq:
		do_routeeq = False
		for u,v,k in G.edges_iter(keys=True):
			if u>=0 and v<DEST_INT and u != v:
				c = G.edge[u][v][k]['capacity']
				total_in = np.sum([ dd['capacity'] for uu,vv,kk,dd in G.in_edges(u,keys=True,data=True) if uu != vv])
				total_out = np.sum([ dd['capacity'] for uu,vv,kk,dd in G.out_edges(v,keys=True,data=True) if uu != vv])
				if c >= total_out or c >= total_in:
					# print u,v,k,c,total_out,total_in
					num_routeeq_applied += 1
					do_routeeq = True
					if c >= total_out:
						# my_print('Can apply to (%d,%d) with capacity %d >= total out %d; rewiring %d edges' % (u,v, c, total_out, np.sum([len(G.edge[uu][vv]) for uu,vv in G.out_edges(v)])))
						for uu,vv,kk,dd in G.out_edges(v, keys=True, data=True):
							G.add_edge(u, vv, len(G.edge[u].get(vv,{})), dd)
						for uu,vv,kk,dd in G.in_edges(v, keys=True, data=True):
							if uu != u or kk != k:
								G.add_edge(uu, u, len(G.edge[uu].get(u,{})), dd)
						G.remove_node(v)
						# my_print('%d' % full_cap_multi(G))
						break
					if c >= total_in:
						# my_print('Can apply to (%d,%d) with capacity %d >= total out %d; rewiring %d edges' % (u,v, c, total_out, np.sum([len(G.edge[uu][vv]) for uu,vv in G.in_edges(u)])))
						for uu,vv,kk,dd in G.in_edges(u, keys=True, data=True):
							G.add_edge(uu, v, len(G.edge[uu].get(v,{})), dd)
						for uu,vv,kk,dd in G.out_edges(u, keys=True, data=True):
							if vv != v or kk != k:
								G.add_edge(v, vv, len(G.edge[v].get(vv,{})), dd)
						G.remove_node(u)
						# my_print('%d' % full_cap_multi(G))
						break
				if do_routeeq:
					break
	return G, num_routeeq_applied

def convert_to_multi(G_input):
	G = nx.MultiDiGraph()
	G.add_nodes_from(G_input.nodes())
	G.add_edges_from([ (u, v, G_input.edge[u][v]) for u,v in G_input.edges_iter() ])
	return G

def routing_violating_multi(G_input):
	G = G_input.copy()
	do_routeineq = True
	numIter = 0
	while do_routeineq:
		numIter += 1
		do_routeineq = False
		G, num_routeeq_applied = routing_equivalent_multi(G)
		do_insideloop = True
		while do_insideloop:
			do_insideloop = False
			for u,v,k in G.edges_iter(keys=True):
				if u>=0 and v<DEST_INT:
					if u == v:
						# my_print('\t\tremoving loops at vertex %d' % u)
						G.remove_edges_from([(u, v, k) for k in G.edge[u][v]])
						do_insideloop = True
						do_routeineq = True
						break
					if len(G.edge[u][v]) > 1:
						# my_print('\t\tcompressing multiple edges from %d to %d' % (u, v))
						tot = np.sum([x['capacity'] for x in G.edge[u][v].values()])
						G.remove_edges_from([(u, v, k) for k in G.edge[u][v]])
						G.add_edge(u, v, 0, {'capacity' : tot, 'weight' : 1})					
						do_insideloop = True
						do_routeineq = True
						break
		# my_print('\tafter roineq |V|=%d, |E|=%d, total cap=%d' % (G.number_of_nodes(), G.number_of_edges(), full_cap_multi(G)))
	return G, numIter

def tradeoff(G_input, func_equiv=routing_violating_multi):
	G = G_input.copy()
	do_tradeoff = True
	total_added_cap = 0
	numIter = 0
	while do_tradeoff:
		numIter += 1
		do_tradeoff = False
		# my_print('Iteration %d:' % numIter)
		G, num_routeviol = func_equiv(G)
		# my_print('\treduced in %d iterations to |V|=%d, |E|=%d' % (num_routeviol, G.number_of_nodes(), G.number_of_edges()))
		edges_candidates = [(u,v,k,d['capacity']) for u,v,k,d in G.edges_iter(keys=True,data=True) if u>=0 and v<DEST_INT and candidate_filter_edge(G, u, v)]
		if len(edges_candidates) > 0:
			do_tradeoff = True
			cand_c = [x[3] for x in edges_candidates]
			cand_Ie = [np.sum([dd['capacity'] for uu,vv,kk,dd in G.in_edges(u, keys=True, data=True) if uu != vv]) for u,v,k,c in edges_candidates]
			cand_Oe = [np.sum([dd['capacity'] for uu,vv,kk,dd in G.out_edges(v, keys=True, data=True) if uu != vv]) for u,v,k,c in edges_candidates]
			cand_amin = np.argmin(np.min(np.vstack([np.array(cand_Ie)-np.array(cand_c), np.array(cand_Oe)-np.array(cand_c)]), axis=0))
			cand_toadd = min(cand_Ie[cand_amin]-cand_c[cand_amin], cand_Oe[cand_amin]-cand_c[cand_amin])
			u,v,k,c = edges_candidates[cand_amin]
			# my_print('\tadding %d to edge (%d, %d) with cap %d' % ( cand_toadd, u, v, c ))
			total_added_cap += cand_toadd
			G.edge[u][v][k]['capacity'] = c + cand_toadd
	return G, numIter, total_added_cap


def candidate_filter_edge(G, u, v):
	if u == v:
		return False
	for uu,vv in G.in_edges(u):
		if uu < 0:
			return False
	for uu,vv in G.out_edges(v):
		if vv >= DEST_INT:
			return False
	return True
