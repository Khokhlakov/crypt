import re
from random import sample, randint
from itertools import combinations

class Substitution():
    alphabet = {"A", "B", "C", "D", "E", "F", "G", "H", "I",
                "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z"}
    alphabetList = ["A", "B", "C", "D", "E", "F", "G", "H", "I",
                    "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                    "S", "T", "U", "V", "W", "X", "Y", "Z"]

    commonBigrams = {"TH":0.0356,"HE":0.0307,"IN":0.0243,"ER":0.0205,
                     "AN":0.0199,"RE":0.0185,"ON":0.0176,"AT":0.0149,
                     "EN":0.0145,"ND":0.0135,"TI":0.0134,"ES":0.0134,
                     "OR":0.0128,"TE":0.0120,"OF":0.0117,"ED":0.0117,
                     "IS":0.0113,"IT":0.0112,"AL":0.0109,"AR":0.0107,
                     "ST":0.0105,"TO":0.0104,"NT":0.0104,"NG":0.0095,
                     "SE":0.0093,"HA":0.0093,"AS":0.0087,"OU":0.0087,
                     "IO":0.0083,"LE":0.0083,"VE":0.0083,"CO":0.0079,
                     "ME":0.0079,"DE":0.0076,"HI":0.0076,"RI":0.0073,
                     "RO":0.0073,"IC":0.0070,"NE":0.0069,"EA":0.0069,
                     "RA":0.0069,"CE":0.0065,"LI":0.0062,"CH":0.0060,
                     "LL":0.0058,"BE":0.0058,"MA":0.0057,"SI":0.0055,
                     "OM":0.0055,"UR":0.0054}
    
    def __init__(self, text="", key="A"):
        self.key = ""
        self.prevKey = ""
        self.doMap = {}
        self.undoMap = {}
        self.setKey(key)
        self.text = ""
        self.cleanText = ""
        self.setText(text)
    
    def setKey(self, key):

        # Set key as string of less than 9 upper case non repeating letters
        newString = ""
        alreadyUsedLetters = set({})
        for char in key.upper():
            if ord(char) >= 65 and ord(char) <= 90 and char not in alreadyUsedLetters:
                alreadyUsedLetters.add(char)
                newString += char

        if len(newString) > 7:
            newString = newString[:7]
        if len(newString) == 0:
            newString = "A"
        self.key = newString

        # Check if key changed
        # If it did, update dictionaries
        if self.key != self.prevKey:
            self.prevKey = self.key

            # Generate encryption and decryption maps
            self.doMap = {}
            self.undoMap = {}
            keyList = list(self.key)
            keySet = set(keyList)
            remainingLetters = Substitution.alphabet - keySet
            remainingLettersList = list(sorted(remainingLetters))
            finalList = keyList + remainingLettersList
            for i in range(len(finalList)):
                self.doMap[chr(i+65)] = finalList[i]
                self.undoMap[finalList[i]] = chr(i+65)
    
    def setText(self, text):
        self.text = text
        regex = re.compile('[^A-Z]')
        self.cleanText = regex.sub('', self.text.upper())
    
    def encrypt(self):
        newStr = ""
        for char in self.cleanText:
            newStr += self.doMap[char]
        return newStr
    
    def decrypt(self):
        newStr = ""
        for char in self.cleanText:
            newStr += self.undoMap[char]
        return newStr

    def setRandomKey(self):
        newKey = ""
        keyList = sample(Substitution.alphabetList, randint(2, 7))
        for char in keyList:
            newKey += char
        self.key = newKey

        # Check if key changed
        # If it did, update dictionaries
        if self.key != self.prevKey:
            self.prevKey = self.key

            # Generate encryption and decryption maps
            self.doMap = {}
            self.undoMap = {}
            keyList = list(self.key)
            keySet = set(keyList)
            remainingLetters = Substitution.alphabet - keySet
            remainingLettersList = list(sorted(remainingLetters))
            finalList = keyList + remainingLettersList
            for i in range(len(finalList)):
                self.doMap[chr(i+65)] = finalList[i]
                self.undoMap[finalList[i]] = chr(i+65)
    
    ### Analisis
    def getFreqOfBigramsOnStr(self, string):
        tempDict = {}
        n = len(string)

        for i in range(n-1):
            word = string[i:i+2]
            if word in tempDict.keys():
                tempDict[word] += 1
            else:
                tempDict[word] = 1
        
        # normalized frequencies
        freqDict = {key:value/(n-1) for (key,value) in tempDict.items()}
        return freqDict

    def getBestKeys(self, string):
        system = Substitution(text=string)
        baseStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        combs = [''.join(l) for i in range(7) for l in combinations(baseStr, i+1)]

        bestChoice = []

        for comb in combs:
            system.setKey(comb)
            outputString = system.decrypt()
            freqDict = self.getFreqOfBigramsOnStr(outputString)
    
            # Assign score to decryption
            sum = 0
            for bigram in freqDict.keys():
                if bigram in Substitution.commonBigrams.keys():
                    sum += Substitution.commonBigrams[bigram]*freqDict[bigram]
            
            # (key, deciphered text, score)
            bestChoice.append((comb, outputString, sum))

        option = sorted(bestChoice, key=lambda x: x[2], reverse=True)
        
        return option

        