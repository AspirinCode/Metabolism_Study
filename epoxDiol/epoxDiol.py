import pandas as pd
import numpy as np
import scipy.stats as stats

data_raw=pd.read_csv('../MetData/Epoxides_Diols.csv')
parentFA=['AA', 'LA', 'DHA', 'aLA', 'EPA']
donors=[u'D229', u'D360',u'D384', u'D391', u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
VCAM=data_raw.loc[0]
tofa=data_raw[data_raw['Oxylipin'].str.contains('To')]
Ftofa=tofa[tofa['Oxylipin'].str.contains('-F')]
PPtofa=tofa[tofa['Oxylipin'].str.contains('-PP')]

nefa=data_raw[data_raw['Oxylipin'].str.contains('NE')]
Fnefa=nefa[nefa['Oxylipin'].str.contains('-F')]
PPnefa=nefa[nefa['Oxylipin'].str.contains('-PP')]


dataHead=['Donor','Parent Fatty Acid','ToRatio','NERatio','VCAM']
data=[]

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

        logVCAM=np.log(VCAM[donor])
        #TOFA ratio
        EfTo=EtempFtofa[donor].sum()
        EpTo=EtempPPtofa[donor].sum()
        DfTo=DtempFtofa[donor].sum()
        DpTo=DtempPPtofa[donor].sum()

        if EpTo:
            ETo=float(EpTo)/float(EfTo)
        else:
            ETo=0.0

        if DpTo:
            DTo=float(DpTo)/float(DfTo)
        else:
            DTo=0.0
        try:
            ToRatio=np.log(ETo/DTo)
        except ZeroDivisionError:
            ToRatio='NaN'

        #NEFA ratio
        Efne=EtempFtofa[donor].sum()
        Epne=EtempPPtofa[donor].sum()
        Dfne=DtempFtofa[donor].sum()
        Dpne=DtempPPtofa[donor].sum()

        if Epne:
            Ene=float(Epne)/float(Efne)
        else:
            Ene=0.0

        if Dpne:
            Dne=float(Dpne)/float(Dfne)
        else:
            Dne=0.0
        try:
            neRatio=np.log(Ene/Dne)
        except ZeroDivisionError:
            neRatio='NaN'

            
        #Natural log ratios appended
        data.append([donor,pfa,ToRatio,neRatio,VCAM[donor]])
    

        print 'To: ',ToRatio,' NE: ', neRatio

dataDF=pd.DataFrame(data,columns=dataHead)
resultsHead=['Parent Fatty Acid','To P-value','NE P-Value','To r^2','NE r^2','To Pearsons','NE Perasons']
results=[]
for pfa in parentFA[1:]:
    faDF=dataDF[(dataDF['Parent Fatty Acid']==pfa) & (dataDF['ToRatio']!='NaN')]
    slope, intercept, to_r_value, to_p_value, std_err = stats.linregress(faDF['ToRatio'],faDF['VCAM'])
    to_pearson,p=stats.pearsonr(faDF['ToRatio'],faDF['VCAM'])
    slope, intercept, ne_r_value, ne_p_value, std_err = stats.linregress(faDF['NERatio'],faDF['VCAM'])
    ne_pearson,p=stats.pearsonr(faDF['NERatio'],faDF['VCAM'])
    results.append([pfa,to_p_value,ne_p_value,to_r_value**2,ne_r_value**2,to_pearson,ne_pearson])

resultsDF=pd.DataFrame(results,columns=resultsHead)
resultsDF.to_csv('../results/epoxDiol.csv',index=False)
