from random import *
import numpy as np
from math import *
from statistics import *
w = 32 #input length
l = 28 #output length
c = 1 #how many bits are excluded in the lsb hash 
def hashGenerator():
	a = randrange(2**w) 
	if a%2 == 0:
		a += 1
	b = randrange(2**l)
	return lambda x: int(((a*x +b) %(2**w) )/ 2**(w-l))
	#return lambda x: (a*x+b) >> (w-l)
def twoForOne(val):
	i = val & (2**(l-c)-1) # get the l-c lower bits 
	a = val >> (l-1) # get the high bit  
	#print(val.bit_length())
	s = 1 - (a << 1) # sign
	return (i,s)
def initiateCS(vals):
	delta = .0005
	epsilon = .05
	n = int(log(1/delta)) #how many copies we will run
	results = np.zeros((n,2**l))
	hashFunctions = []
	for i in range(n):
		hashFunctions.append(hashGenerator())
	for val in vals:
		for i in range(n):
			results[i][twoForOne(hashFunctions[i](val))[0]] = results[i][twoForOne(hashFunctions[i](val))[0]] + twoForOne(hashFunctions[i](val))[1]
	return(results, hashFunctions)
def queryCS(results, hashFunctions, val):
	tmp = []
	for i in range(len(hashFunctions)):
		bucket = twoForOne(hashFunctions[i](val))[0]
		tmp.append(results[i][bucket])
	return median(tmp)
if __name__=="__main__":
	vals = []
	for i in range(10):
		vals.append(randrange(2**w))
	res, hf = initiateCS(vals)
	print(queryCS(res,hf,vals[0]))