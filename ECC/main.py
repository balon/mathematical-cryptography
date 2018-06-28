# main.py
# Corpse to call other functions
#
# Authored by TJ Balon (@tjbalon)
# -----------------------------------------------------------------
import cryptotools as crypto

def main():
	prime = 13
	eqvarA = 3
	pointP = (1, 5)
	coeff = 6
	print(crypto.fastaddition(pointP, coeff, prime, eqvarA))



if __name__ == "__main__":
	main()