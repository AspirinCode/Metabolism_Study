#Performs Paired T-test on a given sheet from metabolism study, returns table of values
PairedT2 <- function(Sheet)
{
  
  library(readxl)
  MData   <- read_excel("C:/Users/anita/Desktop/FinalResults.xlsx", 1, col_names = FALSE)
  cols    <- min(which(is.na(MData[4,]))) - 1
# load data. Readxlxs crashes when you try to load big files. So use read_excel instead. 
# cols- total number of columns 
  TData   <- MData[4:14,1:cols]
  smallT  <- TData[1,] # headers only
  PP1     <- grep('PP',smallT,perl=TRUE) # find all the PP headers 
  PP2     <- TData[,PP1] # Indexing the entire table for PP value 
  F1      <- grep('-F',smallT,perl=TRUE) #same thing for fasting 
  F2      <- TData[,F1]
  names <- F2[1,] # headers for fasting
  final<-c('Name','P-Value') # creating a vector with heading name and P value 
  
  for(val in names) # val changes to different fasting headers in the names vector 
  {
    L <- nchar(val) #length of val -one of the headers
    print(val)
    sub <- substr(val,1,L-2) #remove the -F 
    regS <- sprintf("%s",sub) #print it as a string 
    print(regS)
    match <- grep(regS,smallT,perl=TRUE,value=FALSE) # group the matching PP header and return indeces 
    print(match)
   
    if(length(match) > 1) #if there is a match 
    {
      
            VectorA = TData[,match[1]]
            VectorB = TData[,match[2]]
            test = t.test(as.numeric(VectorA[2:11]),as.numeric(VectorB[2:11]),paired=TRUE)
            print(test)
            final=rbind(final,c(sub,as.numeric(test$p.value)))
        
    }
    
  }
  return(final)
}

