#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:29:37 2020
by Fernando P. L. Marques

This script used as input file the output of the script DFOIL_Picker_mod.R \
contaning terminal names and the four populations to be tested ("p1", "p2", "p3", "p4"), \
the outgroup taxa and the dfoil mode (dfoi or dfoil). \

It returns a file that can be used as input for the script dfoilator.py.

"""

import sys

import pandas as pd

# Check if a file name was provided as the first argument
if len(sys.argv) < 4:
    print("Usage: python my_script.py <file_name> <outgroup_taxa> <dfoil_mode>")
    print()
    print("    Example: ./prep4dfoiliator.py PA07_13_tests.txt JP1230_S13_Trim2 dfoi")
    sys.exit(1)

# Get the file name from the first argument
file_name = sys.argv[1]
outgroup = sys.argv[2]
dfoil_option = sys.argv[3]

# Read the data from the file
df = pd.read_csv(file_name, sep=" ", header=None)

# Add headers to the data frame
df.columns = ["p1", "p2", "p3", "p4"]

# Get the number of rows in the data frame
num_rows = df.shape[0]

# making new columns

dfoil_mode = [dfoil_option] * num_rows
out = [outgroup] * num_rows
test_name = []
num_digits = len(str(num_rows))

for n in range(1, num_rows + 1):
    counter = f"{{:0{num_digits}d}}".format(n)
    test = "test_" + counter
    test_name.append(test)


tobeadded_df = pd.DataFrame(
    {"test_name": test_name, "dfoil_mode": dfoil_mode, "out": out}
)

# Add the new columns to the data frame
df = pd.concat([df, tobeadded_df], axis=1)

# Reorder the columns of the data frame
df = df[["test_name", "p1", "p2", "p3", "p4", "out", "dfoil_mode"]]


# Print the first 5 rows of the DataFrame
print(df.head(5))
print()
outfile = file_name.split(".")[0] + ".tsv"
print(f"Output file: {outfile}")
df.to_csv(outfile, sep="\t", index=False)
# print(len(str(num_rows)))
# print(tobeadded_df.head(5))
# print(out)
