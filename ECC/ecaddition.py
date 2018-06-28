# ecaddition.py
# Elliptic Curve Addition Function
# 
# Authored by TJ Balon (@tjbalon)
import cryptotools as crypto

# Global Variables
EI = 3.14
x = 0
y = 1

def add(prime, eqvarA, pointP, pointQ):
	result = infinityCheck(pointP, pointQ)
	if result != 0:
		return result

	result = inverseCheck(pointP, pointQ, prime)
	if result != 0:
		return result
	
	return ecaddition(prime, eqvarA, pointP, pointQ)

def infinityCheck(pointP, pointQ):	
	if pointP == EI:
		return pointQ
	elif pointQ == EI:
		return pointP
	else:
		return 0

def inverseCheck(pointP, pointQ, prime):
	if pointP[x] == pointQ[x] and pointP[y] == (-pointQ[y] % prime):
		return EI
	else:
		return 0

def ecaddition(prime, eqvarA, pointP, pointQ):
	if(pointP == pointQ):
		eqLambda = ((3 * pow(pointP[x], 2) + eqvarA) * (crypto.inverse(2 * pointP[y], prime)) % prime)
	else:
		eqLambda = (((pointQ[y] - pointP[y]) * crypto.inverse(pointQ[x] - pointP[x], prime)) % prime)

	x3 = ((pow(eqLambda, 2) - pointP[x] - pointQ[x]) % prime)
	y3 = ((((eqLambda * pointP[x]) - (eqLambda * x3)) - pointP[y]) % prime)

	coords = (x3, y3)
	return coords

def main():
	prime = 13
	eqvarA = 3
	pointP = (1, 8)
	pointQ = (1, 8)
	print(add(prime, eqvarA, pointP, pointQ))


if __name__ == "__main__":
	main()