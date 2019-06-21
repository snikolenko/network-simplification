import networkx as nx
import random
import sys
import numpy as np
from datetime import datetime,time,date,timedelta

from graph_heuristics import *

in_fname = sys.argv[1]

num_sources = 5
num_destinations = 5
if len(sys.argv) > 3:
	num_sources = int(sys.argv[2])
	num_destinations = int(sys.argv[3])


for max_capacity in [5, 10, 20, 50]:
	Gfull = read_and_fix_graph(in_fname, max_capacity, num_sources, num_destinations)
	init_totalcap = full_cap(Gfull)

	Gwpp, num_wpp_applied, res_totalcap_wpp = WPP(Gfull)
	Gdagopt, num_dagopt_applied, res_totalcap_dagopt = DAGOPT(Gfull)

	print 'fattree & %d & %d & %d & %d & %d & %d & %d & %d \\\\' % ( Gfull.number_of_nodes(), Gfull.number_of_edges(), max_capacity, init_totalcap, num_wpp_applied, res_totalcap_wpp, num_dagopt_applied, res_totalcap_dagopt )


exit(0)

