import numpy as np
from sympy import Matrix
from Sistema import Sistema
from random import randint


class Hill(Sistema):
    coprimes256 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31,
                   33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61,
                   63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91,
                   93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117,
                   119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141,
                   143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165,
                   167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189,
                   191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213,
                   215, 217, 219, 221, 223, 225, 227, 229, 231, 233, 235, 237,
                   239, 241, 243, 245, 247, 249, 251, 253, 255]
    coprimes26 = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    coprimes96 = [1, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49, 
                  53, 55, 59, 61, 65, 67, 71, 73, 77, 79, 83, 85, 89, 91, 95]

    def __init__(self, text=None, key = np.array([1]), mode='i'):
        
        #self.keyLen = 5
        
        self.mode = mode
        self.keyLen = 5
        self.iv = np.array([randint(0,256) for x in range(self.keyLen)]).astype(int)
        self.text = text
        self.codeKey = None
        self.invKey = None
        self.codeMode = "Modified"
        super(Hill, self).__init__(text, key, "none")
    
    def setKeyLen(self, n):
        self.keyLen = n

    def setKey(self, key=None):
        if key != None:
            try:
                self.codeKey = key
                self.invKey = self.getInvKey()
                self.keyLen = len(self.codeKey)
            except:
                self.codeKey = self.getRandMat(self.keyLen)
                self.invKey = self.getInvKey()
        else:
            self.codeKey = self.getRandMat(self.keyLen)
            self.invKey = self.getInvKey()

    def setIV(self):
        self.iv = np.array([randint(0,256) for x in range(self.keyLen)]).astype(int)
    
    def getIVStr(self):
        return "".join(hex(x).split('x')[-1]+" " for x in self.iv)[:-1]

    def getKeyStr(self):
        myStr = ""
        for i in range(self.keyLen):
            for j in range(self.keyLen):
                myStr += f"{hex(self.codeKey[i,j]).split('x')[-1]:0>2} "
            myStr += "\n" 
        return myStr
    
    def setIVManual(self, myStr):
        out = [0]*self.keyLen
        inputList = myStr.strip().split()
        upperbound = min(len(inputList), self.keyLen)
        for i in range(upperbound):
            out[i] = int(inputList[i],16)%256

        self.iv = np.array(out)
    
    def setKeyManual(self, myStr):
        out = [0]*(self.keyLen**2)
        inputList = myStr.strip().split()
        upperbound = min(len(inputList), self.keyLen**2)
        for i in range(upperbound):
            out[i] = int(inputList[i],16)%256

        outArr = np.array(out).reshape((self.keyLen,self.keyLen))
        #try:
        self.invKey = self.getInvKey2(outArr)
        self.codeKey = outArr
        #except:
        #    pass


    def getRandMat(self, n):
        if self.mode == 'i':
            coprimesList = Hill.coprimes256
            mod = 256
        else:
            coprimesList = Hill.coprimes96
            mod = 96

        mat = np.diag(np.random.choice(coprimesList, size=n)).astype(int)

        for i in range(n-1):
            for j in range(i+1,n):
                mat[i,j] = np.random.randint(0, mod-1, dtype=int)
        for i in range(n-1,-1,-1):
            for j in range(i+1,n):
                rint = np.random.randint(0, mod-1, dtype=int)
                mat[j,:] = np.mod(mat[j,:] + mat[i,:]*rint, mod)

        return mat

    def getInvKey(self):
        if self.mode == 'i':
            return np.array(Matrix(self.codeKey).inv_mod(256)).astype(int)
        return np.array(Matrix(self.codeKey).inv_mod(96)).astype(int)

    def getInvKey2(self, arr):
        if self.mode == 'i':
            return np.array(Matrix(arr).inv_mod(256)).astype(int)
        return np.array(Matrix(self.codeKey).inv_mod(96)).astype(int)

    def encode(self, data):
        """ Encode function """

        layers = data.shape[-1]

        key = self.codeKey
        chunk = self.keyLen
        final = np.zeros(data.shape).astype(int)

        if self.mode == 'i':
            if self.codeMode == "Vanilla":
                if len(data.shape) < 3:
                    for i in range(0, data.shape[0], chunk):
                        for j in range(layers):
                            final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 2)
                else:
                    for i in range(0, data.shape[0], chunk):
                        for j in range(layers):
                            final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 256)
            else:
                p = 2863387
                count = 13
                prev2 = self.iv
                for i in range(0, data.shape[0], chunk):
                    for k in range(0, data.shape[1]):
                        for j in range(layers):
                            final[i:i+chunk,k,j] = np.mod(np.matmul(key, data[i:i+chunk,k,j]^prev2), 256).astype(int)
                            
                            prev2 = np.mod(final[i:i+chunk,k,j]+count, 256)
                            count = (count*13)%p
        else:
            pass
        return final


    def decode(self, data):
        """ Decode function """
        layers = data.shape[-1]

        key = self.invKey
        chunk = self.keyLen
        final = np.zeros(data.shape).astype(int)

        if self.mode == 'i':
            if self.codeMode == "Vanilla":
                if len(data.shape) < 3:
                    for i in range(0, data.shape[0], chunk):
                        for j in range(layers):
                            final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 2)
                else:
                    for i in range(0, data.shape[0], chunk):
                        for j in range(layers):
                            final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 256)
            else:
                p = 2863387
                count = 13
                prev2 = self.iv
                for i in range(0, data.shape[0], chunk):
                    for k in range(0, data.shape[1]):
                        for j in range(layers):
                            final[i:i+chunk,k,j] = np.mod(np.matmul(key, data[i:i+chunk,k,j]), 256).astype(int)^prev2.astype(int)
                            
                            prev2 = np.mod(data[i:i+chunk,k,j]+count, 256)
                            count = (count*13)%p
        else:
            pass
        return final



    # convert string to matrix of hex values with key size rows
    # This method adds padding
    def codestr(self, myStr):
        n = len(self.codeKey)
        textBytes = np.array([(ord(i)-32)%96 for i in myStr])
        residue = len(textBytes) % n
        if residue > 0:
            pad = n-residue
            newBytes = np.zeros(len(textBytes)+pad).astype(int)
            newBytes[:len(textBytes)] = textBytes[:len(textBytes)]
            newBytes[-1] = pad
        else:
            newBytes = np.zeros(len(textBytes)+n).astype(int)
            newBytes[:len(textBytes)] = textBytes[:len(textBytes)]
        return newBytes.reshape(int(len(newBytes)/n), n).T
    
    def codestrNoPadding(self, myStr):
        n = len(self.codeKey)
        newBytes = np.array([(ord(i)-32)%96 for i in myStr])
        return newBytes.reshape(int(len(newBytes)/n), n).T

    def encodeStr(self, myStr):
        myList = self.codestr(myStr)
        outputList = np.mod(np.matmul(self.codeKey, myList), 96)
        return ''.join(chr(i+32) for i in outputList.T.flatten())
    
    def decodeStr(self, myStr):
        myList = self.codestrNoPadding(myStr)
        outputList = np.mod(np.matmul(self.invKey, myList), 96).T.flatten()
        pad = outputList[-1]
        l = len(outputList)
        if pad < l:
            return ''.join(chr(i+32) for i in outputList[:l-pad])
        return ''.join(chr(i+32) for i in outputList[:l-len(self.codeKey)])
