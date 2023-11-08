# dfoiliator
This is a script to run a pipeline to [DFOIL](https://github.com/jbpease/dfoil/) analyses.

## Requirements
[DFOIL](https://github.com/jbpease/dfoil/) executables

[bcftools](https://www.htslib.org/download/)

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
The argument **JP13041_S47_Trim2** refers to the outgroup required in DFOIL analyses and **dfoil** especify the mode in which *dfoil.py* will be executed.

This command line will generate the file **test_01.tsv** with the following structure:

```
test_name	p1	p2	p3	p4	out	dfoil_mode
test_01	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12965_S35_Trim2	JP13041_S47_Trim2	dfoil
test_02	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12963_S106_Trim2	JP13041_S47_Trim2	dfoil
test_03	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12974_S108_Trim2	JP13041_S47_Trim2	dfoil
test_04	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP10115_S89_Trim2	JP13041_S47_Trim2	dfoil
...
```
#### 4. Run dfoiliator:


Run *dfoiliator.py* with the following command line:

```bash
./dfoiliator.py -i test_snps.vcf -t test_01.tsv
```

The option *-i* defines the input file. It can be in .vcf or *.fas formats. If the input file is a VCF, [bcftools](https://www.htslib.org/download/) will be required, and *.tab (from vcf-to-tab) and *.fas will be created.

All files associated with this command line will be stored in the directory **test_01/**, in which the file *test_01_summary_results.tsv* will summarize all the results.

#### 5. Evaluating the results of the dfoiliator run:

You can sort the file *test_01_summary_results.tsv* by its last column in which you can potentially find the direction of the introgression event:

```bash
sort -t$'\t' -k9,9 ./test_01/test_01_summary_results.tsv
```

It should result in something like this:

```
test_name	p1	p2	p3	p4	out	dfoil_mode	signature	introgression
...
test_51	MT12_005	MT12_004	JP12895_S103_Trim2	JP12959_S93_Trim2	JP13041_S47_Trim2	dfoil	0 0 - -	No Introgression
test_13	MT12_004	JP12959_S93_Trim2	JP12965_S35_Trim2	JP10114_S95_Trim2	JP13041_S47_Trim2	dfoil	+ + 0 0	P12 ⇔ P3
test_17	MT12_004	JP12959_S93_Trim2	JP12963_S106_Trim2	JP10117_S88_Trim2	JP13041_S47_Trim2	dfoil	+ + 0 0	P12 ⇔ P3
test_36	JP12893_S21_Trim2	MT12_004	JP12959_S93_Trim2	JP12956_S83_Trim2	JP13041_S47_Trim2	dfoil	+ + 0 0	P12 ⇔ P3
test_45	JP12893_S21_Trim2	MT12_004	JP12959_S93_Trim2	MS04_09	JP13041_S47_Trim2	dfoil	+ + 0 0	P12 ⇔ P3
test_01	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12965_S35_Trim2	JP13041_S47_Trim2	dfoil	- - 0 0	P12 ⇔ P4
test_02	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12963_S106_Trim2	JP13041_S47_Trim2	dfoil	- - 0 0	P12 ⇔ P4
test_03	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP12974_S108_Trim2	JP13041_S47_Trim2	dfoil	- - 0 0	P12 ⇔ P4
test_05	MT12_004	JP12959_S93_Trim2	JP12875_S24_Trim2	JP10116_f_Trim2	JP13041_S47_Trim2	dfoil	- - 0 0	P12 ⇔ P4
test_38	MT12_004	MT12_001	JP12959_S93_Trim2	JP12956_S83_Trim2	JP13041_S47_Trim2	dfoil	+ + + 0	P1 ⇒ P3
test_47	MT12_004	MT12_001	JP12959_S93_Trim2	MS04_09	JP13041_S47_Trim2	dfoil	+ + + 0	P1 ⇒ P3
...
```

Alternatively, you can use the script *check_dfoliator_results.sh* to summarize the results. This script ignores all tests that did not find evidence for introgression and assumes that you have used the notation 'test_0*' as a prefix of your test. Accordingly, you should execute the following command line:

```bash
./check_dfoliator_results.sh 1
```

In this command line, the argument '1' refers to the test name index (i.e., test_01).
The result should be:

```
Results (P1 ⇒ P3):
MT12_004	==>	JP12959_S93_Trim2

Results (P1 ⇒ P4):

Results (P2 ⇒ P3):

Results (P3 ⇒ P1):

Results (P4 ⇒ P1):

Results (P3 ⇒ P2):
...
```
In this particular example, the event Results (P1 ⇒ P3): MT12_004	==>	JP12959_S93_Trim2 represents the red arrow depicted in the figure above representing the direction of introgression from *Potamotrygon motoro* ex Rio Paraguai - Rio Cuiaba \[MT12-004\]to	*Potamotrygon falkneri* ex Rio Paraguai \[BZ-13/MZUSP 117820\]

