# dlp-elgamal.py
# Encrypter and Decrypter Classes El Gamal.
# Modular approach to using El Gamal. This system uses DLP.
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

  def __init__(self, generator, prime):
    self.generator = generator
    self.prime = prime

    # Get a privateKey from the user to use
    while True:
      try:
        self._privateKey = int(input("Insert a private key (private info): "))
        break
      except:
        print("Error: PrivateKey must be an integer!") 

    # Generate publicKey
    self.publicKey = crypto.fastpower(self.generator, self._privateKey, self.prime)
    print("Public Key: ", self.publicKey)

  def getPubkey(self):
    return self.publicKey

  def doDecrypt(self, dpk):
    # Generate g^(ak)
    unlockedGen = crypto.fastpower(dpk[0], self._privateKey, self.prime)

    # find the inverse of g^(ak) (Inverse of unlockedGen)
    inverseGen = crypto.inverse(unlockedGen, self.prime)

    # Multiply inverse times encrypted message, then mod by the prime
    return ((inverseGen * dpk[1]) % self.prime)


# -----------------------------------------------------------------
class Encrypter:
  'Encrypter class, controls encrypting data'

  def __init__(self, generator, prime):
    self.generator = generator
    self.prime = prime

    # Get a message from the user to use
    while True:
      try:
        self._message = int(input("Insert a message (private info): "))
        break
      except:
        print("Error: Message must be an integer!") 

  def encryptMsg(self, ePubkey):
    key = rand.randint(1, self.prime)

    print("Sending message: ", self._message)
    print("Using ephemeral key: ", key)

    generatorKey = crypto.fastpower(self.generator, key, self.prime)
    encodedPub = crypto.fastpower(ePubkey, key, self.prime)
    encodedMsg = encodedPub * self._message

    print("g raised to k: ", generatorKey)
    print("Encoded message: ", encodedMsg)

    self.dpk = crypto.datapack(generatorKey, encodedMsg)

  # Return datapack of encrypted message and generator raised to k
  def getEncrypted(self):
    return self.dpk


# -----------------------------------------------------------------
def main():
  # Control Encrypt/Decrypt Process

  # Get the generator from the user, validating input!
  while True:
    try:
      generator = int(input("Insert a generator (public info): "))
      break
    except:
      print("Error: Generator must be an integer!")

  # Get the prime from the user, validating input!
  while True:
    try:
      prime = int(input("Insert a prime (public info): "))
      break
    except:
      print("Error: Prime must be an integer!")

  print("Generator: ", generator)
  print("Prime: ", prime)

  # Initialize Alice & Bob
  alice = Decrypter(generator, prime)
  bob = Encrypter(generator, prime)

  # Bob encrypts message, with Alice pub-key
  bob.encryptMsg(alice.getPubkey())

  # Alice decrypts message, then prints before exit
  decoded = alice.doDecrypt(bob.getEncrypted())

  print("Decoded/Decrypted message: ", decoded)


# -----------------------------------------------------------------
if __name__ == "__main__" and __package__ is None:
    main()
    __package__ = "expected.package.name"


