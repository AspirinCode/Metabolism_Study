import numpy as np
import pyvttbl as pt
from collections import namedtuple
import pandas as pd

data_raw=pd.read_csv('../MetData/data_normalized_TGRL.csv',header=3)

time=[0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1] # time
proAnti=[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1] # pro vs anti
sub_id=[0,1,2,3,4,0,1,2,3,4,5,6,7,8,9,5,6,7,8,9] #id
groupTitles=['P-value (time)','P-value (proAnti)','P-value (interaction)']
pValues=[]
for r in range(len(data_raw)):
    row1=data_raw.iloc[r].values.tolist()
    title=row1[0]
    rt=row1[1:]
    Sub = namedtuple('Sub', ['Sub_id', 'rt','time', 'proAnti'])               
    df = pt.DataFrame()
     
    for idx in xrange(len(sub_id)):
        df.insert(Sub(sub_id[idx],rt[idx], time[idx],proAnti[idx])._asdict())  

    aov = df.anova('rt', sub='Sub_id', wfactors=['time'],bfactors=['proAnti'])
    i=0
    tempPVals=[]
    for factor in aov.iteritems():
        if i < 3:
            fType=groupTitles[i]
            pval=factor[1]['p']
            tempPVals.append(pval)
        i+=1
    pValues.append(tempPVals)


pValuesDF=pd.DataFrame(pValues,columns=groupTitles)

resultDF=pd.concat([data_raw,pValuesDF],axis=1)

resultDF.to_csv('../results/mixedAnova.csv',index=False)
    



