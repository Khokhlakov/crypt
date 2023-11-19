import re
from random  import randint
from Sistema import Sistema

class Vigenere(Sistema):
    squaredFrequencySum = {"english":0.06553858549999998,
                            "spanish":0.07483239020000003,
                            "german":0.07365403820000002,
                            "italian":0.0749886659,
                            "portuguese":0.07807021811699999,
                            "french":0.07828237919999999}
    
    kappa = {"english":0.0667,
              "spanish":0.0766,
              "german":0.0767,
              "italian":0.0733,
              "portuguese":0.0745,
              "french":0.0746}

    characterFrequency = {"english":{
                                      'A':8.167, 'B':1.492, 'C':2.782, 'D':4.253, 'E':12.702,
                                      'F':2.228, 'G':2.015, 'H':6.094, 'I':6.996, 'J':0.153,
                                      'K':0.772, 'L':4.025, 'M':2.406, 'N':6.749, 'O':7.507,
                                      'P':1.929, 'Q':0.095, 'R':5.987, 'S':6.327, 'T':9.056,
                                      'U':2.758, 'V':0.978, 'W':2.360, 'X':0.150, 'Y':1.974,
                                      'Z':0.074
                                    },
                           "spanish":{
                                      'A':12.09, 'B':1.21, 'C':4.20, 'D':4.65, 'E':13.89,
                                      'F':0.642, 'G':1.11, 'H':1.13, 'I':6.38, 'J':0.461,
                                      'K':0.038, 'L':5.19, 'M':2.86, 'N':7.23, 'O':9.58,
                                      'P':2.74, 'Q':1.37, 'R':6.14, 'S':7.43, 'T':4.49,
                                      'U':4.53, 'V':1.05, 'W':0.011, 'X':0.124, 'Y':1.14,
                                      'Z':0.324
                                     },
                           "german":{
                                      'A':6.506, 'B':2.566, 'C':2.837, 'D':5.414, 'E':16.693,
                                      'F':2.044, 'G':3.647, 'H':4.064, 'I':7.812, 'J':0.191,
                                      'K':1.879, 'L':2.825, 'M':3.005, 'N':9.905, 'O':2.285,
                                      'P':0.944, 'Q':0.055, 'R':6.539, 'S':6.765, 'T':6.742,
                                      'U':3.703, 'V':1.069, 'W':1.396, 'X':0.022, 'Y':0.032,
                                      'Z':1.002
                                    },
                           "italian":{
                                      'A':11.30, 'B':0.975, 'C':4.35, 'D':3.80, 'E':11.24,
                                      'F':1.09, 'G':1.73, 'H':1.02, 'I':11.57, 'J':0.035,
                                      'K':0.078, 'L':6.40, 'M':2.66, 'N':7.29, 'O':9.11,
                                      'P':2.89, 'Q':0.391, 'R':6.68, 'S':5.11, 'T':6.76,
                                      'U':3.18, 'V':1.52, 'W':0.00, 'X':0.024, 'Y':0.048,
                                      'Z':0.958
                                     },
                           "portuguese":{
                                          'A':13.89, 'B':0.980, 'C':4.18, 'D':5.24, 'E':12.72,
                                          'F':1.01, 'G':1.17, 'H':0.905, 'I':6.70, 'J':0.317,
                                          'K':0.0174, 'L':2.76, 'M':4.54, 'N':5.37, 'O':10.90,
                                          'P':2.74, 'Q':1.06, 'R':6.67, 'S':7.90, 'T':4.63,
                                          'U':4.05, 'V':1.55, 'W':0.0104, 'X':0.272, 'Y':0.0165,
                                          'Z':0.400
                                        },
                           "french":{
                                      'A':8.11, 'B':0.903, 'C':3.49, 'D':4.27, 'E':17.22,
                                      'F':1.14, 'G':1.09, 'H':0.769, 'I':7.44, 'J':0.339,
                                      'K':0.097, 'L':5.53, 'M':2.89, 'N':7.46, 'O':5.38,
                                      'P':3.02, 'Q':0.999, 'R':7.05, 'S':8.04, 'T':6.99,
                                      'U':5.65, 'V':1.30, 'W':0.039, 'X':0.435, 'Y':0.271,
                                      'Z':0.098
                                    }}
    
    def __init__(self, text = None, key = [0]):
        super(Vigenere, self).__init__(text, key, "0a25")
        self.lang = 'english'

    def setKey(self, key):
        if type(key) == list:
            self.key = key
            self.codeKey = [x % 26 for x in self.key]
        else:
            self.key = "".join(re.findall("[A-Z]+", key.upper()))
            if len(self.key) > 0:
                self.codeKey = [ord(x) - 65 for x in self.key]
            else:
                self.codeKey = [0]
                print("Clave invalida; reajustada a: \"A\"")

    def encrypt(self, text=None):
        if text != None:
            self.setText(text)
        
        self.cipherCodeText = [x for x in self.codeText]
        lenKey = len(self.codeKey)
        for i in range(len(self.codeText)):
            self.cipherCodeText[i] = (self.cipherCodeText[i] + self.codeKey[i % lenKey]) % 26

        self.decodifyText()
        return self.getCipherString()

    def decrypt(self, text=None):
        if text != None:
            self.setText(text)

        self.cipherCodeText = [x for x in self.codeText]
        lenKey = len(self.codeKey)
        for i in range(len(self.codeText)):
            self.cipherCodeText[i] = (self.cipherCodeText[i] - self.codeKey[i % lenKey]) % 26

        self.decodifyText()
        return self.getCipherString()

    def generateKey(self):
        n = 3
        if type(self.cleanText) != type(None):
            n = len(self.cleanText)
        return [randint(0,25) for x in range(randint(3,n))]
    
    def getFreqIndex(self, string):
        finDict = {}

        for i in range(3, 16):
            text = string[0::i]
            tempDict = {}
            n = len(text)

            for letter in text:
                if letter in tempDict.keys():
                    tempDict[letter] += 1
                else:
                    tempDict[letter] = 1

            sum = 0
            for item in tempDict.items():
                sum += item[1]*(item[1]-1)

            finDict[i] = sum/(n*(n-1))
        return sorted(finDict.items(), key=lambda x: abs(x[1]-Vigenere.kappa[self.lang]))

    def getFreq(string):
        tempDict = {}
        n = len(string)

        for i in range(n):
            word = string[i]
            if word in tempDict.keys():
                tempDict[word] += 1
            else:
                tempDict[word] = 1

        # normalized frequencies
        freqDict = {key:value/n for (key,value) in tempDict.items()}
        return freqDict
    
    #num: Number of recommen ded keys
    def getBestKeys(self, string, num=2):
        freqIndDect = self.getFreqIndex(string)
        n = len(string)

        if num > len(freqIndDect):
            num = len(freqIndDect)

        keys = []
        for keyLenIndex in range(num):
            # m: key length
            m = freqIndDect[keyLenIndex][0]

            keyOption1 = ""
            keyOption2 = ""
            for k in range(m):
                freqDict = self.getFreq(string[k::m])
                bestChoice = {}
                for i in range(26):
                    sum = 0
                    for key in freqDict.keys():
                        sum += Vigenere.characterFrequency[self.lang][chr(((ord(key)-65-i)%26)+65)]*freqDict[key]
                    bestChoice[chr(i+65)] = sum/100
                
                keyOption1 += max(bestChoice.items(), key=lambda x: x[1])[0]
                keyOption2 += min(bestChoice.items(), key=lambda x: abs(x[1]-Vigenere.squaredFrequencySum[self.lang]))[0]
            
            keys.append((keyOption1, keyOption2))
        
        return keys