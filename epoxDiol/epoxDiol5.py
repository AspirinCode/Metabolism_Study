import pandas as pd

dr=pd.read_csv('../results/epoxDiol_2.csv')


nepp=dr['Diol NE-PP sum']/dr['Epoxide NE-PP sum']
nef=dr['Diol NE-F sum']/dr['Epoxide NE-F sum']
topp=dr['Diol To-PP sum']/dr['Epoxide To-PP sum']
tof=dr['Diol To-F sum']/dr['Epoxide To-F sum']



dr['NE-PP Ratio']=nepp
dr['NE-F Ratio']=nef
dr['To-PP Ratio']=topp
dr['To-F Ratio']=tof




