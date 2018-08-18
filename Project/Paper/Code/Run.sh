#!/bin/bash
# This program requires that there be no file called outfile.csv in the Data directory.

# Reads and cleans the raw data.
python datacleaner.py

# Turns the cleaned data into prices and outputs to outfile.csv
Rscript modeler.R

# Does the simulation.
python snakes.py

# Makes pictures of the output of the simulation.
Rscript prettypictures.R