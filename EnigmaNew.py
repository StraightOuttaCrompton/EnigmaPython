#Like the original enigma machines, this implementation only encrypts the alphabet and no other characters.
from random import randint

alphabet ="abcdefghijklmnopqrstuvwxyz"
alphabetLength = 26

#hard code plates in, set as [] to randomise plates
hardCodePlates = ["ekmflgdqvzntowyhxuspaibrcj", "ajdksiruxblhwtmcqgznpyfvoe", "bdfhjlcprtxvznyeiwgakmusqo"]

def encrypt(message):
    global currentPlatePermutations
    output = ""
    for letter in message:
        if(letter != " "):
            letter = encodeForward(letter)
            letter = reflector(letter)
            letter = encodeBackwards(letter)
            currentPlatePermutations = rotateRotors(currentPlatePermutations)
        output += letter
    return(output)

def decrypt(message, platePermutations):
    global currentPlatePermutations
    currentPlatePermutations = platePermutations
    return encrypt(message)

def encodeForward(letter):
    for plateNumber, plate in enumerate(plates):
        index = alphabet.index(letter) + currentPlatePermutations[plateNumber]
        letter = plate[index % alphabetLength]
    return letter

def encodeBackwards(letter):
    plateNumber = len(plates) - 1
    for plate in reversed(plates):
        index = plate.index(letter) - currentPlatePermutations[plateNumber]
        if(index < 0):
            index = alphabetLength + index
        letter = alphabet[index % alphabetLength]
        plateNumber -= 1

    return letter

def reflector(letter):
    a = "abcdefghijklm"
    b = "nopqrstuvwxyz"
    if(a.find(letter) != -1):
        index = a.index(letter)
        return b[index]
    elif(b.find(letter) != -1):
        index = b.index(letter)
        return a[index]

def getRandomPlatePermutations(numberOfPlates):
    output = []
    for i in range(int(numberOfPlates)):
        output.append(randint(0, alphabetLength - 1))
    return output

def getRandomPlates(numberOfPlates):
    output = []
    for i in range(int(numberOfPlates)):
        alphabet = getRandomisedAlphabet(i)
        output.append(alphabet)
    return output

def getRandomisedAlphabet(seed):
    output = ""
    import random
    randomArray = random.Random(seed).sample(range(alphabetLength), alphabetLength)
    for index in randomArray:
        output = output + alphabet[index]
    return output

def rotateRotors(rotorArray):
    rotorArray[0] += 1
    rotorArray[0] = rotorArray[0] % alphabetLength

    if(len(rotorArray) == 1):
        return rotorArray
    
    elif(rotorArray[0] == 0):
        rotorArray.pop(0)
        rotorArray = rotateRotors(rotorArray)
        rotorArray.insert(0, 0)
        return rotorArray
    else:
        return rotorArray

def enterNumberOfRotors ():
    try:
        numberOfRotors = int(input("Enter number of rotors "))
        
    except ValueError:
        numberOfRotors = enterNumberOfRotors()
    return numberOfRotors
            
def main():
    global plates
    global currentPlatePermutations
    global statingPlatePermutations

    plates = hardCodePlates
    if(hardCodePlates == []):
        numberOfRotors = enterNumberOfRotors()
        plates = getRandomPlates(numberOfRotors)
        
    currentPlatePermutations = getRandomPlatePermutations(len(plates))
        
    while(1):       
        command = input("Encrypt or Decrypt? ").lower()
        if(command == "encrypt" or command == "e"):
            
            statingPlatePermutations = list(currentPlatePermutations)
            messageToEncrypt = input("Enter message to encrypt ")
            print("encrypting...")
            print(encrypt(messageToEncrypt))
    
            print(statingPlatePermutations)
            
        if(command == "decrypt" or command == "d"):
            platePermutations = [int(x) for x in input("Enter plate permutations separated by spaces ").split()]
            messageToDecrypt = input("Enter message to decrypt ")
            print("decrypting...")
            print(decrypt(messageToDecrypt, platePermutations))
            
main()
