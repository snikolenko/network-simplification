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
	max_capacity = np.max([Gfull.edge[u][v]['capacity'] for u,v in Gfull.edges_iter()])
	init_totalcap = full_cap(Gfull)

	Gwpp, num_wpp_applied, res_totalcap_wpp = WPP(Gfull)
	Gdagopt, num_dagopt_applied, res_totalcap_dagopt = DAGOPT(Gfull)

	Gfull_m = convert_to_multi(Gfull)
	Gwpp_m = convert_to_multi(Gwpp)
	Gdagopt_m = convert_to_multi(Gdagopt)

	Gfull_req, full_req_iters = routing_equivalent_multi(Gfull_m)
	Gwpp_req, wpp_req_iters = routing_equivalent_multi(Gwpp_m)
	Gdagopt_req, dgopt_req_iters = routing_equivalent_multi(Gdagopt_m)

	Gfull_rineq, full_rineq_iters = routing_violating_multi(Gfull_m)
	Gwpp_rineq, wpp_rineq_iters = routing_violating_multi(Gwpp_m)
	Gdagopt_rineq, dgopt_rineq_iters = routing_violating_multi(Gdagopt_m)

	tuple_toprint = (Gfull.number_of_nodes(), Gfull.number_of_edges(), max_capacity, init_totalcap,
		res_totalcap_wpp, res_totalcap_dagopt,
		num_nodes(Gfull_req), num_edges(Gfull_req), full_cap_multi(Gfull_req),
		num_nodes(Gwpp_req), num_edges(Gwpp_req), full_cap_multi(Gwpp_req),
		num_nodes(Gdagopt_req), num_edges(Gdagopt_req), full_cap_multi(Gdagopt_req),
		num_nodes(Gfull_rineq), num_edges(Gfull_rineq), full_cap_multi(Gfull_rineq),
		num_nodes(Gwpp_rineq), num_edges(Gwpp_rineq), full_cap_multi(Gwpp_rineq),
		num_nodes(Gdagopt_rineq), num_edges(Gdagopt_rineq), full_cap_multi(Gdagopt_rineq)
	)

	print ('_'.join(in_fname.split('.')[1:-1]).replace('_', '\_') + ' & %d' * len(tuple_toprint) + '\\\\') % tuple_toprint
	sys.stdout.flush()

exit(0)

