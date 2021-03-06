from operator import add
import numpy as np
import re
import scipy.stats as stat
from rpy2.robjects.packages import importr
import rpy2.robjects as ro

def F_PP(Input):
	F = []
	P = []
	rows = len(Input)
	cols = len(Input[0])
	for i in range(rows):
		pSearch= re.search('-P',Input[i][0])
		fSearch = re.search('-F',Input[i][0])
		if (fSearch):
			F.append(Input[i])
		if (pSearch):
			P.append(Input[i])
	return F,P



def FP_Pairing(F,P):
	Frow = len(F)
	Prow = len(P)
	cols = len(F[0])
	pairs = list()
	noMatch=[u'Unmatched with corresponding PP']
	if(len(F[0]) != len(P[0])):
		print 'Error, inputs have different numnber of columns'
	for i in range(Frow):
		matched=0
		name = F[i][0][:-2]
		pat = re.compile('^'+re.escape(name))
		for j in range(Prow):
			match = pat.search(P[j][0])
			if match:
				pairs.append([F[i],P[j]])
				matched = 1
		if(not matched):

			noMatch.append(F[i][0])
	return pairs,noMatch

def Nefa_Sort(pairs):
	ne=[]
	to=[]
	for i in pairs:
		isNe=re.search('-NE-',i[0][0])
		if isNe:
			ne.append(i)
		else:
			to.append(i)
	return ne,to

def Org_Sum(pairs,orgType):
	orgSum = dict()
	orgTemp=dict()
	hasNone=[u'Contains empty values']
	rows = len(pairs)

	if len(orgType)==2:
		for m in orgType[0]:
			for k in orgType[1]:
				orgSum[m+': '+k] = [[0]*10,[0]*10]
				for j in range(rows):
					row = pairs[j]
					if(pairs[j][0][2] == m or pairs[j][0][1] == m) and not contains_Nonetype(row[0],row[1]) and (pairs[j][0][2] == k or pairs[j][0][1] == k):
						x = [orgSum[m+': '+k][0][z-3]+row[0][z] for z in range(3,13) ] #Fasting
						orgSum[m+': '+k][0] = x
						y = [orgSum[m+': '+k][1][z-3]+row[1][z] for z in range(3,13) ] #Post Prandial
						orgSum[m+': '+k][1] = y
					if(contains_Nonetype(row[0],row[1])): #keeps log of incomplete data oxylipins
						hasNone.append(row[0][0][:-2])						

	else:
		for m in orgType:
			orgSum[m] = [[0]*10,[0]*10]
			for j in range(rows):
				row = pairs[j]
				if(pairs[j][0][2] == m or pairs[j][0][1] == m) and not contains_Nonetype(row[0],row[1]):
					x = [orgSum[m][0][z-3]+row[0][z] for z in range(3,13) ] #Fasting
					for j in x:
						if j>80:
							#print [row,x]
					orgSum[m][0] = x
					y = [orgSum[m][1][z-3]+row[1][z] for z in range(3,13) ] #Post Prandial
					orgSum[m][1] = y

				if(contains_Nonetype(row[0],row[1])): #keeps log of incomplete data oxylipins
					hasNone.append(row[0][0][:-2])


	return orgSum,list(set(hasNone))

def contains_Nonetype(in1,in2):
	none = False
	for x in in1:
		if x is None:
			none = True
			return none
	for y in in2:
		if y is None:
			none = True
			return none
	return none

def Paired_T(input,orgType):
	allDonors=dict()
	for m in orgType:
		Fasting=input[m][0]
		Post=input[m][1]
		allDonors[m]=stat.ttest_rel(Fasting,Post).pvalue

	return allDonors

def Ttest(input,label): #orgSum dictionary is input
	tests=[[label,'Overall','Pro','Anti','Fasting','ANCOVA FA','ANCOVA GRP']]
	i=0
	for m in input.keys():
		AntiF = input[m][0][0:5]
		ProF = input[m][0][5:10]
		AntiP = input[m][1][0:5]
		ProP = input[m][1][5:10]
		Fasting=input[m][0]
		Post=input[m][1]

		ttest=range(7)
		ttest[0] = m
		ttest[1] = stat.ttest_rel(Fasting,Post).pvalue
		ttest[2] = stat.ttest_rel(ProF,ProP).pvalue
		ttest[3] = stat.ttest_rel(AntiF,AntiP).pvalue
		ttest[4] = stat.ttest_ind(AntiF,ProF).pvalue

		stats=importr('stats')
		broom=importr('broom')
		P = ro.FloatVector(Post)
		Fa = ro.FloatVector(Fasting)
		grp = ro.IntVector([1,1,1,1,1,2,2,2,2,2])
		ro.globalenv["P"]=P
		ro.globalenv["Fa"]=Fa
		ro.globalenv["grp"]=grp
		test = ro.r('aov(P ~ Fa + grp)')
		test = broom.tidy(test)
		pvals=test.rx2('p.value')

		ttest[5]=float(pvals[0])
		ttest[6]=float(pvals[1])

		if type(ttest[6]) == 'rpy2.rinterface.NARealType':
			ttest[6]='None'

		for x in range(6):
			try:
				if (not ttest[x]):
					ttest[x] = 'None'
			except ValueError:
				ttest[x]='None'
				print label +' '+str(ttest[x])
		tests.append(ttest)
		i=i+1
	return tests
def sort(SheetIn):

	PFA =	['AA', 'aLA', 'EPA', 'DHA', 'LA']
	Oxy =	['Ketones', 'Diols', 'Alcohols','Alcohol Precursors', 'Epoxides','Triols','Prostaglandins']
	Both = [PFA,Oxy]

	[F,P]=F_PP(SheetIn) # Create Fasting and PP
	[pairs,noMatch]=FP_Pairing(F,P)#Pair matching fasting and pp
	[ne,to]=Nefa_Sort(pairs) # Sorts to nefa and total
	
	#Class organization for nefa and total seperately
	[neOxySum,hasNone]=Org_Sum(ne,Oxy)
	[nePfaSum,hasNone]=Org_Sum(ne,PFA)
	[toOxySum,hasNone]=Org_Sum(to,Oxy)
	[toPfaSum,hasNone]=Org_Sum(to,PFA)

	[neBothSum,hasNone]=Org_Sum(ne,Both)
	[toBothSum,hasNone]=Org_Sum(to,Both)
	#organize according to classes for all
	[pfaSum,hasNone]=Org_Sum(pairs,PFA) 
	[oxySum,hasNone]=Org_Sum(pairs,Oxy)
	[bothSum,hasNone]=Org_Sum(pairs,Both)



	oxyTest=Ttest(oxySum,'Oxylipin') # run ttest on each grouping
	pfaTest=Ttest(pfaSum,'Parent FA')
	bothTest=Ttest(bothSum,'PFA: Oxylipin')

	neOxyTest=Ttest(neOxySum,'Oxylipin - NEFA') 
	nePfaTest=Ttest(nePfaSum,'Parent FA - NEFA')
	toOxyTest=Ttest(toOxySum,'Oxylipin - To') 
	toPfaTest=Ttest(toPfaSum,'Parent FA - To')
	neBothTest=Ttest(neBothSum,'PFA: Oxylipin - NEFA')
	toBothTest=Ttest(toBothSum,'PFA: Oxylipin - to')

	data=[oxyTest,pfaTest,bothTest,neOxyTest,nePfaTest,neBothTest,toOxyTest,toPfaTest,toBothTest,hasNone,noMatch]
	sums=[oxySum,pfaSum,bothSum,neOxySum,nePfaSum,neBothSum,toOxySum,toPfaSum,toBothSum]
	return [data,sums]

def write_results(input,outSheet,outSheet2):
	for item in range(len(input[0])):
		for row in input[0][item]:
			if isinstance(row,unicode):
				row = [row]
			outSheet.append(row)
		empty=[]
		outSheet.append(empty)
		if item < 9:
			heading = input[0][item][0][0]+' Sums'
			heading = [heading]

			outSheet2.append(heading)
			for key in input[1][item]:			
				
				states = [' -F',' -PP']
				for state in range(len(input[1][item][key])):
					title = key + states[state]
					row=[]
					row.append(title)
					for donor in input[1][item][key][state]:
						row.append(donor)
					outSheet2.append(row)




	pass


