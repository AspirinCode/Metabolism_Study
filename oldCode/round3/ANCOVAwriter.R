#Writes to an Excel File the paired T-test data for both Plasma and TGRL
library(readxl)
library("xlsx")
source("ANCOVA.R")

TGRL <- ANCOVA("TGRL Combined Lipid Results ")
Plasma <- ANCOVA("Plasma Combined Lipid Results ")

write.xlsx2(Plasma, file="ANCOVA.xlsx", 
           sheetName="Plasma",col.names=FALSE, row.names=FALSE, append=FALSE)
write.xlsx2(TGRL, file="ANCOVA.xlsx", 
           sheetName="TGRL",col.names=FALSE, row.names=FALSE, append=TRUE)
