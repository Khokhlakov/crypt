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

        if text != None:
            self.setText(text)
        if key != None:
            self.setKey(key)

    def setText(self, text):
        self.text = text
        self.depurateText()
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
        return cipherStr

    def depurateText(self):
        if self.codificacion == "0a25":
            upperText = self.text.upper()

            textList = []
            for i in upperText:
                if ord(i) <= 90 and ord(i) >= 65:
                    textList.append(i)

            self.cleanText = textList
            self.textSize = len(textList)
        else:
            pass

    def codifyText(self):
        if self.codificacion == "0a25":
            self.codeText = map(lambda x: ord(x)-65, self.cleanText)
        else:
            pass

    def decodifyText(self):
        if self.codificacion == "0a25":
            self.cipherText = map(lambda x: chr(x+65), self.cipherCodeText)
        else:
            pass

    def validateKey(self):
        pass

    def printCleanText(self):
        print(self.getCleanString())

    def printCipherText(self):
        print(self.getCipherString())
