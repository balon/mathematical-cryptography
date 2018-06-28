# ecc-elgamal.py
# Encrypter and Decrypter Classes using ECC (Elliptic Curve Crypto)
# Modular approach to using El Gamal. This system used ECC.
#
# Authored by TJ Balon (@tjbalon)
# -----------------------------------------------------------------
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import cryptotools as crypto
import random as rand

# -----------------------------------------------------------------
class Decrypter:
  'Decrypter class, controls decrypting data'

  def __init__(self, pointP, prime, eqvarA):
    self.pointP = pointP
    self.prime = prime
    self.eqvarA = eqvarA

    # Get a privateKey from the user to use
    while True:
      try:
        self._privateKey = int(input("Insert a private key (private info): "))
        break
      except:
        print("Error: PrivateKey must be an integer!") 

    # Generate publicKey
    self.publicKey = crypto.fastaddition(self.pointP, self._privateKey, self.prime, eqvarA)
    print("Public Key: ", self.publicKey)

  def getPubkey(self):
    return self.publicKey

  def doDecrypt(self, dpk):
    # Get the point with the private key kP
    unlockedPoint = crypto.fastaddition(dpk[0], self._privateKey, self.prime, self.eqvarA)

    # find the inverse (Inverse of unlockedPoint)
    inversePoint = crypto.eccinverse(unlockedPoint)

    # ECC Add inverse to c2 from bob
    return (crypto.eccadd(self.prime, self.eqvarA, dpk[1], inversePoint))


# -----------------------------------------------------------------
class Encrypter:
  'Encrypter class, controls encrypting data'

  def __init__(self, pointP, prime, eqvarA):
    self.pointP = pointP
    self.prime = prime
    self.eqvarA = eqvarA

    # Get a message from the user to use
    while True:
      try:
        self._message = input("Insert a message (M) format as x,y [private info]: ")
        self._message = tuple(map(int,self._message.split(',')))  
        break
      except:
        print("Error: Message must be an in format x,y! Example: 2,3") 

  def encryptMsg(self, ePubkey):
    key = rand.randint(1, self.prime)

    print("Sending message: ", self._message)
    print("Using ephemeral key: ", key)

    encodedPoint = crypto.fastaddition(self.pointP, key, self.prime, self.eqvarA)
    encodedPub = crypto.fastaddition(ePubkey, key, self.prime, self.eqvarA)
    encodedMsg = crypto.eccadd(self.prime, self.eqvarA, encodedPub, self._message)

    print("g raised to k: ", encodedPoint)
    print("Encoded message: ", encodedMsg)

    self.dpk = crypto.datapack(generatorKey, encodedMsg)
    print("Stored datapack: ", self.dpk)

  # Return datapack of encrypted message and encoded point
  def getEncrypted(self):
    return self.dpk


# -----------------------------------------------------------------
def main():
  # Control Encrypt/Decrypt Process

  # Start by getting the first point from the user.
  while True:
    try:
      pointP = input("Insert a point (P) format as x,y [public info]: ")
      pointP = tuple(map(int,pointP.split(',')))  
      break
    except:
      print("Error: Point must be an in format x,y! Example: 2,3")

  # Get the prime from the user, validating input!
  while True:
    try:
      prime = int(input("Insert a prime (public info): "))
      break
    except:
      print("Error: Prime must be an integer!")

  # Get A from the user (equation)
  while True:
    try:
      eqvarA = int(input("Insert A (from the equation): "))
      break
    except:
      print("Error: Equation Variable A must be an integer!")

  print("Starting Point: ", pointP)
  print("Prime: ", prime)
  print("A: ", eqvarA)

  # Initialize Alice & Bob
  alice = Decrypter(pointP, prime, eqvarA)
  bob = Encrypter(pointP, prime, eqvarA)

  # Bob encrypts message, with Alice pub-key
  bob.encryptMsg(alice.getPubkey())

  # Alice decrypts message, then prints before exit
  decoded = alice.doDecrypt(bob.getEncrypted())

  print("Decoded/Decrypted message: ", decoded)


# -----------------------------------------------------------------
if __name__ == "__main__":
  main()