library(broom)
library(tidyr)
library(dplyr)

data_raw   <-read.csv("~/Desktop/Metabolism_Study/MetData/data_normalized_TGRL.csv",header=FALSE,sep=',')

#Removes first few rows of csv file (the headers)
data_raw=data_raw[-1,]
data_raw=data_raw[-1,]
data_raw=data_raw[-1,]
data_raw=data_raw[-1,]

#Used to classify as pro or anti, anti =1 pro =2
phenotype<-c(1,1,1,1,1,2,2,2,2,2)

#columns with fasting and PP
Fcols<-c(2,3,4,5,6,12,13,14,15,16)
Pcols<-c(7,8,9,10,11,17,18,19,20,21)

#Variable to hold full table initialized with headers
final<-c('Name','fa','grp')

#Goes through each metabolite and does ancova
for(i in 1:nrow(data_raw))
{
  metab<-t(data_raw[i,]) # Select data from 1 metabolite
  metName<-metab[1] # Gets name of metabolite
  
  #Format fasting and PP data
  Fa<-as.numeric(metab[Fcols]) 
  P<-as.numeric(metab[Pcols])
  
  #Performs and formats the ancova
  test <- aov(P~Fa+phenotype)
  test <- tidy(test)

  #Attatches result to final table
  results <- c(metName, test$p.value[1],test$p.value[2]) 
  final=rbind(final,results)
}

#Writes table to a csv file
write.table(final,file="ancovaNormTGRL.csv",sep=',',row.names = F,
            col.names = F)