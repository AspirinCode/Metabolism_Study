from openpyxl import load_workbook,Workbook
import re

def sortOxylipins(sheetIn,sheetOut,offset):

	#Sets definitions as dictionaries for parent FA and Oxylipins
	parentfaDef =	{
						'LA'	:	['-hode','kode','oxo-ode','epome','dihome','hpode','trihome'],
						'aLA'	:	['-hote','kote','oxo-ote','epode','dihode'],
						'AA'	:	['-hete','kete','oxo-ete','epetre','eet','dihetre','dhet','pgf2a','pgf1a','isops'],
						'EPA'	:	['-hepe','kepe','epete','dihete','hpete','dihetre'],
						'DHA'	:	['hdohe','kdohe','epdope','edp','dihdope','epdpe']
	}
	oxylipinDef	=	{
						'Alcohols'			:	['-hete', '-hote', '-hepe', 'hdohe', '-hode'],
						'Alcohol Precursors': 	['hpete','hpode',],
						'Ketones'			:	['kete','kote','kepe','kdohe','kode'],
						'Epoxides'			:	['epome','epode','epetre','epete','epdope','epdpe'],
						'Diols'				:	['dhet', 'dihode', 'dihete', 'dihdope', 'dihome','dihetre'],
						'Triols'			:	['trihome'],
						'Prostaglandins'	:	['pgf2a','pgf1a','isops']
		
	}

	nameRow 	=	3 +offset
	lastRow		= 	14+offset

	#Looks through relevant rows for every column
	for col in sheetIn.iter_cols(min_row=nameRow,max_row=lastRow):
		tmp=list() #temporarily stores values of columns, used to append as row to final file
		error=list()
		#looks at each cell in the column
		for cell in col:
			tmp.append(cell.value)

			#checks that cell value is the name (aka is a string not number)
			if cell.value and isinstance(cell.value,basestring):

				pfa 		=	0
				oxy 		=	0
				#classification of individual names
				for key,value in parentfaDef.items():
					for x in value:
						matchPFA = re.search(x,cell.value,re.I)					
						if matchPFA:
							pfa = key
				for key,value in oxylipinDef.items():
					for x in value:
						matchOxy = re.search(x,cell.value,re.I)
						if matchOxy:
							oxy = key
	
		if(pfa and oxy and tmp[1]):
			tmp.pop(0) #removes blank space added to tmp
			tmp.insert(1,oxy) #insert oxylipin type
			tmp.insert(2,pfa) #insert parent fatty acid
			sheetOut.append(tmp) #append row to sheet
		if(not(pfa) or not(oxy)) and tmp[1]:
			tmp.pop(0) #removes blank space added to tmp
			tmp.insert(1,oxy) #insert oxylipin type
			tmp.insert(2,pfa) #insert parent fatty acid			
			error.append(tmp)
	print error

	return


