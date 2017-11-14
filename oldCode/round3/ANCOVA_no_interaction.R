
ANCOVA_NI <- function(Sheet)
{
  
  MData   <- read_excel("~/Desktop/Metabolism_Study/Passerini TGRL-Plasma Final Res.xlsx", sheet = Sheet, col_names = FALSE)
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
  
  final<-c('Name','fastingtoPP-pval','Pro vs Anti-pvalue','Grpandfasting-Pval','Pro-PP Mean','Pro-PP Std','Anti-PP Mean','Anti-PP Std') # creating a vector with heading name and P value 
  for(val in names) #Go through each Fasting value
  {
    L <- nchar(val)
    sub <- substr(val,1,L-2)
    matchInd <- grep(sub,smallT,perl=FALSE,value=FALSE, fixed=TRUE)
    
    if(length(matchInd) > 1)
    {
      for (ind in matchInd)
      {
        name <- as.character(smallT[ind])
        isPP <- grep(name,PP2[1,],fixed=TRUE) #Verify match is PP
        if((as.character(name) != "%-C22:6n3-NEFA-PP") & (length(isPP) != 0))
        {
          nl<-length(grep("%",name,fixed=TRUE)) #Check name for percent sign
          vl<-length(grep("%",val,fixed=TRUE)) # Check val for percent sign
          Lm <- nchar(name) #Name Length of match
          if (Lm <= (L+1) & Lm>=(L-1) & L != Lm & vl==nl)
          {
            regN = sprintf("^%s$",name)
            regV = sprintf("^%s$",val)
            Fasting = which(smallT==val)
            Post = which(smallT==name)
            Fasting = TData[,Fasting]
            Fasting = as_data_frame(Fasting)
            Fa = list()
            for(x in Fasting)
            {
              Fa = rbind(Fa,x)
            }
            
            Post = TData[,Post]
            Post= as_data_frame(Post)
            P = list()
            for(y in Post)
            {
              P = rbind(P,y)
            }
            
            Fa=as.numeric(Fa[2:11])
            P=as.numeric(P[2:11])
            AntiP = P[1:5]
            AntiP.avg = mean(AntiP)
            AntiP.std = sd(AntiP)
            ProP = P[6:10]
            ProP.avg = mean(ProP)
            ProP.std = sd(ProP)
            std = sd(P-Fa)
            
            grp= c(1,1,1,1,1,2,2,2,2,2)
            
            naCount= length(which(is.na(Fa))) + length(which(is.na(P))) #Finds number of missing values
            
            test1 <- aov(P ~ Fa+grp)
            test <- tidy(test1)
            
            results <- c(sub, test$p.value[1],test$p.value[2],test$p.value[3],ProP.avg,ProP.std,AntiP.avg,AntiP.std) 
            final=rbind(final,results)
            
          }
        }
      }
    }
    
  }
  return(final)
}
