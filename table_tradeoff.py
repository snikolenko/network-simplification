import networkx as nx
import random
import glob
import sys
import numpy as np
from datetime import datetime,time,date,timedelta

from graph_heuristics import *

in_dir = sys.argv[1]

num_sources = 5
num_destinations = 5
if len(sys.argv) > 3:
	num_sources = int(sys.argv[2])
	num_destinations = int(sys.argv[3])

for in_fname in glob.glob(in_dir + '/graph*.txt'):
	Gfull = read_graph(in_fname)
	init_totalcap = full_cap(Gfull)
	max_capacity = np.max([Gfull.edge[u][v]['capacity'] for u,v in Gfull.edges_iter()  if u>=0 and v<DEST_INT])
	init_numnodes, init_numedges = num_nodes(Gfull), num_edges(Gfull)

	# Gwpp, num_wpp_applied, res_totalcap_wpp = WPP(Gfull)
	Gdagopt, num_dagopt_applied, res_totalcap_dagopt = DAGOPT(Gfull)

	Gdagopt_m = convert_to_multi(Gdagopt)

	Gdagopt_req, dgopt_req_iters = routing_equivalent_multi(Gdagopt_m)
	dagopt_req_numnodes,dagopt_req_numedges = num_nodes(Gdagopt_req), num_edges(Gdagopt_req)

	Gdagopt_rineq, dgopt_rineq_iters = routing_violating_multi(Gdagopt_m)
	dagopt_rineq_numnodes,dagopt_rineq_numedges = num_nodes(Gdagopt_rineq), num_edges(Gdagopt_rineq)

	Gtradeoff_eq, numIter_tradeoff_eq, total_added_cap_eq = tradeoff(Gdagopt_req, func_equiv=routing_equivalent_multi)
	tradeoff_req_numnodes,tradeoff_req_numedges = num_nodes(Gtradeoff_eq), num_edges(Gtradeoff_eq)

	Gtradeoff, numIter_tradeoff, total_added_cap = tradeoff(Gdagopt_rineq)
	tradeoff_rineq_numnodes, tradeoff_rineq_numedges = num_nodes(Gtradeoff), num_edges(Gtradeoff)

	tuple_toprint = (init_numnodes, init_numedges, max_capacity, init_totalcap,
		res_totalcap_dagopt,
		dagopt_req_numnodes, dagopt_req_numedges, full_cap_multi(Gdagopt_req),
		total_added_cap_eq, tradeoff_req_numnodes, tradeoff_req_numedges, full_cap_multi(Gtradeoff_eq),
		dagopt_rineq_numnodes, dagopt_rineq_numedges, full_cap_multi(Gdagopt_rineq),
		total_added_cap, tradeoff_rineq_numnodes, tradeoff_rineq_numedges, full_cap_multi(Gtradeoff)
	)

	print ('_'.join(in_fname.split('.')[1:-1]).replace('_', '\_') + ' & %d' * len(tuple_toprint) + '\\\\') % tuple_toprint
	sys.stdout.flush()

exit(0)

