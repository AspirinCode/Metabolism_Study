#Writes to an Excel File the paired T-test data for both Plasma and TGRL
library(readxl)
library("xlsx")
source("PairedT.R")

TGRL <- PairedT("TGRL Combined Lipid Results ")
Plasma <- PairedT("Plasma Combined Lipid Results ")

write.xlsx2(Plasma, file="Pro-v-Anti_SA.xlsx", 
           sheetName="Plasma",col.names=FALSE, row.names=FALSE, append=FALSE)
write.xlsx2(TGRL, file="Pro-v-Anti_SA.xlsx", 
           sheetName="TGRL",col.names=FALSE, row.names=FALSE, append=TRUE)
