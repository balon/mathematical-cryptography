# cryptotools.py
# FastPower, Inverse, etc
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
  power = 0
  for index in reversed(bExp):
    # if power is 0, set base; else compute all[-1]^2
    val = power and (pow(pAll[-1], 2) % prime) or base

    if int(index) == 1:           # if index is 1, bit is on so needed
      pNeed.append(val)           # store in our needed array

    pAll.append(val)              # store in all val to comptue powers fast
    power += 1                    # increment our power

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
