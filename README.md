# dfoiliator
This is a script to run a pipeline to [DFOIL](https://github.com/jbpease/dfoil/) analyses.

## Workflow

### Here is the example we will explore

![alt text](https://github.com/fplmarques/dfoiliator/blob/main/test_files/clade_01_test.png)

#### 1. Compile all possible tests ((p1,p2)(p3,p4)) based on a rooted tree and a list of terminals:

Here I am using a complete rooted topology (rooted.tre) and a list of terminals that, in this case, include all terminals of the clade above (tax_names.txt).

```bash
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

#### 2. Determine the taxa involved in the test and extract four-taxon trees that include them:

For T1 (test 01) we want to evaluate the direction of introgression between terminals *Potamotrygon motoro* ex Rio Paraguai - Rio Cuiaba \[MT12-004\]	<==>	*Potamotrygon falkneri* ex Rio Paraguai \[BZ-13/MZUSP 117820\]

The sequence names associated with these terminals are **MT12_004**  and **JP12959_S93_Trim2**, respectively.

To extract the four-taxon trees that include both terminals, you should run this command line in your terminal:

```bash
grep MT12_004 four_taxa_sets.txt | grep JP12959_S93_Trim2 > test_01.txt
```

This command will write the file **test_01.txt** which should contain 52 lines.


#### 3. Prepare the input file for dfoiliator:

The output of the previous command line will be used to create a *.tsv file that will be used as the input file for dfoiliator.

You should run the following command line:

```bash
./prep4dfoiliator.py test_01.txt JP13041_S47_Trim2 dfoil
```
The argument **JP13041_S47_Trim2** refers to the outgroup required in DFOIL analyses and **dfoil** especify the mode in which dfoil.py will be executed.

This command line will generate the file **test_01.tsv** with the following structure:

```
test_name	p1	p2	p3	p4	out	dfoil_mode
test_01	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12965_S35_Trim2	JP13041_S47_Trim2	dfoil
test_02	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12963_S106_Trim2	JP13041_S47_Trim2	dfoil
test_03	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12974_S108_Trim2	JP13041_S47_Trim2	dfoil
test_04	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP10115_S89_Trim2	JP13041_S47_Trim2	dfoil
...
```


./dfoiliator.py -i potamotrygon_reference_91_clade_01dsuit.fas -t test_04.tsv
sort -t$'\t' -k9,9 ./test_04/test_04_summary_results.tsv
./check_dfoliator_results.sh



