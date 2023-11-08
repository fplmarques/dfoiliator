#!/bin/bash

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




