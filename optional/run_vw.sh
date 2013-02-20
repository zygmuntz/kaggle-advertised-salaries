#!/bin/bash

# a script for running validation

vw -d data/train_v.vw -c -f model --passes 20

vw -t -d data/test_v.vw -c -i model -p data/p.txt

python mae.py data/test_v.vw data/p.txt

# MAE: 7148.75808773