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

    def __init__(self, text = None, key = [1,0]):
        super(Afin, self).__init__(text, key, "0a25")
        self.hasCipherOutput = False
        self.freqDict = {1:[], 2:[], 3:[], 4:[]}


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