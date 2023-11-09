#!/bin/bash
#
# usage: 
#      ./check_dfoiliator_results.sh <int>
#
# This script just uses grep and awk to parse *_summary_results.tsv from dfoiliator.py runs.
# It will only work if you adopt the prefix "test_0<int>"
# However you can use the logic applied here to to reach the same results regardless of how you name your tests.
# Because this command line only sorts unique records for terminals of interest (i.e., p1 and p5),
# it reduces the number of events of introgression reported in comparison to what is found in  *_summary_results.tsv
# It is recommended to evaluate the number of tests performed and make appropriate corrections to p-values (Bonferroni procedure)
#
#                                                    Fernando P. L. Marques Nov. 2023
#

TEST=$1

echo ""
echo "Results (P1 ⇒ P3):"
grep 'P1 ⇒ P3' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $2 "\t==>\t" $4}' | sort -u

echo ""
echo "Results (P1 ⇒ P4):"
grep 'P1 ⇒ P4' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $2 "\t==>\t" $5}' | sort -u

echo ""
echo "Results (P2 ⇒ P3):"
grep 'P2 ⇒ P3' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $3 "\t==>\t" $4}' | sort -u


echo ""
echo "Results (P3 ⇒ P1):"
grep 'P3 ⇒ P1' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $4 "\t==>\t" $2}' | sort -u

echo ""
echo "Results (P4 ⇒ P1):"
grep 'P4 ⇒ P1' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $5 "\t==>\t" $2}' | sort -u

echo ""
echo "Results (P3 ⇒ P2):"
grep 'P3 ⇒ P2' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $4 "\t==>\t" $3}' | sort -u

echo " "
echo "Results (P12 ⇔ P3):"
grep 'P12 ⇔ P3' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $2 "+" $3 "\t<==>\t" $4}' | sort -u
echo ""
echo "Results (P12 ⇔ P4):"
grep 'P12 ⇔ P4' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $2 "+" $3 "\t<==>\t" $5}' | sort -u

echo " "
echo "Results (P3 ⇔ P12):"
grep 'P3 ⇔ P12' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $4 "\t<==>\t" $2 "+" $3}' | sort -u
echo ""
echo "Results (P4 ⇔ P12):"
grep 'P4 ⇔ P12' ./test_0${TEST}/test_0${TEST}_summary_results.tsv | awk -F'\t' '{print $5 "\t<==>\t" $2 "+" $3}' | sort -u




