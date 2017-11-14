PairedT <- function(Sheet)
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
  
  final<-c('Name','Pro Vs Anti P-Value','Pro vs Anti Average','Pro Average','Pro Std','Anti Average','Anti std','Number of Missing Values') # creating a vector with heading name and P value 
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
            Post = TData[,Post]
            
            Fa=as.numeric(Fasting[2:11])
            P=as.numeric(Post[2:11])
            std = sd(P-Fa)
            
            FastingAnti = as.numeric(Fasting[2:6])
            FastingPro = as.numeric(Fasting[7:11])
            PostAnti = as.numeric(Post[2:6])
            PostPro = as.numeric(Post[7:11])
            
            normAnti = (PostAnti-FastingAnti)/FastingAnti
            normPro = (PostPro-FastingPro)/FastingPro
            
            AntiAvg = mean(normAnti,na.rm = TRUE)
            AntiStd = sd(normAnti,na.rm = TRUE)
            ProAvg = mean(normPro,na.rm = TRUE)
            ProStd = sd(normPro,na.rm = TRUE)
            
            naCount= length(which(is.na(Fa))) + length(which(is.na(P))) #Finds number of missing values
            
            TotTest = t.test(Fa,P,paired=TRUE) #Original paired T-test
            PvATest = t.test(normPro,normAnti) #compare anti vs pro normalized in unpaired t-test
            
            
            results <- c(sub, PvATest$p.value, diff(PvATest$estimate), ProAvg, ProStd, AntiAvg, AntiStd,naCount)
            final=rbind(final,results)
            
          }
        }
      }
    }
    
  }
  return(final)
}