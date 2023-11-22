class Sistema():
    def __init__(self, text = None, key = None, codificacion = "0a25"):
        self.codificacion = codificacion
        self.text = text
        self.key = key
        self.cleanText = None
        self.textSize = 0
        self.codeText = None
        self.cipherCodeText = None
        self.cipherText = None
        self.codeKey = None
        self.outputText = None

        if type(text) != type(None):
            self.setText(text)
        if type(key) != type(None):
            self.setKey(key)

    def setText(self, text):
        self.text = text
        self.depurateText()
        self.textSize = len(self.cleanText)
        self.codifyText()

    def setKey(self, key):
        pass

    def setCodificacion(self, string):
        self.codificacion = string
        self.setText(self.text)

    def getCleanString(self):
        cleanStr = ''.join([str(elem) for elem in self.cleanText])
        return cleanStr

    def getCipherString(self):
        cipherStr = ''.join([str(elem) for elem in self.cipherText])
        self.outputText = cipherStr
        return cipherStr
    
    def getInputKey(self):
        return self.key

    def depurateText(self):
        if self.codificacion == "0a25":
            upperText = self.text.upper()

            textList = []
            for i in upperText:
                if ord(i) <= 90 and ord(i) >= 65:
                    textList.append(i)

            self.cleanText = textList

        elif self.codificacion == "noSpaces":
            self.cleanText = list(''.join(self.text.split()))
        elif self.codificacion == "0a95":
            upperText = self.text

            textList = []
            for i in upperText:
                if ord(i) <= 126 and ord(i) >= 32:
                    textList.append(i)

            self.cleanText = textList
        else:
            self.cleanText = self.text

    def codifyText(self):
        if self.codificacion == "0a25":
            self.codeText = [ord(x)-65 for x in self.cleanText]
        elif self.codificacion == "0a95":
            self.codeText = [ord(x)-32 for x in self.cleanText]
        elif self.codificacion == "noSpaces":
            self.codeText = self.cleanText
        else:
            pass

    def decodifyText(self):
        if self.codificacion == "0a25":
            self.cipherText = [chr(x+65) for x in self.cipherCodeText]
        elif self.codificacion == "0a95":
            self.cipherText = [chr(x+32) for x in self.cipherCodeText]
        elif self.codificacion == "noSpaces":
            self.cipherText = self.cipherCodeText
        else:
            pass

    def validateKey(self):
        pass

    def printCleanText(self):
        print(self.getCleanString())

    def printCipherText(self):
        print(self.getCipherString())
