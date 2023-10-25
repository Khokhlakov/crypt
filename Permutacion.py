from Sistema import Sistema

class Permutacion(Sistema):
    def __init__(self, text = None, key = [0]):
        super(Permutacion, self).__init__(text, key, "noSpaces")

    def setKey(self, key):
        if type(key) == list:
            self.key = key
            self.codeKey = key

            self.inverseKey = [None]*len(self.key)
            for i in range(len(self.key)):
                self.inverseKey[self.codeKey[i]] = i
        else:
            pass

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


