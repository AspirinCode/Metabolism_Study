# Passerini Lab Metablism Study Data Analysis Scripts

This folder contains an aggregation of scripts used to incrementally analyze data from a metabolimics study consisting of 10 donors.

## Folder Descriptions

MetData: Original Metabolism data


OxylipinSorting: (Python) Scripts used in sorting oxylipins based on their name. Sorting gave information about Parent Fatty Acid and Class

PairedT: (R) Scripts to conduct a paired T-test on metabolomics data of each metabolites abundance before and after meal.

TotalOxylipin: (Python) Scripts to sort through all oxylipins, classify by PFA, Tofa/NEFA classification, PP/F, and conducted paired t-tests on the sums of each subset of data.

epoxDiol: (Python) Scripts to determine ratio of epoxides to diols for specific classifications of metabolites

johnsonNorm: (Python) Scripts to pair PP and F data for each metabolite and find the difference and ratio of PP to F for the Johnson Normalize Data set.

mixedAnova: (Python) Code to attempt a mixed Anova on the data_normalized_TGRL.csv data

normTGRL: (R) Runs an ANCOVA test on PP vs F and Pro vs Anti data from data_normalized_TGRL.csv data

oldCode: (R) Preliminary attempts at pairing Fasting and PP data and running Anova tests

orgOxy: (Python) Reorganizes original metabolism data with columns for Donor,Pro/Anti,To/NE,F/PP, and each metabolite measured. Used for JMP analysis.

results: General directory for results of scripts above.
