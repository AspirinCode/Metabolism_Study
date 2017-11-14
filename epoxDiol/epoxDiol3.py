import pandas as pd
import numpy as np
import scipy.stats as stats

data_raw=pd.read_csv('../MetData/Classification_Epoxides_diols.csv')
parentFA=['All','AA', 'LA', 'DHA', 'ALA', 'EPA']
donors=[u'D229', u'D360',u'D384', u'D391', u'D75', u'D274', u'D34', u'D356', u'D368', u'D370']
VCAM=data_raw.loc[0][donors].values.astype(np.float)

types=['Epoxide NE-PP -F sum', 'Epoxide To-PP-F sum', 'Diol To-F sum', 'VCAM-1 ', 'Diol To-PP-F sum', 'Diol NE-F sum', 'Epoxide To-PP -Fsum', 'Diol NE-PP-F sum', 'Diol To-PP sum', 'Epoxide NE-PP -Fsum', 'Epoxide To-F sum', 'Diol NE-PP sum', 'Epoxide NE-F sum', 'Diol NE-PP -Fsum', 'DiolTo-PP-F sum', 'Epoxide NE-PP-F sum', 'Epoxide NE-PP sum', 'Epoxide To-PP sum', 'Diol NE -PP -F sum', 'Diol To-PP -Fsum', 'Epoxide To-PP -F sum', 'Diol To-PP -F sum']


resultsHead=['Parent Fatty Acid','To P-value','NE P-Value','To-PP P-Value','To-F P-Value','NE-PP P-Value','NE-F P-Value','To r^2','NE r^2','To-PP r^2','To-F r^2','NE-PP r^2','NE-F r^2','To Pearsons','NE Perasons','To-PP Pearsons','To-F Pearsons','NE-PP Pearsons','NE-F Perasons']
results=[]

def div0( a, b ):
    """ ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0] """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 0  # -inf inf NaN
    return c

for pfa in parentFA:
    print pfa
    dataPFA=data_raw[data_raw['pfa']==pfa]
    EpoxNE=dataPFA[dataPFA['Type']=='Epoxide NE-PP-F sum']
    EpoxTo=dataPFA[dataPFA['Type']=='Epoxide To-PP-F sum']

    EpoxNE_pp=dataPFA[dataPFA['Type']=='Epoxide NE-PP sum']
    EpoxNE_f=dataPFA[dataPFA['Type']=='Epoxide NE-F sum']
    EpoxTo_pp=dataPFA[dataPFA['Type']=='Epoxide To-PP sum']
    EpoxTo_f=dataPFA[dataPFA['Type']=='Epoxide To-F sum']

    DiolNE=dataPFA[dataPFA['Type']=='Diol NE-PP-F sum']
    DiolTo=dataPFA[dataPFA['Type']=='Diol To-PP-F sum']

    DiolNE_pp=dataPFA[dataPFA['Type']=='Diol NE-PP sum']
    DiolNE_f=dataPFA[dataPFA['Type']=='Diol NE-F sum']
    DiolTo_pp=dataPFA[dataPFA['Type']=='Diol To-PP sum']
    DiolTo_f=dataPFA[dataPFA['Type']=='Diol To-F sum']

    NeRatio_pp=div0(EpoxNE_pp[donors].values.astype(np.float),DiolNE_pp[donors].values.astype(np.float))
    if len(NeRatio_pp):
        NeRatio_pp=NeRatio_pp[0]
        slope, intercept, ne_pp_r_value, ne_pp_p_value, std_err = stats.linregress(NeRatio_pp,VCAM)
        ne_pp_pearson,p=stats.pearsonr(NeRatio_pp,VCAM)
    else:
        ne_pp_r_value=0
        ne_pp_p_value=0
        ne_pp_pearson=0
    
    ToRatio_pp=div0(EpoxTo_pp[donors].values.astype(np.float),DiolTo_pp[donors].values.astype(np.float))
    if len(ToRatio_pp):
        ToRatio_pp=ToRatio_pp[0]
        slope, intercept, to_pp_r_value, to_pp_p_value, std_err = stats.linregress(ToRatio_pp,VCAM)
        to_pp_pearson,p=stats.pearsonr(ToRatio_pp,VCAM)
    else:
        to_pp_r_value=0
        to_pp_p_value=0
        to_pp_pearson=0

    NeRatio_f=div0(EpoxNE_f[donors].values.astype(np.float),DiolNE_f[donors].values.astype(np.float))
    if len(NeRatio_f):
        NeRatio_f=NeRatio_f[0]
        slope, intercept, ne_f_r_value, ne_f_p_value, std_err = stats.linregress(NeRatio_f,VCAM)
        ne_f_pearson,p=stats.pearsonr(NeRatio_f,VCAM)
    else:
        ne_f_r_value=0
        ne_f_p_value=0
        ne_f_pearson=0
    
    ToRatio_f=div0(EpoxTo_f[donors].values.astype(np.float),DiolTo_f[donors].values.astype(np.float))
    if len(ToRatio_f):
        ToRatio_f=ToRatio_f[0]
        slope, intercept, to_f_r_value, to_f_p_value, std_err = stats.linregress(ToRatio_f,VCAM)
        to_f_pearson,p=stats.pearsonr(ToRatio_f,VCAM)
    else:
        to_f_r_value=0
        to_f_p_value=0
        to_f_pearson=0

    NeRatio=div0(EpoxNE[donors].values.astype(np.float),DiolNE[donors].values.astype(np.float))
    if len(NeRatio):
        NeRatio=NeRatio[0]
        slope, intercept, ne_r_value, ne_p_value, std_err = stats.linregress(NeRatio,VCAM)
        ne_pearson,p=stats.pearsonr(NeRatio,VCAM)
    else:
        ne_r_value=0
        ne_p_value=0
        ne_pearson=0
    
    ToRatio=div0(EpoxTo[donors].values.astype(np.float),DiolTo[donors].values.astype(np.float))
    if len(ToRatio):
        ToRatio=ToRatio[0]
        slope, intercept, to_r_value, to_p_value, std_err = stats.linregress(ToRatio,VCAM)
        to_pearson,p=stats.pearsonr(ToRatio,VCAM)
    else:
        to_r_value=0
        to_p_value=0
        to_pearson=0

    results.append([pfa,to_p_value,ne_p_value,to_pp_p_value,to_f_p_value,ne_pp_p_value,ne_f_p_value,to_r_value**2,ne_r_value**2,to_pp_r_value**2,to_f_r_value**2,ne_pp_r_value**2,ne_f_r_value**2,to_pearson,ne_pearson,to_pp_pearson,to_f_pearson,ne_pp_pearson,ne_f_pearson])


resultsDF=pd.DataFrame(results,columns=resultsHead)
#resultsDF.to_csv('../results/epoxDiol3.csv',index=False)
