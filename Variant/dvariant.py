import ast
from FaultLocalization.DataReader import DataReader
def mid(x,y,z): #2 1 3
	m = z
	if (y<z):
		if x<y:
			m = y
		elif (x<z):
			m = x # old version : m = y
	else:
		if(x>y):
			m = y
		elif (x>z):
			m = x
	return m