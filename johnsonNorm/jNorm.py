import pandas as pd
import numpy as np
import scipy.stats as stats

dr=pd.read_csv('johnsonNorm.csv',header=8)


fData=dr.loc[dr['Metabolite'].str.contains('-F')]
pData=dr.loc[dr['Metabolite'].str.contains('-PP')]
donors=[u'D229', u'D360', u'D384', u'D391',
       u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']


resultHead=['Metabolite',u'F-D229', u'F-D360', u'F-D384', u'F-D391',
       u'F-D75', u'F-D274', u'F-D34', u'F-D356', u'F-D368', u'F-D370',u'PP-D229', u'PP-D360', u'PP-D384', u'PP-D391',
       u'PP-D75', u'PP-D274', u'PP-D34', u'PP-D356', u'PP-D368', u'PP-D370']
results=[]

for ind in range(len(fData)):
    fSamp=fData.iloc[ind]

    metab=fSamp['Metabolite'][:-1]
    metabRegex='^'+metab+'PP' 
    metabRegex=metabRegex.replace('(','\(')
    metabRegex=metabRegex.replace(')','\)')
    pSamp=pData.loc[pData['Metabolite'].str.contains(metabRegex)]

    if pSamp.empty:
        print 'NO MATCH: '+metab[:-1]
    else:
        pSamp=pSamp.iloc[0][donors].values.tolist()
        fSamp=fSamp[donors].values.tolist()
        #print metab[:-1]
        #print 'p-value: ',p
        result=fSamp+pSamp
        result.insert(0,metab[:-1])
        results.append(result)

resultDF=pd.DataFrame(results,columns=resultHead)
        

