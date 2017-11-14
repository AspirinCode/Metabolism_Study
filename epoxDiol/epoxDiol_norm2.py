import pandas as pd
import numpy as np
import scipy.stats as stats

data_raw=pd.read_csv('../MetData/epoxDiolTypes.csv')

donors=[u'D229', u'D360',u'D384', u'D391', u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']

VCAM=data_raw.iloc[0][donors]

resultHead=['Type','r^','p','Pearsons']
results=[]
for i in range(len(data_raw)-1):
    j=i+1
    title=data_raw.iloc[j][0]
    response=data_raw.iloc[j][donors]
    slope, intercept, r,p, std_err = stats.linregress(response,VCAM)
    pearson,p=stats.pearsonr(response,VCAM)

    results.append([title,r**2,p,pearson])
    
resultsDF=pd.DataFrame(results,columns=resultHead)
