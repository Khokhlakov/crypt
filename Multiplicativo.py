import re
from Sistema import Sistema

class Multiplicativo(Sistema):
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

    def __init__(self, text = None, key = 1):
        super(Multiplicativo, self).__init__(text, key, "0a25")
        self.hasCipherOutput = False
        self.freqDict = {1:[], 2:[], 3:[], 4:[]}


    def setKey(self, key):

        self.key = key

        if type(key) == int:
            self.codeKey = key % 26
        else:
            key = re.sub(r'\W+', '', key)
            try:
                self.codeKey = int(key) % 26
            except ValueError:
                # key contiene characteres no numericos o vacio
                if len(key) > 0:
                    ordKey = ord(key[0].upper())
                    if ordKey < 65:
                        key = re.match(r'\d+', key).group()
                        self.codeKey = int(key) % 26
                    elif ordKey <= 90:
                        self.codeKey = ordKey - 65
                    else:
                        print("Clave invalida; reajustada a: 1")
                        self.codeKey = 1
                else:
                    print("Clave invalida; reajustada a: 1")
                    self.codeKey = 1

        # Comprobamos que codeKey es unidad
        if not (self.codeKey % 2 == 1 and self.codeKey != 13):
            print("Clave invalida; reajustada a: 1")
            self.codeKey = 1

    def encrypt(self, text=None):
        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: (x * self.codeKey) % 26, self.codeText)
        self.decodifyText()

        self.hasCipherOutput = False
        return self.getCipherString()

    def decrypt(self, text=None):
        self.hasCipherOutput = False

        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: (x * Multiplicativo.inverseKey[self.codeKey]) % 26, self.codeText)
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