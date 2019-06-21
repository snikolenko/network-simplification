# network-simplification
Code for the "New Network Simplification Algorithms: A Tradeoff Between Simplicity and Capacity" paper. Subdirectories hold various graph topologies used in the evaluation study in the paper.

To reproduce Table I, "Evaluation results for capacity planning and topology reduction algorithms", run
```
python table_capacity.py dir
```
where `dir` is a directory with topology graphs.

To reproduce Table II, "Evaluation results for trading capacity for simplicity", run
```
python table_tradeoff.py dir
```
where `dir` is a directory with topology graphs.

