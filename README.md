# dfoiliator
This is a script to run a pipeline to [DFOIL](https://github.com/jbpease/dfoil/) analyses.

## Workflow

### Here is the example we will explore

![alt text](https://github.com/fplmarques/dfoiliator/blob/main/test_files/clade_01_test.png)

### 1. Compile all possible test ((p1,p2)(p3,p4)) based on a rooted tree and a list of terminals

Here I am using a complete rooted topology (in rooted.tre) and a list of terminals that, in this case, include all terminals of the clade above (tax_names.txt).

```sh
Rscript DFOIL_Picker_mod.R -n tax_names.txt -t rooted.tre
```
