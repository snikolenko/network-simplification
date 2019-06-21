import networkx as nx
import random
import numpy as np
from datetime import datetime,time,date,timedelta

from graph_heuristics import *

in_fname = "~/topobench/graph.0.txt"
num_sources = 5
num_destinations = 5
max_capacity = 20
DEST_INT = 100000
LARGE_INT = 1000000


my_print('G capacity = %d' % full_cap(Gfull))

## WPP
do_wpp = True
num_wpp_applied = 0
G = Gfull.copy()
while do_wpp:
	do_wpp = False
	for e in G.edges_iter():
		c = cap(G, e)
		if e[0] >= 0:
			I_e = np.sum([ cap(G, e_in) for e_in in G.in_edges(e[0]) ])
			if c > I_e:
				my_print("\tedge %s has cap=%d > I_e=%d" % (e, cap(G, e), I_e))
				G[e[0]][e[1]]['capacity'] = min(c, I_e)
				do_wpp = True
		if e[1] < DEST_INT:
			O_e = np.sum([ cap(G, e_out) for e_out in G.out_edges(e[1]) ])
			if c > O_e:
				my_print("\tedge %s has cap=%d > O_e=%d" % (e, c, O_e))
				G[e[0]][e[1]]['capacity'] = min(c, O_e)
				do_wpp = True
		if do_wpp:
			num_wpp_applied += 1
			break

my_print('Applied WPP %d times, got total capacity = %d' % (num_wpp_applied, full_cap(G)) )


## WPP
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
				my_print('Maxflow capacity is smaller! Was %d now %d' % (G.edge[u][v]['capacity'], flowValue))
				G[u][v]['capacity'] = flowValue
				num_dagopt_applied += 1
				do_dagopt = True
				break

my_print('Applied DAGOPT %d times, got total capacity = %d' % (num_dagopt_applied, full_cap(G)) )



np.sum([G.edge[e[0]][e[1]]['capacity'] for e in G.edges_iter()])


max_capacity = 20
Gfull = read_and_fix_graph(in_fname)

num_routeeq_applied = 0
G = nx.MultiDiGraph()
G.add_nodes_from(Gfull.nodes())
G.add_edges_from([ (u, v, Gfull.edge[u][v]) for u,v in Gfull.edges_iter() ])


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
					print u,v,k,c,total_out,total_in
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

G = nx.MultiDiGraph()
G.add_nodes_from(Gfull.nodes())
G.add_edges_from([ (u, v, Gfull.edge[u][v]) for u,v in Gfull.edges_iter() ])

do_routeineq = True
numIter = 0
while do_routeineq:
	numIter += 1
	do_routeineq = False
	my_print('Iteration %d:')
	my_print('\tstarted from |V|=%d, |E|=%d, total cap=%d' % (G.number_of_nodes(), G.number_of_edges(), full_cap_multi(G)))
	G, num_routeeq_applied = routing_equivalent_multi(G)
	my_print('\tafter routeq |V|=%d, |E|=%d, total cap=%d' % (G.number_of_nodes(), G.number_of_edges(), full_cap_multi(G)))
	do_insideloop = True
	while do_insideloop:
		do_insideloop = False
		for u,v in G.edges_iter():
			if u>=0 and v<DEST_INT:
				if u == v:
					my_print('\t\tremoving loops at vertex %d' % u)
					G.remove_edges_from([(u, v, k) for k in G.edge[u][v]])
					do_insideloop = True
					do_routeineq = True
					break
				if len(G.edge[u][v]) > 1:
					my_print('\t\tcompressing multiple edges from %d to %d' % (u, v))
					tot = np.sum([x['capacity'] for x in G.edge[u][v].values()])
					G.remove_edges_from([(u, v, k) for k in G.edge[u][v]])
					G.add_edge(u, v, 0, {'capacity' : tot, 'weight' : 1})					
					do_insideloop = True
					do_routeineq = True
					break
	my_print('\tafter roineq |V|=%d, |E|=%d, total cap=%d' % (G.number_of_nodes(), G.number_of_edges(), full_cap_multi(G)))



Gset = set([(u,v,k) for u,v in G.edges() for k in G.edge[u][v]])
GGset = set([(u,v,k) for u,v in GG.edges() for k in GG.edge[u][v]])

for u,v,k in Gset:
	if not (u,v,k) in GGset or G.edge[u][v][k]['capacity'] != GG.edge[u][v][k]['capacity']:
		print u,v,k,G.edge[u][v][k]['capacity']

for u,v,k in GGset:
	if not (u,v,k) in Gset or G.edge[u][v][k]['capacity'] != GG.edge[u][v][k]['capacity']:
		print u,v,k,GG.edge[u][v][k]['capacity']

np.sum([G.edge[u][v][k]['capacity'] for u,v,k in Gset])
np.sum([GG.edge[u][v][k]['capacity'] for u,v,k in GGset])

d = {}
for u,v in G.edges():
	if (u,v) in d:
		print u,v
	else:
		d[(u,v)] = True


GGmG = list(set([(u,v,k) for u,v in GG.edges() for k in GG.edge[u][v]]) - set([(u,v,k) for u,v in G.edges() for k in G.edge[u][v]]))

for uu,vv,kk in GGmG:
	print uu,vv,kk,GG.edge[uu][vv][kk]
print ""
for uu,vv,kk in GmGG:
	print uu,vv,kk,G.edge[uu][vv][kk]

for u,v in G.edges_iter():
	for k in G.edge[u][v]:
		if (u,v) in GG.edges() and k in GG.edge[u][v] and G.edge[u][v][k]['capacity'] != GG.edge[u][v][k]['capacity']:
			print u,v,k, GG.edge[u][v][k], G.edge[u][v][k]

for u,v in GG.edges_iter():
	for k in GG.edge[u][v]:
		if (u,v) in G.edges() and k in G.edge[u][v] and GG.edge[u][v][k]['capacity'] != G.edge[u][v][k]['capacity']:
			print u,v,k,GG.edge[u][v][k],G.edge[u][v][k]



def candidate_filter_edge(G, u, v):
	for uu,vv in G.in_edges(u):
		if uu < 0:
			return False
	for uu,vv in G.out_edges(v):
		if vv >= DEST_INT:
			return False
	return True

G = Gdagopt_m.copy()
do_tradeoff = True
total_added_cap = 0
numIter = 0
while do_tradeoff:
	numIter += 1
	do_tradeoff = False
	my_print('Iteration %d:' % numIter)
	G, num_routeviol = routing_equivalent_multi(G)
	my_print('\treduced in %d iterations to |V|=%d, |E|=%d' % (num_routeviol, G.number_of_nodes(), G.number_of_edges()))
	edges_candidates = [(u,v,k,d['capacity']) for u,v,k,d in G.edges_iter(keys=True,data=True) if u>=0 and v<DEST_INT and candidate_filter_edge(G, u, v)]
	if len(edges_candidates) > 0:
		do_tradeoff = True
		cand_c = [x[3] for x in edges_candidates]
		cand_Ie = [np.sum([dd['capacity'] for uu,vv,kk,dd in G.in_edges(u, keys=True, data=True)]) for u,v,k,c in edges_candidates]
		cand_Oe = [np.sum([dd['capacity'] for uu,vv,kk,dd in G.out_edges(v, keys=True, data=True)]) for u,v,k,c in edges_candidates]
		cand_amin = np.argmin(np.min(np.vstack([np.array(cand_Ie)-np.array(cand_c), np.array(cand_Oe)-np.array(cand_c)]), axis=0))
		cand_toadd = min(cand_Ie[cand_amin]-cand_c[cand_amin], cand_Oe[cand_amin]-cand_c[cand_amin])
		u,v,k,c = edges_candidates[cand_amin]
		my_print('\tadding %d to edge (%d, %d) with cap %d' % ( cand_toadd, u, v, c ))
		total_added_cap += cand_toadd
		G.edge[u][v][k]['capacity'] = c + cand_toadd


len([n for n in G.nodes() if n>=0 and n<DEST_INT])



