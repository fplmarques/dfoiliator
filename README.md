# dfoiliator
This is a script to run a pipeline to [DFOIL](https://github.com/jbpease/dfoil/) analyses.

## Workflow

### Here is the example we will explore

![alt text](https://github.com/fplmarques/dfoiliator/blob/main/test_files/clade_01_test.png)

### Compile all possible test ((p1,p2)(p3,p4)) based on a rooted tree and a list of terminals

Here I am using a complete rooted topology (rooted.tre) and a list of terminals that, in this case, include all terminals of the clade above (tax_names.txt).

```basg
Rscript DFOIL_Picker_mod.R -n tax_names.txt -t rooted.tre
```

This command line will generate the file *four_taxa_sets.txt* with 3611 sets of tests that can be made based on the topology:

```
JP13241_S20_Trim2 JP12962_S105_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP12958_S104_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP12893_S21_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 MT12_005 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 MT12_004 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 MT12_001 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP13007_S22_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP12957_S92_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP12895_S103_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
JP13241_S20_Trim2 JP12959_S93_Trim2 JP12875_S24_Trim2 JP12965_S35_Trim2
...

```
