from random import randint
import numpy as np
import imageio.v3 as iio
import os
import sys

class SimplerDES():
    IP = [1,5,2,0,3,7,4,6]
    IPinv = [3,0,2,4,6,1,7,5]
    S_0 = [
                [ [0, 1], [0, 0], [1, 1], [1, 0] ],
                [ [1, 1], [1, 0], [0, 1], [0, 0] ],
                [ [0, 0], [1, 0], [0, 1], [1, 1] ],
                [ [1, 1], [0, 1], [1, 1], [1, 0] ],
            ]
    S_1 = [
                [ [0, 0], [0, 1], [1, 0], [1, 1] ],
                [ [1, 0], [0, 0], [0, 1], [1, 1] ],
                [ [1, 1], [0, 0], [0, 1], [0, 0] ],
                [ [1, 0], [0, 1], [0, 0], [1, 1] ],
            ]
    def __init__ (self):
        self.key = [0,1,1,1,1,1,1,1,0,1]
        self.key1 = None
        self.key2 = None
        self.iv = 17
        self.doMap = {}
        self.undoMap = {}

    def generateKeys(self):
        key = self.key
        prekey = [key[2],
                  key[4],
                  key[1],
                  key[6],
                  key[3],
                  key[9],
                  key[0],
                  key[8],
                  key[7],
                  key[5]]

        prekey11 = [prekey[1],
                    prekey[2],
                    prekey[3],
                    prekey[4],
                    prekey[0],
                    prekey[6],
                    prekey[7],
                    prekey[8],
                    prekey[9],
                    prekey[5]]

        prekey12 = [prekey[3],
                    prekey[4],
                    prekey[0],
                    prekey[1],
                    prekey[2],
                    prekey[8],
                    prekey[9],
                    prekey[5],
                    prekey[6],
                    prekey[7]]
        
        self.key1 = [prekey11[5],
                prekey11[2],
                prekey11[6],
                prekey11[3],
                prekey11[7],
                prekey11[4],
                prekey11[9],
                prekey11[8]]

        self.key2 = [prekey12[5],
                prekey12[2],
                prekey12[6],
                prekey12[3],
                prekey12[7],
                prekey12[4],
                prekey12[9],
                prekey12[8]]


    def process(self, myByte):
        key1 = self.key1
        key2 = self.key2
        # IP
        myByte1 = [0]*8
        for i in range(8):
            myByte1[i] = myByte[SimplerDES.IP[i]]
        
        # F1
        exp1 = [myByte1[7],myByte1[4],myByte1[5],myByte1[6],myByte1[5],myByte1[6],myByte1[7],myByte1[4]]
        right1 = [key1[0]^exp1[0],key1[1]^exp1[1],key1[2]^exp1[2],key1[3]^exp1[3],key1[4]^exp1[4],key1[5]^exp1[5],key1[6]^exp1[6],key1[7]^exp1[7]]
        
        int1, int2 = SimplerDES.S_0[right1[0]*2+right1[3]][right1[1]*2+right1[2]]
        int3, int4 = SimplerDES.S_1[right1[4]*2+right1[7]][right1[5]*2+right1[6]]

        myByte2 = [myByte1[0]^int2,myByte1[1]^int4,myByte1[2]^int3,myByte1[3]^int1,myByte1[4],myByte1[5],myByte1[6],myByte1[7]]

        # Swap
        myByte3 = [myByte2[4],myByte2[5],myByte2[6],myByte2[7],myByte2[0],myByte2[1],myByte2[2],myByte2[3]]

        # F2
        exp2 = [myByte3[7],myByte3[4],myByte3[5],myByte3[6],myByte3[5],myByte3[6],myByte3[7],myByte3[4]]
        right2 = [key2[0]^exp2[0],key2[1]^exp2[1],key2[2]^exp2[2],key2[3]^exp2[3],key2[4]^exp2[4],key2[5]^exp2[5],key2[6]^exp2[6],key2[7]^exp2[7]]
        
        int1, int2 = SimplerDES.S_0[right2[0]*2+right2[3]][right2[1]*2+right2[2]]
        int3, int4 = SimplerDES.S_1[right2[4]*2+right2[7]][right2[5]*2+right2[6]]

        myByte4 = [myByte3[0]^int2,myByte3[1]^int4,myByte3[2]^int3,myByte3[3]^int1,myByte3[4],myByte3[5],myByte3[6],myByte3[7]]

        # inverse IP
        # IP
        myByte5 = [0]*8
        for i in range(8):
            myByte5[i] = myByte4[SimplerDES.IPinv[i]]
        return myByte5
    
    def intToList(self, num):
        binInt = bin(num)
        numList = [0]*8
        for i in range(-1, -len(binInt)+1, -1):
            numList[i] = int(binInt[i])
        return numList

    def listToInt(self, myList):
        weights = {-1:1, -2:2, -3:4, -4:8, -5:16, -6:32, -7:64, -8:128}
        num = 0
        for i in range(-1, -9, -1):
            if myList[i]:
                num += weights[i]
        return num
    
    def generateMaps(self):
        self.doMap = {}
        self.undoMap = {}
        for i in range(256):
            pre = self.intToList(i)
            post = self.listToInt(self.process(pre))
            self.doMap[i] = post
            self.undoMap[post] = i

    def setKey(self, key):
        self.key = key
        self.generateKeys()
        self.generateMaps()

    def setRandomKey(self):
        self.key = [randint(0,1) for x in range(10)]
        self.generateKeys()
        self.generateMaps()
    
    def setIV(self, iv):
        self.iv = iv

    def setRandomIV(self):
        self.iv = randint(0,255)

    def encryptECB(self, img_path):
        img = np.array(iio.imread(img_path))

        img_besyt = img.tobytes()
        output_bytes = [0]*len(img_besyt)
        for i in range(len(img_besyt)):
            output_bytes[i] = self.doMap[img_besyt[i]]

        enc_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)

        # Save the image 
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), enc_img)

    
    def decryptECB(self, img_path):

        img = iio.imread(img_path)
        enc_img = img.tobytes()
        output_bytes = [0]*len(enc_img)
        for i in range(len(enc_img)):
            output_bytes[i] = self.undoMap[enc_img[i]]
        
        dec_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), dec_img) 
    
    def encryptCBC(self, img_path):
        img = np.array(iio.imread(img_path))

        img_besyt = img.tobytes()

        
        output_bytes = [0]*len(img_besyt)
        # alter first block using iv
        output_bytes[0] = self.doMap[img_besyt[0]^self.iv]

        for i in range(1, len(img_besyt)):
            output_bytes[i] = self.doMap[img_besyt[i]^output_bytes[i-1]]

        enc_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)

        # Save the image 
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), enc_img)

    
    def decryptCBC(self, img_path):

        img = iio.imread(img_path)
        enc_img = img.tobytes()


        output_bytes = [0]*len(enc_img)
        output_bytes[0] = self.undoMap[enc_img[0]]^self.iv
        for i in range(1, len(enc_img)):
            output_bytes[i] = self.undoMap[enc_img[i]]^enc_img[i-1]
        
        dec_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), dec_img) 

    def encryptOFB(self, img_path):
        img = np.array(iio.imread(img_path))

        img_besyt = img.tobytes()

        cipherIV = self.doMap[self.iv]


        output_bytes = [0]*len(img_besyt)
        output_bytes[0] = img_besyt[0]^cipherIV


        for i in range(1, len(img_besyt)):
            cipherIV = self.doMap[cipherIV]
            output_bytes[i] = img_besyt[i]^cipherIV

        enc_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)

        # Save the image 
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), enc_img)

    
    def decryptOFB(self, img_path):

        img = iio.imread(img_path)
        enc_img = img.tobytes()
        output_bytes = [0]*len(enc_img)

        cipherIV = self.doMap[self.iv]
        output_bytes[0] = enc_img[0]^cipherIV

        for i in range(1, len(enc_img)):
            cipherIV = self.doMap[cipherIV]
            output_bytes[i] = enc_img[i]^cipherIV
        
        dec_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), dec_img)  
    
    def encryptCTR(self, img_path):
        img = np.array(iio.imread(img_path))

        img_besyt = img.tobytes()


        output_bytes = [0]*len(img_besyt)
        counter = 0

        for i in range(len(img_besyt)):
            output_bytes[i] = self.doMap[counter^self.iv]^img_besyt[i]
            counter = (counter+1)%256

        enc_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)

        # Save the image 
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), enc_img)

    
    def decryptCTR(self, img_path):

        img = iio.imread(img_path)
        enc_img = img.tobytes()
        output_bytes = [0]*len(enc_img)
        counter = 0

        for i in range(len(enc_img)):
            output_bytes[i] = self.doMap[counter^self.iv]^enc_img[i]
            counter = (counter+1)%256
        
        dec_img = np.frombuffer(bytes(output_bytes), np.uint8).reshape(img.shape)
        iio.imwrite(os.path.join(os.path.dirname(sys.argv[0]),"PiCKED App", 'sdes_output.png'), dec_img)  