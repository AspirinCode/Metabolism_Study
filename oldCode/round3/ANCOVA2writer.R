#Writes to an Excel File the paired T-test data for both Plasma and TGRL
library(readxl)
library("xlsx")
library(broom)
library(tidyr)
library(dplyr)
source("ANCOVA2.R")

TGRL <- ANCOVA2("TGRL Combined Lipid Results ")
Plasma <- ANCOVA2("Plasma Combined Lipid Results ")

write.xlsx2(Plasma, file="ANCOVA2.xlsx", 
            sheetName="Plasma",col.names=FALSE, row.names=FALSE, append=FALSE)
write.xlsx2(TGRL, file="ANCOVA2.xlsx", 
            sheetName="TGRL",col.names=FALSE, row.names=FALSE, append=TRUE)
