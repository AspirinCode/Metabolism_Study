import numpy as np
import pandas as pd

data=pd.read_csv('Input/sortedOxylipins_TGRL.csv')

NEPP=data.loc[data.Oxylipin.str.contains('-NE-PP')]
NEF=data.loc[data.Oxylipin.str.contains('-NE-F')]
ToPP=data.loc[data.Oxylipin.str.contains('-To-PP')]
ToF=data.loc[data.Oxylipin.str.contains('-To-F')]

if not len(NEPP)+len(NEF)+len(ToPP)+len(ToF) == len(data):
    print 'Sorting Error: Not all oxylipins correctly sorted' 

enzymes=['COX', 'LOX', 'CYP ', 'auto ', 'SEH']
pfas=['AA', 'aLA', 'EPA', 'DHA', 'LA']
donors=['D229', 'D360', 'D384', 'D391', 'D75', 'D274', 'D34', 'D356', 'D368', 'D370']

subs=['-NE-PP','-NE-F','-To-PP','-To-F']
header=['Type','Enzyme','Total','AA', 'aLA', 'EPA', 'DHA', 'LA']
lox=[]
resDF=pd.DataFrame(columns=['Enzyme','Type','PFA','D229', 'D360', 'D384', 'D391', 'D75', 'D274', 'D34', 'D356', 'D368', 'D370'])
for s in subs:
    print s
    sub=data.loc[data.Oxylipin.str.contains(s)]
    total=sub[donors].sum()

    # LOX DATA
    enz='LOX'
    enzSub=sub.loc[sub['Enzyme ']==enz]
    enzTot=enzSub[donors].sum()/total
    enzTot['Enzyme']=enz
    enzTot['Type']=s[1:]
    enzTot['PFA']='Total'
    resDF=resDF.append(enzTot,ignore_index=True)
    for pfa in pfas:
        pfaSub=sub.loc[sub['Parent FA']==pfa]
        pfaEnz=enzSub.loc[enzSub['Parent FA']==pfa]
        enzPfaAct=pfaEnz[donors].sum()/pfaSub[donors].sum()
        
        enzPfaAct['Enzyme']=enz
        enzPfaAct['Type']=s[1:]
        enzPfaAct['PFA']=pfa

        resDF=resDF.append(enzPfaAct,ignore_index=True)

    # CYP DATA
    enz='CYP '
    enzSub=sub.loc[sub['Enzyme ']==enz]
    enzTot=enzSub[donors].sum()/total
    enzTot['Enzyme']=enz
    enzTot['Type']=s[1:]
    enzTot['PFA']='Total'
    resDF=resDF.append(enzTot,ignore_index=True)
    for pfa in pfas:
        pfaSub=sub.loc[sub['Parent FA']==pfa]
        pfaEnz=enzSub.loc[enzSub['Parent FA']==pfa]
        enzPfaAct=pfaEnz[donors].sum()/pfaSub[donors].sum()
        
        enzPfaAct['Enzyme']=enz
        enzPfaAct['Type']=s[1:]
        enzPfaAct['PFA']=pfa

        resDF=resDF.append(enzPfaAct,ignore_index=True)

    # COX DATA
    enz='COX'
    enzSub=sub.loc[sub['Enzyme ']==enz]
    enzTot=enzSub[donors].sum()/total
    enzTot['Enzyme']=enz
    enzTot['Type']=s[1:]
    enzTot['PFA']='Total'
    resDF=resDF.append(enzTot,ignore_index=True)
    for pfa in pfas:
        pfaSub=sub.loc[sub['Parent FA']==pfa]
        pfaEnz=enzSub.loc[enzSub['Parent FA']==pfa]
        enzPfaAct=pfaEnz[donors].sum()/pfaSub[donors].sum()
        
        enzPfaAct['Enzyme']=enz
        enzPfaAct['Type']=s[1:]
        enzPfaAct['PFA']=pfa

        resDF=resDF.append(enzPfaAct,ignore_index=True)

    # SEH DATA
    enz='SEH'

    cypSub=sub.loc[sub['Enzyme ']=='CYP ']
    cypTotal=cypSub[donors].sum()

    enzSub=sub.loc[sub['Enzyme ']==enz]
    
    enzTot=enzSub[donors].sum()/cypTotal
    enzTot['Enzyme']=enz
    enzTot['Type']=s[1:]+' (CYP METABOLITES)'
    enzTot['PFA']='Total'
    resDF=resDF.append(enzTot,ignore_index=True)
    for pfa in pfas:
        pfaSub=cypSub.loc[cypSub['Parent FA']==pfa]
        pfaEnz=enzSub.loc[enzSub['Parent FA']==pfa]
        enzPfaAct=pfaEnz[donors].sum()/pfaSub[donors].sum()
        
        enzPfaAct['Enzyme']=enz
        enzPfaAct['Type']=s[1:]+' (CYP METABOLITES)'
        enzPfaAct['PFA']=pfa

        resDF=resDF.append(enzPfaAct,ignore_index=True)
    



