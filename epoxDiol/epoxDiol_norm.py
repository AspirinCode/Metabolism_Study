import pandas as pd
import numpy as np
import scipy.stats as stats

data_raw=pd.read_csv('../MetData/transposedDN.csv')
parentFA=['AA', 'LA', 'DHA', 'aLA', 'EPA']
donors=[u'D229', u'D360',u'D384', u'D391', u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
types=['5_15', '17_18', '19_20', '15_16', '16_17', '9_10', '5_6', '12_13', '11_12', '14_15', '8_9']

VCAM=data_raw.loc[1]

tofa=data_raw[data_raw['Oxylipin'].str.contains('To')]
Ftofa=tofa[tofa['Oxylipin'].str.contains('-F')]
PPtofa=tofa[tofa['Oxylipin'].str.contains('-PP')]

nefa=data_raw[data_raw['Oxylipin'].str.contains('NE')]
Fnefa=nefa[nefa['Oxylipin'].str.contains('-F')]
PPnefa=nefa[nefa['Oxylipin'].str.contains('-PP')]


dataHead=['Donor','Parent Fatty Acid','type','To-PP','To-F','NE-PP','NE-F']
data=[]

for pfa in parentFA:
    for tp in types:
        pto=[]
        fto=[]
        pne=[]
        fne=[]

        dataType=data_raw[(data_raw['Type']==tp) & (data_raw['Parent FA']==pfa)]
        tofa=dataType[dataType['Oxylipin'].str.contains('To')]
        Ftofa=tofa[tofa['Oxylipin'].str.contains('-F')]
        PPtofa=tofa[tofa['Oxylipin'].str.contains('-PP')]

        EPPtofa=PPtofa[PPtofa['Class']=='Epoxides']
        DPPtofa=PPtofa[PPtofa['Class']=='Diols']
        EFtofa=Ftofa[Ftofa['Class']=='Epoxides']
        DFtofa=Ftofa[Ftofa['Class']=='Diols']
        if not (EPPtofa.empty or DPPtofa.empty):
            Evals=EPPtofa[donors].values.astype(np.float)
            Dvals=DPPtofa[donors].values.astype(np.float)
            pto=Evals-Dvals
            pto=pto.tolist()[0]
        if not (EFtofa.empty or DFtofa.empty):
            Evals=EFtofa[donors].values.astype(np.float)
            Dvals=DFtofa[donors].values.astype(np.float)
            fto=Evals-Dvals
            fto=fto.tolist()[0]

        nefa=dataType[dataType['Oxylipin'].str.contains('NE')]
        Fnefa=nefa[nefa['Oxylipin'].str.contains('-F')]
        PPnefa=nefa[nefa['Oxylipin'].str.contains('-PP')]
        
        EFnefa=Fnefa[Fnefa['Class']=='Epoxides']
        DFnefa=Fnefa[Fnefa['Class']=='Diols']
        EPPnefa=PPnefa[PPnefa['Class']=='Epoxides']
        DPPnefa=PPnefa[PPnefa['Class']=='Diols']
        if not (EPPnefa.empty or DPPnefa.empty):
            Evals=EPPnefa[donors].values.astype(np.float)
            Dvals=DPPnefa[donors].values.astype(np.float)
            pne=Evals-Dvals
            pne=pne.tolist()[0]
        if not (EFnefa.empty or DFnefa.empty):
            Evals=EFnefa[donors].values.astype(np.float)
            Dvals=DFnefa[donors].values.astype(np.float)
            fne=Evals-Dvals
            fne=fne.tolist()[0]
        for i,don in enumerate(donors):
            tpto=0
            tfto=0
            tpne=0
            tfne=0
            if pto:
                tpto=pto[i]
            if fto:
                tfto=fto[i]
            if pne:
                tpne=pne[i]
            if fne:
                tfne=fne[i]
            if (pto or fto or pne or fne):
                data.append([don,pfa,tp,tpto,tfto,tpne,tfne])




dataDF=pd.DataFrame(data,columns=dataHead)


