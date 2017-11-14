import pandas as pd
import numpy as np
import scipy.stats as stats

data_raw=pd.read_csv('../MetData/Epoxides_Diols_1.csv')
parentFA=['AA', 'LA', 'DHA', 'aLA', 'EPA']
donors=[u'D229', u'D360',u'D384', u'D391', u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
VCAM=data_raw.loc[0]
tofa=data_raw[data_raw['Oxylipin'].str.contains('To')]
Ftofa=tofa[tofa['Oxylipin'].str.contains('-F')]
PPtofa=tofa[tofa['Oxylipin'].str.contains('-PP')]

nefa=data_raw[data_raw['Oxylipin'].str.contains('NE')]
Fnefa=nefa[nefa['Oxylipin'].str.contains('-F')]
PPnefa=nefa[nefa['Oxylipin'].str.contains('-PP')]


dataHead=['Donor','Parent Fatty Acid','Epoxide To-PP sum','Epoxide To-F sum','Epoxide NE-PP sum','Epoxide NE-F sum','Diol To-PP sum','Diol To-F sum','Diol NE-PP sum','Diol NE-F sum']

data=[]

EtempFtofa=Ftofa[(Ftofa['Class']=='Epoxides')]
EtempFnefa=Fnefa[(Fnefa['Class']=='Epoxides')]
EtempPPtofa=PPtofa[(PPtofa['Class']=='Epoxides')]
EtempPPnefa=PPnefa[(PPnefa['Class']=='Epoxides')]

DtempFtofa=Ftofa[(Ftofa['Class']=='Diols')]
DtempFnefa=Fnefa[(Fnefa['Class']=='Diols')]
DtempPPtofa=PPtofa[(PPtofa['Class']=='Diols')]
DtempPPnefa=PPnefa[(PPnefa['Class']=='Diols')]
pfa='All'
for donor in donors:

    #TOFA ratio
    EfTo=EtempFtofa[donor].sum()
    EpTo=EtempPPtofa[donor].sum()
    DfTo=DtempFtofa[donor].sum()
    DpTo=DtempPPtofa[donor].sum()

    #NEFA ratio
    Efne=EtempFnefa[donor].sum()
    Epne=EtempPPnefa[donor].sum()
    Dfne=DtempFnefa[donor].sum()
    Dpne=DtempPPnefa[donor].sum()
        
    data.append([donor,pfa,EpTo,EfTo,Epne,Efne,DpTo,DfTo,Dpne,Dfne,])


for pfa in parentFA:
    EtempFtofa=Ftofa[(Ftofa['Parent FA']==pfa) & (Ftofa['Class']=='Epoxides')]
    EtempFnefa=Fnefa[(Fnefa['Parent FA']==pfa) & (Fnefa['Class']=='Epoxides')]
    EtempPPtofa=PPtofa[(PPtofa['Parent FA']==pfa) & (PPtofa['Class']=='Epoxides')]
    EtempPPnefa=PPnefa[(PPnefa['Parent FA']==pfa) & (PPnefa['Class']=='Epoxides')]

    DtempFtofa=Ftofa[(Ftofa['Parent FA']==pfa) & (Ftofa['Class']=='Diols')]
    DtempFnefa=Fnefa[(Fnefa['Parent FA']==pfa) & (Fnefa['Class']=='Diols')]
    DtempPPtofa=PPtofa[(PPtofa['Parent FA']==pfa) & (PPtofa['Class']=='Diols')]
    DtempPPnefa=PPnefa[(PPnefa['Parent FA']==pfa) & (PPnefa['Class']=='Diols')]
    print pfa
    for donor in donors:

        #TOFA ratio
        EfTo=EtempFtofa[donor].sum()
        EpTo=EtempPPtofa[donor].sum()
        DfTo=DtempFtofa[donor].sum()
        DpTo=DtempPPtofa[donor].sum()

        #NEFA ratio
        Efne=EtempFnefa[donor].sum()
        Epne=EtempPPnefa[donor].sum()
        Dfne=DtempFnefa[donor].sum()
        Dpne=DtempPPnefa[donor].sum()
            
        data.append([donor,pfa,EpTo,EfTo,Epne,Efne,DpTo,DfTo,Dpne,Dfne,])


dataDF=pd.DataFrame(data,columns=dataHead)
dataDF.to_csv('../results/epoxDiol_2.csv',index=False)
