import re
from random import choice, randint
from Sistema import Sistema

class Afin(Sistema):
    inverseKey = {1:1,
                  3:9,
                  5:21,
                  7:15,
                  9:3,
                  11:19,
                  15:7,
                  17:23,
                  19:11,
                  21:5,
                  23:17,
                  25:25}
    
    coprimes26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

    squaredFrequencySum = {"English":0.06553858549999998,
                            "Spanish":0.07483239020000003,
                            "German":0.07365403820000002,
                            "Italian":0.0749886659,
                            "Portuguese":0.07807021811699999,
                            "French":0.07828237919999999}
    
    kappa = {"English":0.0667,
              "Spanish":0.0766,
              "German":0.0767,
              "Italian":0.0733,
              "Portuguese":0.0745,
              "French":0.0746}

    characterFrequency = {"English":{
                                      'A':8.167, 'B':1.492, 'C':2.782, 'D':4.253, 'E':12.702,
                                      'F':2.228, 'G':2.015, 'H':6.094, 'I':6.996, 'J':0.153,
                                      'K':0.772, 'L':4.025, 'M':2.406, 'N':6.749, 'O':7.507,
                                      'P':1.929, 'Q':0.095, 'R':5.987, 'S':6.327, 'T':9.056,
                                      'U':2.758, 'V':0.978, 'W':2.360, 'X':0.150, 'Y':1.974,
                                      'Z':0.074
                                    },
                           "Spanish":{
                                      'A':12.09, 'B':1.21, 'C':4.20, 'D':4.65, 'E':13.89,
                                      'F':0.642, 'G':1.11, 'H':1.13, 'I':6.38, 'J':0.461,
                                      'K':0.038, 'L':5.19, 'M':2.86, 'N':7.23, 'O':9.58,
                                      'P':2.74, 'Q':1.37, 'R':6.14, 'S':7.43, 'T':4.49,
                                      'U':4.53, 'V':1.05, 'W':0.011, 'X':0.124, 'Y':1.14,
                                      'Z':0.324
                                     },
                           "German":{
                                      'A':6.506, 'B':2.566, 'C':2.837, 'D':5.414, 'E':16.693,
                                      'F':2.044, 'G':3.647, 'H':4.064, 'I':7.812, 'J':0.191,
                                      'K':1.879, 'L':2.825, 'M':3.005, 'N':9.905, 'O':2.285,
                                      'P':0.944, 'Q':0.055, 'R':6.539, 'S':6.765, 'T':6.742,
                                      'U':3.703, 'V':1.069, 'W':1.396, 'X':0.022, 'Y':0.032,
                                      'Z':1.002
                                    },
                           "Italian":{
                                      'A':11.30, 'B':0.975, 'C':4.35, 'D':3.80, 'E':11.24,
                                      'F':1.09, 'G':1.73, 'H':1.02, 'I':11.57, 'J':0.035,
                                      'K':0.078, 'L':6.40, 'M':2.66, 'N':7.29, 'O':9.11,
                                      'P':2.89, 'Q':0.391, 'R':6.68, 'S':5.11, 'T':6.76,
                                      'U':3.18, 'V':1.52, 'W':0.00, 'X':0.024, 'Y':0.048,
                                      'Z':0.958
                                     },
                           "Portuguese":{
                                          'A':13.89, 'B':0.980, 'C':4.18, 'D':5.24, 'E':12.72,
                                          'F':1.01, 'G':1.17, 'H':0.905, 'I':6.70, 'J':0.317,
                                          'K':0.0174, 'L':2.76, 'M':4.54, 'N':5.37, 'O':10.90,
                                          'P':2.74, 'Q':1.06, 'R':6.67, 'S':7.90, 'T':4.63,
                                          'U':4.05, 'V':1.55, 'W':0.0104, 'X':0.272, 'Y':0.0165,
                                          'Z':0.400
                                        },
                           "French":{
                                      'A':8.11, 'B':0.903, 'C':3.49, 'D':4.27, 'E':17.22,
                                      'F':1.14, 'G':1.09, 'H':0.769, 'I':7.44, 'J':0.339,
                                      'K':0.097, 'L':5.53, 'M':2.89, 'N':7.46, 'O':5.38,
                                      'P':3.02, 'Q':0.999, 'R':7.05, 'S':8.04, 'T':6.99,
                                      'U':5.65, 'V':1.30, 'W':0.039, 'X':0.435, 'Y':0.271,
                                      'Z':0.098
                                    }}

    def __init__(self, text = None, key = [1,0]):
        super(Afin, self).__init__(text, key, "0a25")
        self.hasCipherOutput = False
        self.freqDict = {1:[], 2:[], 3:[], 4:[]}
        self.lang = 'English'


    def setKey(self, key):
        self.codeKey = [1,0]
        if type(key) == list:
            self.codeKey[0] = key[0] % 26
            self.codeKey[1] = key[1] % 26
        else:
            keyList = key.split(",", 1)
            if len(keyList) > 1:
                key1 = re.sub(r'\W+', '', keyList[0])
                key2 = re.sub(r'\W+', '', keyList[1])

                try:
                    self.codeKey[0] = int(key1) % 26
                except ValueError:
                    if len(key1) > 0:
                        ordKey = ord(key1[0].upper())
                        if ordKey < 65:
                            key1 = re.match(r'\d+', key1).group()
                            self.codeKey[0] = int(key1) % 26
                        elif ordKey <= 90:
                            self.codeKey[0] = ordKey - 65
                        else:
                            print("Clave invalida; reajustada a: (1,{})".format(key2))
                            self.codeKey[0] = 1
                    else:
                        print("Clave invalida; reajustada a: (1,{})".format(key2))
                        self.codeKey[0] = 1

                try:
                    self.codeKey[1] = int(key2) % 26
                except ValueError:
                    if len(key2) > 0:
                        ordKey = ord(key2[0].upper())
                        if ordKey < 65:
                            key2 = re.match(r'\d+', key2).group()
                            self.codeKey[1] = int(key2) % 26
                        elif ordKey <= 90:
                            self.codeKey[1] = ordKey - 65
                        else:
                            print("Clave invalida; reajustada a: ({},0)".format(self.codeKey[0]))
                            self.codeKey[1] = 0
                    else:
                        print("Clave invalida; reajustada a: ({},0)".format(self.codeKey[0]))
                        self.codeKey[1] = 0

            else:
                print("Clave invalida; reajustada a: (1,0)")
                key1 = 1
                key2 = 0

        if not (self.codeKey[0] % 2 == 1 and self.codeKey[0] != 13):
            print("Clave invalida; reajustada a: (1,{})".format(self.codeKey[1]))
            self.codeKey[0] = 1

    def encrypt(self, text=None):
        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: (x * self.codeKey[0] + self.codeKey[1]) % 26, self.codeText)
        self.decodifyText()

        self.hasCipherOutput = True
        return self.getCipherString()

    def decrypt(self, text=None):
        self.hasCipherOutput = False

        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: ((x - self.codeKey[1]) * Afin.inverseKey[self.codeKey[0]]) % 26, self.codeText)
        self.decodifyText()
        return self.getCipherString()
    
    def getFreq(self):
        if self.hasCipherOutput:
            tempDict = {1:{}, 2:{}, 3:{}, 4:{}}
            n = len(self.outputText)

            for k in range(1,5):
                for i in range(n+1-k):
                    word = self.outputText[i:i+k]
                    if word in tempDict[k].keys():
                        tempDict[k][word] += 1
                    else:
                        tempDict[k][word] = 1

            freqDict = {1: sorted({key:round(100*value/n, 2) for (key,value) in tempDict[1].items()}.items(), key=lambda x: x[1], reverse=True),
                        2: sorted({key:round(100*value/(n-1), 2) for (key,value) in tempDict[2].items()}.items(), key=lambda x: x[1], reverse=True),
                        3: sorted({key:round(100*value/(n-2), 2) for (key,value) in tempDict[3].items()}.items(), key=lambda x: x[1], reverse=True),
                        4: sorted({key:round(100*value/(n-3), 2) for (key,value) in tempDict[4].items()}.items(), key=lambda x: x[1], reverse=True)}
            self.freqDict = freqDict

    def generateKey(self):
        return [choice(Afin.coprimes26), randint(0,25)]
    
    ### Analisis
    def getFreqOfStr(self, string):
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

    # num: number of recommended keys
    def getBestKeys(self, string, num=2):
        freqDict = self.getFreqOfStr(string)
        bestChoice = {}
        for i in Afin.coprimes26:
            for j in range(26):
                sum = 0
                for key in freqDict.keys():
                    sum += Afin.characterFrequency[self.lang][chr((((ord(key)-65-j)*Afin.inverseKey[i])%26)+65)]*freqDict[key]
                bestChoice[str(i)+","+str(j)] = sum/100
        
        option1 = sorted(bestChoice.items(), key=lambda x: x[1], reverse=True)
        option2 = sorted(bestChoice.items(), key=lambda x: abs(x[1]-Afin.squaredFrequencySum[self.lang]))

        if num > len(option1):
            num = len(option1)

        return (option1[:num], option2[:num])