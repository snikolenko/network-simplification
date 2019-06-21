import networkx as nx
import random
import glob
import sys
import numpy as np
from datetime import datetime,time,date,timedelta

from graph_heuristics import *

in_dir = sys.argv[1]
out_dir = sys.argv[2]

num_sources = 5
num_destinations = 5
if len(sys.argv) > 4:
	num_sources = int(sys.argv[3])
	num_destinations = int(sys.argv[4])


for in_fname in glob.glob(in_dir + '/graph*.txt'):
	for max_capacity in [145]:
		Gfull = read_and_fix_graph(in_fname, max_capacity, num_sources, num_destinations)
		with open(out_dir + '/' + in_fname.split('/')[-1][:-4] + ('.cap%d' % max_capacity) + '.txt', 'w') as outf:
			for u,v in Gfull.edges_iter():
				outf.write("%d %d %d\n" % (u, v, Gfull[u][v]['capacity']))



