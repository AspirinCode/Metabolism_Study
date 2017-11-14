#Writes to an Excel File the paired T-test data for both Plasma and TGRL
library(readxl)
library("xlsx")
library(broom)
library(tibble)
source("ANCOVA_no_interaction.R")

TGRL <- ANCOVA_NI("TGRL Combined Lipid Results ")
Plasma <- ANCOVA_NI("Plasma Combined Lipid Results ")

write.xlsx2(Plasma, file="ANCOVA_no_interaction.xlsx", 
            sheetName="Plasma",col.names=FALSE, row.names=FALSE, append=FALSE)
write.xlsx2(TGRL, file="ANCOVA_no_interaction.xlsx", 
            sheetName="TGRL",col.names=FALSE, row.names=FALSE, append=TRUE)
