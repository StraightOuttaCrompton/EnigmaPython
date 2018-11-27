alphabet ="abcdefghijklmnopqrstuvwxyz"

def decrypt(message, platePermutations):
    global currentPlatePermutations
    currentPlatePermutations = platePermutations
    return encrypt(message)

def encodeBackwards(letter):
    plateNumber = len(plates) - 1
    for plate in reversed(plates):
        index = plate.index(letter) - currentPlatePermutations[plateNumber]
        if(index < 0):
            index = 26 + index
        letter = alphabet[index % 26]
        plateNumber -= 1

    return letter

def encodeForward(letter):
    for plateNumber, plate in enumerate(plates):
        index = alphabet.index(letter) + currentPlatePermutations[plateNumber]
        letter = plate[index % 26]
    return letter

def encrypt(message):
    global currentPlatePermutations
    global statingPlatePermutations
    statingPlatePermutations = list(currentPlatePermutations)
    output = ""
    for letter in message:
        letter = encodeForward(letter)
        letter = reflector(letter)
        letter = encodeBackwards(letter)
        currentPlatePermutations = rotateRotors(currentPlatePermutations)
        output = output + letter
    return(output)

def getPlatePermutations(numberOfPlates):
    output = []
    from random import randint
    for i in range(int(numberOfPlates)):
        output.append(randint(0,25))
    return output

def getPlates(numberOfPlates):
    output = []
    for i in range(int(numberOfPlates)):
        alphabet = getRandomisedAlphabet(i)
        output.append(alphabet)
    return output

def getRandomisedAlphabet(seed):
    output = ""
    import random
    randomArray = random.Random(seed).sample(range(26), 26)
    for index in randomArray:
        output = output + alphabet[index]
    return output

def reflector(letter):
    a = "abcdefghijklm"
    b = "nopqrstuvwxyz"
    if(a.find(letter) != -1):
        index = a.index(letter)
        return b[index]
    elif(b.find(letter) != -1):
        index = b.index(letter)
        return a[index]

def rotateRotors(rotorArray):
    rotorArray[0] += 1
    rotorArray[0] = rotorArray[0] % 26

    if(len(rotorArray) == 1):
        return rotorArray
    
    elif(rotorArray[0] == 0):
        rotorArray.pop(0)
        rotorArray = rotateRotors(rotorArray)
        rotorArray.insert(0, 0)
        return rotorArray
    else:
        return rotorArray
            
def main():
    global plates
    global currentPlatePermutations
    global statingPlatePermutations
    
    while(1):       
        command = input("Encrypt or Decrypt? ").lower()
        if(command == "encrypt" or command == "e"):
            numberOfRotors = input("Enter number of rotors ")
            plates = getPlates(numberOfRotors)
            currentPlatePermutations = getPlatePermutations(len(plates))
            statingPlatePermutations = list(currentPlatePermutations)
            messageToEncrypt = input("Enter message to encrypt ")
            print("encrypting...")
            print(encrypt(messageToEncrypt))
            print(statingPlatePermutations)
            
        if(command == "decrypt" or command == "d"):
            platePermutations = [int(x) for x in input("Enter plate permutations separated be spaces ").split()]
            messageToDecrypt = input("Enter message to decrypt ")
            print("decrypting...")
            print(decrypt(messageToDecrypt, platePermutations))
            
main()
