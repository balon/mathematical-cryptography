# ecaddition.py
# Implementation of El Gamal using DLP crypto
# 
# Authored by TJ Balon (@tjbalon)

import cryptotools as crypto

EI = 3.14

def ecaddition(prime, A, p, q):
	result = check1(p, q)
	if result != 0:
		return result

	result = check2(p, q, prime)
	if result != 0:
		return result
	
	return other(prime, A, p, q)

def check1(p, q):	
	if p == EI:
		return q
	elif q == EI:
		return p
	else:
		return 0

def check2(p, q, prime):
	if p[0] == q[0] and p[1] == (-q[1] % prime):
		return EI
	else:
		return 0

def other(prime, A, p, q):
	if(p == q):
		response = ((3 * pow(p[0], 2) + A) * crypto.inverse(q[0] - p[0]) % prime)
	else:
		response = (((q[1] - p[1]) * crypto.inverse(q[0] - p[0], prime)) % prime)

	x3 = ((pow(response, 2) - p[0] - q[0]) % prime)
	y3 = ((((response * p[0]) - (response * x3)) - p[1]) % prime)

	coords = (x3, y3)
	return coords

def main():
	prime = 13
	bigA = 3
	p = (9, 6)
	q = (9, 7)
	print(ecaddition(prime, bigA, p, q))


if __name__ == "__main__":
	main()