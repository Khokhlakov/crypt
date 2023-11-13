import numpy as np
from sympy import Matrix
from Sistema import Sistema


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

    def __init__(self, text=None, key = np.array([1]), mode='i'):
        
        #self.keyLen = 5
        
        self.mode = mode
        self.keyLen = len(key)
        self.text = text
        self.codeKey = None
        self.invKey = None
        if mode == 'i':
            super(Hill, self).__init__(text, key, "none")
        else:
            super(Hill, self).__init__(text, key, "0a25")
    
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


    def getRandMat(self, n):
        if self.mode == 'i':
            coprimesList = Hill.coprimes256
            mod = 256
        else:
            coprimesList = Hill.coprimes26
            mod = 26

        mat = np.diag(np.random.choice(coprimesList, size=n))

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
            return np.array(Matrix(self.codeKey).inv_mod(256))
        return np.array(Matrix(self.codeKey).inv_mod(26))

    def encode(self, data):
        """ Encode function """

        layers = data.shape[-1]

        key = self.codeKey
        chunk = self.keyLen
        final = np.zeros(data.shape)

        if self.mode == 'i':
            if len(data.shape) < 3:
                for i in range(0, data.shape[0], chunk):
                    for j in range(layers):
                        final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 2)
            else:
                for i in range(0, data.shape[0], chunk):
                    for j in range(layers):
                        final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 256)
        else:
            for i in range(0, data.shape[0], chunk):
                final[i:i + chunk,:] = np.mod(np.matmul(key, data[i:i + chunk,:]), 26)
        return final


    def decode(self, data):
        """ Decode function """
        layers = data.shape[-1]

        key = self.invKey
        chunk = self.keyLen
        final = np.zeros(data.shape)

        if self.mode == 'i':
            if len(data.shape) < 3:
                for i in range(0, data.shape[0], chunk):
                    for j in range(layers):
                        final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 2)
            else:
                for i in range(0, data.shape[0], chunk):
                    for j in range(layers):
                        final[i:i + chunk,:,j] = np.mod(np.matmul(key, data[i:i + chunk,:,j]), 256)
        else:
            for i in range(0, data.shape[0], chunk):
                final[i:i + chunk,:] = np.mod(np.matmul(key, data[i:i + chunk,:]), 26)
        return final