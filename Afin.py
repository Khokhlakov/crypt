import re
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

    def __init__(self, text = None, key = [1,0]):
        super(Afin, self).__init__(text, key, "0a25")

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
        return self.getCipherString()

    def decrypt(self, text=None):
        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: ((x - self.codeKey[1]) * Afin.inverseKey[self.codeKey[0]]) % 26, self.codeText)
        self.decodifyText()
        return self.getCipherString()