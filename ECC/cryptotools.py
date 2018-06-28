# cryptotools.py
# FastPower, Inverse, FastAddition, ECC-Addition, etc
# Tools and functions for DLP and ECC Crypto-System Implementations
#
# Authored by TJ Balon (@tjbalon)
# -----------------------------------------------------------------
from functools import reduce 

# -----------------------------------------------------------------
def fastpower(base, exp, prime):
  ''' fastpower():
      - Accepts a base, exponent, prime. Computes fast-power solution.
  '''

  # Variables
  pAll = []
  pNeed = []

  bExp = "{0:b}".format(exp) # Convert the exponent into binary

  # Fast-Power
  isBase = 0
  for index in reversed(bExp):
    # if power is 0, set base; else compute all[-1]^2
    val = isBase and (pow(pAll[-1], 2) % prime) or base

    if int(index) == 1:           # if index is 1, bit is on so needed
      pNeed.append(val)           # store in our needed array

    pAll.append(val)              # store in all val to comptue powers fast
    isBase += 1                    # increment our power

  print("All values: ", pAll)
  print("Needed values: ", pNeed)

  return (reduce(lambda x, y: x*y, pNeed) % prime)

# -----------------------------------------------------------------
def inverse(base, prime):
  ''' inverse():
    - Accept base, prime. Compute inverse using prime - 2 method
  '''

  if base > prime:
    base = base % prime

  return fastpower(base, prime - 2, prime)

# -----------------------------------------------------------------
def datapack(*argv):
  ''' datapack():
    - Accepts variable number of items and puts in list
  '''
  dp = []
  for arg in argv:
    dp.append(arg)

  return dp

# -----------------------------------------------------------------
# ECC ADDITION PORTION --- FUNCTIONS MUST BE IN THIS ORDER!
# -----------------------------------------------------------------

# Global Variables
EI = 3.14
x = 0
y = 1

# -----------------------------------------------------------------
# EC Addition Functions (Merged)                              START 
# -----------------------------------------------------------------
def eccadd(prime, eqvarA, pointP, pointQ):
  result = infinityCheck(pointP, pointQ)
  if result != 0:
    return result

  result = inverseCheck(pointP, pointQ, prime)
  if result != 0:
    return result
  
  return advaddition(prime, eqvarA, pointP, pointQ)

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

def advaddition(prime, eqvarA, pointP, pointQ):
  if(pointP == pointQ):
    eqLambda = ((3 * pow(pointP[x], 2) + eqvarA) * (inverse(2 * pointP[y], prime)) % prime)
  else:
    eqLambda = (((pointQ[y] - pointP[y]) * inverse(pointQ[x] - pointP[x], prime)) % prime)

  x3 = ((pow(eqLambda, 2) - pointP[x] - pointQ[x]) % prime)
  y3 = ((((eqLambda * pointP[x]) - (eqLambda * x3)) - pointP[y]) % prime)

  coords = (x3, y3)
  return coords
# -----------------------------------------------------------------
# EC Addition Functions (Merged)                                END
# -----------------------------------------------------------------


# -----------------------------------------------------------------
def fastaddition(base, coeff, prime, eqvarA):
  ''' fastaddition():
      - Accepts a base, coefficient, prime. Computes fast-power solution.
  '''

  # Variables
  pAll = []
  pNeed = []

  bCoeff = "{0:b}".format(coeff) # Convert the exponent into binary

  # Fast-Power
  isBase = 0
  for index in reversed(bCoeff):
    # if power is 0, set base; else compute all[-1]^2
    val = isBase and (eccadd(prime, eqvarA, pAll[-1], pAll[-1])) or base

    if int(index) == 1:           # if index is 1, bit is on so needed
      pNeed.append(val)           # store in our needed array

    pAll.append(val)              # store in all val to comptue powers fast
    isBase += 1                    # increment our power

  print("All values: ", pAll)
  print("Needed values: ", pNeed)

  return (reduce(lambda x, y: eccadd(prime, eqvarA, x, y), pNeed))

# -----------------------------------------------------------------