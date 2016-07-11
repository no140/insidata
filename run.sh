#!/usr/bin/env bash

# example of the run script for running the rolling_median calculation with a python file, 
# but could be replaced with similar files from any major language

# I'll execute my programs, with the input directory venmo_input and output the files in the directory venmo_output

python3 ./src/rolling_median_noplot_opt.py ./venmo_input/venmo-trans.txt ./venmo_output/output.txt
#python3 ./src/rolling_median_noplot.py ./venmo_input/venmo-trans.txt ./venmo_output/output.txt
#python3 ./src/rolling_median_netwk_noplot.py ./venmo_input/venmo-trans.txt ./venmo_output/output.txt
#python3 ./src/rolling_median_netwk.py ./venmo_input/venmo-trans.txt ./venmo_output/output.txt



