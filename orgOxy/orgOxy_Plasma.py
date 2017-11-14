import pandas as pd
import numpy as np
import scipy.stats as stats

donors=[u'D229', u'D360', u'D384', u'D391',
       u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
proAnti=['Anti','Anti','Anti','Anti','Anti','Pro','Pro','Pro','Pro','Pro']
Plasma=pd.read_csv('../MetData/Plasma.csv',nrows=438)
Plasma[donors] = (
    Plasma[donors]
    # Replace things that aren't numbers and change any empty entries to nan
    # (to allow type conversion)
    .replace({r'[^0-9\.]': '', '': np.nan}, regex=True)
    # Change to float and convert from %s
    .astype(np.float64) 
)
Plasma=Plasma.sort_values(by=['Metabolite'])
rep='Anti'
for fa in ['To','NE']:
    for t in ['-F','-PP']:
        tempD=Plasma.loc[Plasma['Metabolite'].str.contains(t)]
        tempD=tempD.loc[tempD['Metabolite'].str.contains(fa)]
        names=tempD['Metabolite'].values.tolist()
        subCount=-len(t)
        for i in range(len(names)):
            names[i]=names[i][:subCount]
            
        print( ", ".join( str(e) for e in ['donors','Anti/Pro','PP/F','NE/To']+names ) )
        for i in range(len(donors)):
            tempRes=tempD[donors[i]].values.tolist()
            tempRes=[donors[i]]+[proAnti[i]]+[t[1:]]+[fa]+tempRes
            print( ", ".join( str(e) for e in tempRes ) )
            

#TGRLfData=TGRL.loc[TGRL['Metabolite'].str.contains('-F')]
#TGRLpData=TGRL.loc[TGRL['Metabolite'].str.contains('-PP')]
#PlasmafData=Plasma.loc[Plasma['Metabolite'].str.contains('-F')]
#PlasmapData=Plasma.loc[Plasma['Metabolite'].str.contains('-PP')]
#
#resultHead=['Metabolite',u'PP-F D229', u'PP-F D360', u'PP-F D384', u'PP-F D391',
#       u'PP-F D75', u'PP-F D274', u'PP-F D34', u'PP-F D356', u'PP-F D368', u'PP-F D370',u'PP/F D229', u'PP/F D360', u'PP/F D384', u'PP/F D391',
#       u'PP/F D75', u'PP/F D274', u'PP/F D34', u'PP/F D356', u'PP/F D368', u'PP/F D370']

