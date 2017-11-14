import pandas as pd
import numpy as np
import scipy.stats as stats

donors=[u'D229', u'D360', u'D384', u'D391',
       u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
TGRL=pd.read_csv('../MetData/TGRL.csv',nrows=429)
TGRL[donors] = (
    TGRL[donors]
    # Replace things that aren't numbers and change any empty entries to nan
    # (to allow type conversion)
    .replace({r'[^0-9\.]': '', '': np.nan}, regex=True)
    # Change to float and convert from %s
    .astype(np.float64) 
)

Plasma=pd.read_csv('../MetData/Plasma.csv',nrows=438)
Plasma[donors] = (
    Plasma[donors]
    # Replace things that aren't numbers and change any empty entries to nan
    # (to allow type conversion)
    .replace({r'[^0-9\.]': '', '': np.nan}, regex=True)
    # Change to float and convert from %s
    .astype(np.float64) 
)


TGRLfData=TGRL.loc[TGRL['Metabolite'].str.contains('-F')]
TGRLpData=TGRL.loc[TGRL['Metabolite'].str.contains('-PP')]
PlasmafData=Plasma.loc[Plasma['Metabolite'].str.contains('-F')]
PlasmapData=Plasma.loc[Plasma['Metabolite'].str.contains('-PP')]

resultHead=['Metabolite',u'PP-F D229', u'PP-F D360', u'PP-F D384', u'PP-F D391',
       u'PP-F D75', u'PP-F D274', u'PP-F D34', u'PP-F D356', u'PP-F D368', u'PP-F D370',u'PP/F D229', u'PP/F D360', u'PP/F D384', u'PP/F D391',
       u'PP/F D75', u'PP/F D274', u'PP/F D34', u'PP/F D356', u'PP/F D368', u'PP/F D370']

TGRLresults=[]

## TGRL Pairing
for ind in range(len(TGRLfData)):
    fSamp=TGRLfData.iloc[ind]

    metab=fSamp['Metabolite'][:-1]
    metabRegex='^'+metab+'PP' 
    metabRegex=metabRegex.replace('(','\(')
    metabRegex=metabRegex.replace(')','\)')
    pSamp=TGRLpData.loc[TGRLpData['Metabolite'].str.contains(metabRegex)]

    if pSamp.empty:
        print 'NO MATCH: '+metab[:-1]
    else:
        pSamp=pd.to_numeric(pSamp.iloc[0][donors])
        fSamp=pd.to_numeric(fSamp[donors].values.tolist())

        diff=pSamp-fSamp
        div=pSamp/fSamp

        result=diff.values.tolist()+div.values.tolist()
        result.insert(0,metab[:-1])

        TGRLresults.append(result)
TGRLDF=pd.DataFrame(TGRLresults,columns=resultHead)

## Plasma Pairing
Plasmaresults=[]
for ind in range(len(PlasmafData)):
    fSamp=PlasmafData.iloc[ind]

    metab=fSamp['Metabolite'][:-1]
    metabRegex='^'+metab+'PP' 
    metabRegex=metabRegex.replace('(','\(')
    metabRegex=metabRegex.replace(')','\)')
    pSamp=PlasmapData.loc[PlasmapData['Metabolite'].str.contains(metabRegex)]

    if pSamp.empty:
        print 'NO MATCH: '+metab[:-1]
    else:
        pSamp=pd.to_numeric(pSamp.iloc[0][donors])
        fSamp=pd.to_numeric(fSamp[donors].values.tolist())

        diff=pSamp-fSamp
        div=pSamp/fSamp

        result=diff.values.tolist()+div.values.tolist()
        result.insert(0,metab[:-1])

        Plasmaresults.append(result)
PlasmaDF=pd.DataFrame(Plasmaresults,columns=resultHead)
        


