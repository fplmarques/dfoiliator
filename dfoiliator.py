#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 2 15:29:37 2020
by Fernando P. L. Marques
"""

import argparse
import os
import re
import subprocess
from math import e
from sys import prefix
from turtle import st

import pandas as pd
from Bio import SeqIO


#
## First set of funcion to test introgression cenarios using Dfoil
#
def processing_input_files() -> (str, pd.DataFrame):
    """
    This function process the input files and returns the name of the fasta file and a pandas dataframe with the tests to be performed by DFOIL.
    """
    parser = argparse.ArgumentParser(
        description=f"DFOILIATOR: This ia a pipeline for DFOIL (https://github.com/jbpease/dfoil).\n \
                      It requires sequence data in *fas or *.vcf format and a \
                      a tsv file containing the tests to be performed by DFOIL."
    )

    # Define command-line arguments
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input file name in FASTA or VCF format",
        required=True,
    )
    parser.add_argument(
        "-t", "--test", type=str, help="Test file name in TSV format", required=True
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # You should use the built-in -h or --help argument to display help instructions
    if args.input:
        # If -i and -t are provided, print the names of the imported files
        print(f"Input file: {args.input}")
        # checking file type for inputfile
        #         if args.input.split(".")[-1] == "vcf":
        if args.input.endswith(".vcf"):
            print("Input file is a VCF file.")
            fasta_file_name = vcf2fasta(args.input)
        elif args.input.endswith(".vcf.gz"):
            print("Input file is a compressed VCF file.")
            fasta_file_name = vcf2fasta(args.input)
        elif (
            args.input.endswith(".fas")
            or input.endswith(".fasta")
            or input.endswith(".fa")
        ):
            print("Input file is a FASTA file.")
            fasta_file_name = args.input
        else:
            print("Input file is not a VCF or FASTA file.")
            exit(1)

    else:
        print(
            "Please provide input file in fasta, vcf, or vcf.gz format. Use -h or --help for help instructions."
        )

    if args.test:
        print(f"Tests table file: {args.test}")
        # checking file type for testfile
        tests_dataframe = read_tsv_file(args.test)
        global tests_filename_prefix  # making it global to use at the end to save results
        tests_filename_prefix = args.test.split(".")[0]
    else:
        print(
            "Please provide tests table file. Use -h or --help for help instructions."
        )

    return fasta_file_name, tests_dataframe


def vcf2fasta(input_file: str) -> str:
    """
    This function converts a VCF file to a FASTA file.
    It requires that vcf-to-tab is installed (bcftools package).
    """
    prefix = input_file.split(".")[0]
    output_file = prefix + ".fas"
    tab_file = prefix + ".tab"
    if input_file.endswith(".vcf"):
        command = f"cat {input_file} | vcf-to-tab --iupac > {tab_file}"
    else:
        command = f"zcat {input_file} | vcf-to-tab --iupac > {tab_file}"

    try:
        print(f"  Converting {input_file} to {tab_file} via vcf-to-tab ...")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(
            "Error running the command. Please make sure the necessary tools are installed and the input file exists."
        )

    # converting tab to fasta
    print(f"  Converting {tab_file} to {output_file} ...")
    fasta = {}
    current_keys = []

    with open(tab_file, "r") as file:
        for line in file:
            if line.startswith("#"):
                # Parse the header line to determine the keys
                elements = line.strip().split("\t")
                current_keys = elements[3:]
                for key in current_keys:
                    fasta[key] = ""
            else:
                elements = line.strip().split("\t")
                for i, key in enumerate(current_keys):
                    if elements[i + 3] == ".":
                        # Replace '.' with 'N'
                        fasta[key] += "N"
                    else:
                        fasta[key] += elements[i + 3]

    # Write the sequences to a FASTA file
    with open(output_file, "w") as fasta_file:
        for key, sequence in fasta.items():
            fasta_file.write(">" + key + "\n" + sequence + "\n")

    return output_file


def read_tsv_file(file_path: str) -> pd.DataFrame:
    """
    This function reads a TSV file into a pandas data frame.
    The *.tsv file had to have the following columns: "test_name", "p1", "p2", "p3", "p4", "out", "dfoil_mode"
    """
    # Read the TSV file into a pandas data frame
    df = pd.read_csv(file_path, sep="\t")

    # Check that the data frame has 7 columns
    if len(df.columns) != 7:
        raise ValueError("The input file does not have 7 columns.")

    # Check that the column names are correct
    expected_columns = ["test_name", "p1", "p2", "p3", "p4", "out", "dfoil_mode"]
    if not all(col in df.columns for col in expected_columns):
        raise ValueError("The input file does not have the expected column names.")

    # Check that all cells are non-empty
    if df.isnull().values.any():
        raise ValueError("The input file contains empty cells.")

    # Return the data frame
    return df


def fasta4test(fasta_file_name: str, test_name: str, list_of_taxa: str) -> str:
    """
    This function creates a FASTA file with the sequences for the specified taxa.
    The resulting string is a file named "<tests_filename_prefix>_<test_name>.fas".
    The order in the fasta file is: "p1", "p2", "p3", and "p4"
    """
    # selected_fasta = "selected_taxa_" + test_name + ".fas"
    selected_fasta = f"{tests_filename_prefix}_{test_name}.fas"
    # Create a dictionary to store selected sequences
    selected_sequences = {}

    # Iterate through the input FASTA file and select sequences for the specified taxa
    for record in SeqIO.parse(fasta_file_name, "fasta"):
        taxon = record.id
        if taxon in list_of_taxa:
            selected_sequences[taxon] = record

    # Write the selected sequences in the order specified by -t to the output FASTA file
    with open(selected_fasta, "w") as output_handle:
        for taxon in list_of_taxa:
            if taxon in selected_sequences:
                # Convert the sequence to a single line
                selected_sequence = selected_sequences[taxon]
                selected_sequence.seq = selected_sequence.seq.replace("-", "")
                # selected_sequence.seq = selected_sequence.seq.ungap('-')  # Remove gaps
                SeqIO.write(selected_sequence, output_handle, "fasta")

    print(f"  Extracted {len(selected_sequences)} sequences to {selected_fasta}")

    return selected_fasta


def run_fasta2dfoil(taxa_list: str, selected_fasta: str, test: str):
    """
    This function runs fasta2dfoil to count patterns of allele distribution.
    fasta2dfoil.py is a script that comes with DFOIL.
    """
    taxa = ",".join(taxa_list)
    output_file = selected_fasta[:-4] + "_counts.txt"
    command = f"./fasta2dfoil.py {selected_fasta} -o {output_file} --name {taxa}"

    # Running fasta2dfoil
    try:
        print(f"  Counting patters of allele distribution for test: {test}.\n")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(
            "Error running fastaedfoil. Please make sure it is installed and the input file exists."
        )

    return output_file


def run_dfoil(dfoil_mode: str, dfoil_patterns_file: str) -> str:
    """
    This function runs dfoil to test for introgression.
    dfoil.py is a script that comes with DFOIL.
    The function returns the name of the output file.
    """

    dfoil_outfile = dfoil_patterns_file[:-10] + "dfoil.out"

    # Running dfoil

    command = f"./dfoil.py --mode {dfoil_mode} --infile {dfoil_patterns_file} --out {dfoil_outfile}"

    try:
        print(
            f"Running: ./dfoil.py --mode {dfoil_mode} --infile {dfoil_patterns_file} --out {dfoil_outfile}"
        )
        subprocess.run(command, shell=True, check=True)

    except subprocess.CalledProcessError:
        print(
            "Error running dfoil. Please make sure it is installed and the input file exists."
        )
    return dfoil_outfile


def run_dfoil_analyze(dfoil_outfile: str) -> str:
    """
    This function runs dfoil_analyze to summarize the results of dfoil.
    dfoil_analyze.py is a script that comes with DFOIL.
    The function returns the name of the output file.
    """

    dfoil_analyze_outfile = dfoil_outfile[:-10] + "_stats.txt"
    command = f"./dfoil_analyze.py {dfoil_outfile} > {dfoil_analyze_outfile}"
    try:
        print(f"  Analyzing Dfoil results in {dfoil_outfile}.\n")
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(
            "Error running dfoil_analyze. Please make sure it is installed and the input file exists."
        )
    return dfoil_analyze_outfile


#
## Second set of funcion to summarize results
#

# DFOIL signatures for DFO/DIL/DFI/DOL and correstpoding
# event based on Table 1 of Pease and Hahn (2015:DOI:10.1093/sysbio/syv023)

dfoil_signatures4introgression = {
    "+++0": "P1 ⇒ P3",
    "+0++": "P3 ⇒ P1",
    "--0+": "P1 ⇒ P4",
    "-0++": "P4 ⇒ P1",
    "++-0": "P2 ⇒ P3",
    "0+--": "P3 ⇒ P2",
    "--0-": "P2 ⇒ P4",
    "0---": "P4 ⇒ P2",
    "++00": "P12 ⇔ P3",
    "--00": "P12 ⇔ P4",
    "--++": "P12 ⇔ P4",  # this is not in the Table one, but was in the output of dfoil
    "0000": "No Introgression",
    "00++": "No Introgression",
    "00--": "No Introgression",
    "****": "NA",
}


def parse_results(stats_file: str) -> pd.DataFrame:
    """
    This function parses the results of dfoil_analyze into a pandas data frame.
    """

    data = []  # Initialize a list to store the data
    current_stat = None

    with open(stats_file, "r") as file:
        for line in file:
            if line.startswith("stat"):
                current_stat = line.strip().split("\t")
            elif current_stat:
                data_line = line.strip().split("\t")
                if len(data_line) == len(current_stat):
                    data.append(data_line)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=current_stat)

    # Filter the DataFrame to include only the desired columns
    columns_to_include = [
        "stat",
        "min",
        "mean",
        "max",
        "5%ile",
        "25%ile",
        "50%ile",
        "75%ile",
        "95%ile",
    ]
    results_df = df[columns_to_include]

    return results_df


def get_raw_metrics(data_frame: pd.DataFrame) -> dict:
    """
    This function extracts the raw values for D stats and p-values from the data frame \
        compiled in the previous function from dfoil_analyze run.
    The function retuns a dictionary using as keys "DFO", "DIL", "DFI", and "DOL" for which\
        D stats and p-values are assigned as values.
    """

    raw_metrics = {}

    # DFO mean and pvalue
    try:
        dfo_value = float(data_frame.iat[0, 2])
    except ValueError:
        dfo_value = data_frame.iat[0, 2]
    try:
        dfo_pvalue = float(data_frame.iat[2, 2])
    except ValueError:
        dfo_pvalue = data_frame.iat[2, 2]

    # DIL mean and pvalue
    try:
        dil_value = float(data_frame.iat[3, 2])
    except ValueError:
        dil_value = data_frame.iat[3, 2]
    try:
        dil_pvalue = float(data_frame.iat[5, 2])
    except ValueError:
        dil_pvalue = data_frame.iat[5, 2]

    # DFI mean and pvalue
    try:
        dfi_value = float(data_frame.iat[6, 2])
    except ValueError:
        dfi_value = data_frame.iat[6, 2]
    try:
        dfi_pvalue = float(data_frame.iat[8, 2])
    except ValueError:
        dfi_pvalue = data_frame.iat[8, 2]

    # DOL mean and pvalue
    try:
        dol_value = float(data_frame.iat[9, 2])
    except ValueError:
        dol_value = data_frame.iat[9, 2]
    try:
        dol_pvalue = float(data_frame.iat[11, 2])
    except ValueError:
        dol_pvalue = data_frame.iat[11, 2]

    raw_metrics = {
        "DFO": [dfo_value, dfo_pvalue],
        "DIL": [dil_value, dil_pvalue],
        "DFI": [dfi_value, dfi_pvalue],
        "DOL": [dol_value, dol_pvalue],
    }
    # print(raw_metrics)

    return raw_metrics


def get_sample_dfoil_signature(raw_metrics: dict, alpha: float) -> str:
    """
    This function receives a dictionay from get_raw_metrics() and assigns \
        the introgression signature based on Table 1 of Pease and Hahn (2015:DOI:10.1093/sysbio/syv023).    
    """
    sample_dfoil_signature = ""
    for key, value in raw_metrics.items():
        if value[1] == "na":
            sample_dfoil_signature += "*"
        else:
            if value[1] > alpha:
                sample_dfoil_signature += "0"

            if value[1] <= alpha and value[0] > 0:
                sample_dfoil_signature += "+"

            if value[1] <= alpha and value[0] < 0:
                sample_dfoil_signature += "-"

    return sample_dfoil_signature


def sumarize_results(stats_file: str, alpha: float = 0.05) -> (str, str):
    """
    This function summarizes the results of dfoil_analyze.
    It receives the name of the stats file output from dfoil_analyze.
    Run a seried of functions associated with results summarization.
    It returns two strings, the key and the value of dfoil_signatures4introgression dictionary
    """

    input_stats_file = stats_file

    # Read the results file into a pandas data frame
    results_df = parse_results(input_stats_file)

    # Extract raw values for D stats and p-values
    raw_metrics = get_raw_metrics(results_df)

    # Get sample pattern signature
    sample_dfoil_signature = get_sample_dfoil_signature(raw_metrics, alpha)

    # Detection of introgression
    if "*" in sample_dfoil_signature:
        pattern_detected = "NA"
    else:
        pattern_detected = "Unrecognized pattern for DFO/DIL/DFI/DOL"
        for signature, pattern in dfoil_signatures4introgression.items():
            if sample_dfoil_signature == signature:
                # print(f"Introgression detected: {pattern}")
                pattern_detected = pattern
                break
    # print(f"Pattern detected: {pattern_detected}")

    # to print as a table
    mod_sample_dfoil_signature = " ".join(sample_dfoil_signature)

    return mod_sample_dfoil_signature, pattern_detected


def save_to_directory(dir_name: str) -> None:
    """
    This function saves the results in a directory named after the test file.
    If the directory already exists, it adds a number to the end of the directory name.
    """

    counter = 0
    while True:
        if counter == 0:
            new_dir_name = dir_name
        else:
            new_dir_name = f"{dir_name}_{counter}"
        if not os.path.exists(new_dir_name):
            os.makedirs(new_dir_name)
            break
        counter += 1

    for file_name in os.listdir("./"):
        # print(file_name)
        if file_name.startswith(tests_filename_prefix) and os.path.isfile(file_name):
            #    os.rename(file_name, os.path.join(new_dir_name, file_name))
            os.rename(
                file_name, os.path.join(new_dir_name, os.path.basename(file_name))
            )


#
## Main function
#


def main():
    fasta_file_name, tests_dataframe = processing_input_files()
    print(f"  Processing {fasta_file_name} ...")
    print(f"  Performing the following testes:\n")

    # Extract the test names
    test_names = tests_dataframe["test_name"].tolist()

    # Extract the taxa to test
    taxa_to_test = tests_dataframe[["p1", "p2", "p3", "p4", "out"]].values.tolist()

    # Extract the variable names
    dfoil_mode = tests_dataframe["dfoil_mode"].tolist()

    # Running Dfoil
    signatures = []
    introgression = []
    for idx, test_name in enumerate(test_names):
        # Making FASTA files for each test
        selected_fasta_file = fasta4test(fasta_file_name, test_name, taxa_to_test[idx])
        dfoil_patterns_file = run_fasta2dfoil(
            taxa_to_test[idx], selected_fasta_file, test_name
        )
        dfoil_outfile_file = run_dfoil(dfoil_mode[idx], dfoil_patterns_file)
        dfoil_analyze_outfile = run_dfoil_analyze(dfoil_outfile_file)

        print(f"  Results of the analysis in: {dfoil_analyze_outfile}")

        # Summarizing results
        mod_sample_dfoil_signature, pattern_detected = sumarize_results(
            dfoil_analyze_outfile
        )
        signatures.append(mod_sample_dfoil_signature)
        introgression.append(pattern_detected)

    # Creating dataframe with results
    dfoil_results_df = pd.DataFrame(columns=["signature", "introgression"])
    dfoil_results_df["signature"] = signatures
    dfoil_results_df["introgression"] = introgression

    summary_results_dataframe = pd.concat([tests_dataframe, dfoil_results_df], axis=1)
    print()
    print("* ----------------------------------------------------------------- *")
    print()
    print("Summary of results:")
    print(summary_results_dataframe)

    # Saving summary results in tsv file
    outfile = f"{tests_filename_prefix}_summary_results.tsv"
    print()
    print(f"Resulting dataframe saved in {outfile}")

    summary_results_dataframe.to_csv(outfile, sep="\t", index=False)

    save_to_directory(tests_filename_prefix)


if __name__ == "__main__":
    main()
