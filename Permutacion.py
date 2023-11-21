from random import randint, shuffle
from Sistema import Sistema
from itertools import permutations
import re

class Permutacion(Sistema):
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
    
    def __init__(self, text = None, key = [0]):
        super(Permutacion, self).__init__(text, key, "noSpaces")

    def setKey(self, key):
        self.key = key

        # input is list
        if type(key) == list or type(key) == tuple:
            self.key = key
            self.codeKey = key

        # input is string
        else:
            if len(self.key) >= 8:
                self.key = self.key[:8]
            key = re.sub('[^0-9A-Za-z,]+', '', self.key)
            keyList = key.split(",")
            if len(keyList) == 1:
                keyList = list(keyList[0])
                indexedKey = list(zip(keyList, range(len(keyList))))
                indexedKey.sort(key = lambda x: ord(x[0]))
                permList = [None]*len(keyList)
                for i in range(len(indexedKey)):
                    permList[indexedKey[i][1]] = i
                self.codeKey = permList
            else:
                keyList = re.sub('[^0-9,]+', '', self.key).strip(",").split(",")
                if len(keyList) > 1:
                    self.codeKey = [int(x) for x in keyList]
                else:
                    self.codeKey = [0]

        self.inverseKey = [None]*len(self.codeKey)
        for i in range(len(self.codeKey)):
            self.inverseKey[self.codeKey[i]] = i

    def encrypt(self, text=None):
        if text != None:
            self.setText(text)
        
        self.cipherCodeText = []
        for i in self.inverseKey:
            index = i
            while index < self.textSize:
                self.cipherCodeText.append(self.codeText[index])
                index += len(self.codeKey)

        self.decodifyText()
        return self.getCipherString()

    def decrypt(self, text=None):
        if text != None:
            self.setText(text)

        n = self.textSize
        m = len(self.codeKey)
        p = n // m
        r = n % m

        newCleanText = [x for x in self.cleanText]

        columnHeight = [p]*m
        for i in range(r):
            columnHeight[i] += 1

        for i in range(m):
            if columnHeight[self.inverseKey[i]] != p+1:
                newCleanText.insert((i+1)*(p+1)-1, " ")
        
        self.cipherCodeText = []
        for i in range(p+1):
            for j in self.codeKey:
                nextChar = newCleanText[j*(p+1)+i]
                if nextChar != " ":
                    self.cipherCodeText.append(nextChar)

        self.decodifyText()
        return self.getCipherString()

    def generateKey(self):
        temp = list(range(randint(3, 9)))
        shuffle(temp)
        return temp

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

    # num: number of keys
    def getBestKeys(self, string, num=2):
        system = Permutacion(text=string)
        perms = [list(permutations(range(i))) for i in range(2,9)]

        bestChoice = []

        for permsOfLenN in perms:
            for perm in permsOfLenN:
                system.setKey(perm)
                system.decrypt()
                outputString = system.getCipherString()
                myString = outputString.upper()
                regex = re.compile('[^A-Z]')
                myString = regex.sub('', myString)
                freqDict = self.getFreqOfBigramsOnStr(myString)
        
                # assign score to decryption
                sum = 0
                for bigram in freqDict.keys():
                    if bigram in Permutacion.commonBigrams.keys():
                        sum += Permutacion.commonBigrams[bigram]*freqDict[bigram]
                
                # (key, deciphered text, score)
                bestChoice.append((perm, outputString, sum))

        option = sorted(bestChoice, key=lambda x: x[2], reverse=True)
        
        return option[:num]