# network-simplification
Code for the "New Network Simplification Algorithms: A Tradeoff Between Simplicity and Capacity" paper. Subdirectories hold various graph topologies used in the evaluation study in the paper.

### Dependencies
The code should be run with Python 2.7. It requires `numpy`, `networkx`, and `python-louvain` Python packages (the latter with version not exceeding 0.9) that can be installed through
```
pip install numpy networkx 'python-louvain<0.9'
```

### Running the code
To run the DAGOPT and WPP algorithms on a single graph, run
```
python table_capacity.py filename
```
where `filename` is a topology graph file. The code outputs TeX table format for different values of maximal capacity; sample output:
```
> python table_capacity.py jellyfish_s5_d5/graph.20.20.30.20.10.16.cap10.txt
jellyfish_s5_d5/graph.20.20.30.20.10.16.cap10.txt & 55 & 307 & 5 & 3241 & 10 & 3214 & 19 & 3040 \\
jellyfish_s5_d5/graph.20.20.30.20.10.16.cap10.txt & 55 & 302 & 10 & 3881 & 20 & 3807 & 26 & 3624 \\
jellyfish_s5_d5/graph.20.20.30.20.10.16.cap10.txt & 56 & 303 & 20 & 5284 & 22 & 5135 & 27 & 4881 \\
jellyfish_s5_d5/graph.20.20.30.20.10.16.cap10.txt & 56 & 309 & 50 & 9240 & 26 & 8862 & 31 & 8426 \\
```

To reproduce Table I, "Evaluation results for capacity planning and topology reduction algorithms", run
```
python table_topology.py dir
```
where `dir` is a directory with topology graphs. The code outputs TeX table format; sample output:
```
> python table_topology.py jellyfish_s5_d5
20\_30\_30\_20\_12\_14\_cap10 & 60 & 360 & 100 & 1883 & 1829 & 1692 & 43 & 330 & 1817 & 43 & 330 & 1777 & 43 & 330 & 1641 & 43 & 317 & 1817 & 43 & 317 & 1777 & 43 & 316 & 1641\\
20\_40\_30\_20\_25\_9\_cap10 & 70 & 461 & 100 & 2486 & 2217 & 2216 & 53 & 427 & 2437 & 48 & 422 & 2171 & 49 & 423 & 2177 & 53 & 416 & 2437 & 48 & 401 & 2171 & 49 & 404 & 2177\\
20\_30\_30\_20\_18\_11\_cap5 & 60 & 372 & 50 & 1026 & 931 & 931 & 42 & 339 & 999 & 42 & 339 & 912 & 42 & 339 & 912 & 41 & 311 & 992 & 41 & 311 & 905 & 41 & 311 & 905\\
20\_30\_30\_20\_12\_15\_cap10 & 60 & 368 & 100 & 1880 & 1689 & 1422 & 38 & 333 & 1786 & 38 & 333 & 1619 & 36 & 331 & 1354 & 38 & 292 & 1768 & 38 & 309 & 1619 & 36 & 299 & 1354\\
...
```

To reproduce Table II, "Evaluation results for trading capacity for simplicity", run
```
python table_tradeoff.py dir
```
where `dir` is a directory with topology graphs. The code outputs TeX table format; sample output:
```
> python table_tradeoff.py jellyfish_s5_d5
20\_30\_30\_20\_12\_14\_cap10 & 50 & 337 & 10 & 1883 & 1692 & 43 & 330 & 1641 & 1011 & 11 & 298 & 1367 & 43 & 316 & 1641 & 622 & 11 & 31 & 659\\
20\_40\_30\_20\_25\_9\_cap10 & 60 & 434 & 10 & 2486 & 2216 & 49 & 423 & 2177 & 1096 & 10 & 384 & 1842 & 49 & 404 & 2177 & 462 & 10 & 33 & 945\\
20\_30\_30\_20\_18\_11\_cap5 & 50 & 347 & 5 & 1026 & 931 & 42 & 339 & 912 & 576 & 11 & 308 & 776 & 41 & 311 & 905 & 425 & 11 & 40 & 586\\
20\_30\_30\_20\_12\_15\_cap10 & 50 & 345 & 10 & 1880 & 1422 & 36 & 331 & 1354 & 919 & 9 & 304 & 1138 & 36 & 299 & 1354 & 814 & 9 & 31 & 899\\
...
```
