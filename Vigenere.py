import re
from Sistema import Sistema

class Vigenere(Sistema):
    def __init__(self, text = None, key = [0]):
        super(Vigenere, self).__init__(text, key, "0a25")

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