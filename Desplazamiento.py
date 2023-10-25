import re
from Sistema import Sistema

class Desplazamiento(Sistema):
    def __init__(self, text = None, key = 0):
        super(Desplazamiento, self).__init__(text, key, "0a25")

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
                        print("Clave invalida; reajustada a: 0")
                        self.codeKey = 0
                else:
                    print("Clave invalida; reajustada a: 0")
                    self.codeKey = 0

    def encrypt(self, text=None):
        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: (x + self.codeKey) % 26, self.codeText)
        self.decodifyText()
        return self.getCipherString()

    def decrypt(self, text=None):
        if text != None:
            self.setText(text)
        self.cipherCodeText = map(lambda x: (x - self.codeKey) % 26, self.codeText)
        self.decodifyText()
        return self.getCipherString()