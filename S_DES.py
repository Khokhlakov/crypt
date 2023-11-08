
import random


class SDES:
    def __init__(self, key = None, mode = None, IV  = None):
        self.key = key
        self.mode = mode
        self.iv = IV
        self.ctr = IV
        self.k1 = None
        self.k2 = None

        self.IP = [1,5,2,0,3,7,4,6]         #26314857
        self.P10 = [2,4,1,6,3,9,0,8,7,5]    #35274.10.1986 
        self.P8 = [5,2,6,3,7,4,9,8]         #637485.10.9
        self.P4 = [1,3,2,0]                 #2431
        self.inv_IP = [3,0,2,4,6,1,7,5]     #41357286
        self.EP = [3,0,1,2,1,2,3,0]         #41232341

        self.S_0 = [
            [ [0, 1], [0, 0], [1, 1], [1, 0] ],
            [ [1, 1], [1, 0], [0, 1], [0, 0] ],
            [ [0, 0], [1, 0], [0, 1], [1, 1] ],
            [ [1, 1], [0, 1], [1, 1], [1, 0] ],
        ]

        self.S_1 = [
            [ [0, 0], [0, 1], [1, 0], [1, 1] ],
            [ [1, 0], [0, 0], [0, 1], [1, 1] ],
            [ [1, 1], [0, 0], [0, 1], [0, 0] ],
            [ [1, 0], [0, 1], [0, 0], [1, 1] ],
        ]


    def generate_random_key(self):

        # Generate a random sequence of 10 bits
        random_key = [random.choice([0, 1]) for _ in range(10)]
        # Convert the list into a bit string
        random_key = ''.join(map(str, random_key))
        # Upgrade key
        self.key = random_key

        return self.key
    
    def generate_random_iv(self):
        # Generate a random sequence of 8 bits
        random_iv = [random.choice([0, 1]) for _ in range(8)]
        # Convert the list into a bit string
        random_iv = ''.join(map(str, random_iv))
        #Upgrade iv
        self.iv = random_iv

        return self.iv


    def get_k1_k2(self):
        #Get k1 and k2 from key bit string
        key = self.str_to_list(self.key)
        k1 = self.p10(key)
        k1 = self.ls_1(k1)
        k2 = self.ls_1(self.ls_1(k1))
        k1 = self.p8(k1)
        k2 = self.p8(k2)
        self.k1 = k1
        self.k2 = k2

#permutations       
    def permutation(self, input_list, permutation_list): #permutation numbers in [0,9]
        
        #Creates a list for permuted bits
        permuted_bits = []
        for val in permutation_list:
            permuted_bits.append(input_list[val])
        return permuted_bits

    def ip(self,input_str):
        return self.permutation(input_str, self.IP)

    def inv_ip(self,input_str):
        return self.permutation(input_str, self.inv_IP)

    def p8(self,input_str):
        return self.permutation(input_str, self.P8)

    def ls_1(self,input_str):
        return self.permutation(input_str, [1,2,3,4,0,6,7,8,9,5])

    def p10(self,input_str):
        return self.permutation(input_str, self.P10)

    def ep(self,input_str):
        return self.permutation(input_str, self.EP)
    
    def p4(self,input_str):
        return self.permutation(input_str, self.P4)
    
    def swap(self, input_str):
        return self.permutation(input_str, [4,5,6,7,0,1,2,3])

#inner s-des functions
    def f(self, key_val, input_str):
        left = input_str[:4]
        right = input_str[4:]
        return self.xor(left, self.F(key_val, right)) + right
        
    def xor(self,input_list1,input_list2): #both bit sequences have the same length
        output_list = []
        for i in range(len(input_list1)):
            output_list.append(input_list1[i]^input_list2[i])
        # Perform XOR operation between both sequences
        return output_list

    def F(self, key_val, input_list):
        output_list = self.ep(input_list)
        output_list = self.xor(output_list, key_val)
        output_list = self.s0s1(output_list)
        return self.p4(output_list)

    def s0s1(self,input_list):
        #Split input_list in left and right
        left = input_list[:4]
        right = input_list[4:]
        #get matrix value from S_0 and S_1 for left and right sides
        matrix_left = self.s_i(left, self.S_0)
        matrix_right = self.s_i(right, self.S_1)
        #Join both bit lists
        return matrix_left + matrix_right

    def s_i(self,input_list, matrix):
        #gets the matrix value from 4 bits sequence
        row = input_list[0]*2 + input_list[3]
        column = input_list[1]*2 + input_list[2]
        return matrix[row][column]

#list<->str functions        
    def str_to_list(self,input_str):
        # Convert a string into a list of integers
        return [int(character) for character in input_str]

    def list_to_str(self,input_list):
        #convert a list to a string
        return "".join(map(str, input_list))

#extra functions
    def xor_str(self, str1, str2): #xor of 8 bits strings
        result_xor = ""
        for i in range(8):
            if str1[i] != str2[i]:
                result_xor += "1"
            else:
                result_xor += "0"
        return result_xor

#standar S-DES encrypt and decrpyt functions

    def std_encrypt(self,plain_str):
        #return a cipher bit list from a plain bit string
        cipher_list = self.ip(self.str_to_list(plain_str))
        cipher_list = self.f(self.k1,cipher_list)
        cipher_list = self.swap(cipher_list)
        cipher_list = self.f(self.k2,cipher_list)
        cipher_list = self.inv_ip(cipher_list)
        
        return cipher_list

    def std_decrypt(self,cipher_str):
        #return a plain bit list from a cipher bit string
        plain_list = self.ip(self.str_to_list(cipher_str))
        plain_list = self.f(self.k2,plain_list)
        plain_list = self.swap(plain_list)
        plain_list = self.f(self.k1,plain_list)
        plain_list = self.inv_ip(plain_list)
    
        return plain_list

#main encrypt and decrpyt SDES functions    
    def encrypt(self,plain_message):
        #gets k1 and k2 from key bit string
        self.get_k1_k2()
        #encrypt plain message using selected mode
        if self.mode == "ECB":
            return self.ECB_encrypt(plain_message)
        elif self.mode == "CBC":
            return self.CBC_encrypt(plain_message)
        elif self.mode == "OFB":
            return self.OFB_encrypt(plain_message)
        elif self.mode == "CTR":
            return self.CTR_encrypt(plain_message)
    
    def decrypt(self, cipher_message):
        #gets k1 and k2 from key bit string
        self.get_k1_k2()
        #decrypt plain message using selected mode
        if self.mode == "ECB":
            return self.ECB_decrypt(cipher_message)
        elif self.mode == "CBC":
            return self.CBC_decrypt(cipher_message)
        elif self.mode == "OFB":
            return self.OFB_encrypt(cipher_message)
        elif self.mode == "CTR":
            return self.CTR_encrypt(cipher_message)
        
#Modes
  
#ECB mode 
    def ECB_encrypt(self, plain_message):
        # Create list of bytes of cipher message
        cipher_message_bytes_list = []
        print("len_plain_message: ", len(plain_message))
        
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in plain_message:
            if i%100000==0: print("i: ",i)
            i+=1
            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')
            
            #encrypt binary representation with standar S-DES
            bits_list = self.std_encrypt(bits_str)
            
            # Converts encrypted binary representation list to byte
            cipher_byte = 0
            for j in bits_list:
                cipher_byte = cipher_byte*2 + j
            
            # Appends cipher byte to list of cipher message bytes
            cipher_message_bytes_list.append(cipher_byte)

        # Create bytes string from cipher message bytes list
        return bytes(cipher_message_bytes_list)
 
    def ECB_decrypt(self, cipher_message):
        # Create list of bytes of cipher message
        plain_message_bytes_list = []
        print("len_plain_message: ", len(cipher_message))
        
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in cipher_message:
            if i%100000==0: print("i: ",i)
            i+=1
            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')
            
            #encrypt binary representation with standar S-DES
            bits_list = self.std_decrypt(bits_str)
            
            # Converts encrypted binary representation list to byte
            plain_byte = 0
            for j in bits_list:
                plain_byte = plain_byte*2 + j
            
            # Appends cipher byte to list of cipher message bytes
            plain_message_bytes_list.append(plain_byte)

        # Create bytes string from cipher message bytes list
        return bytes(plain_message_bytes_list)

#CBC mode
    def CBC_encrypt(self, plain_message):
        # Create list of bytes of cipher message
        cipher_message_bytes_list = []
        print("len_plain_message: ", len(plain_message))

        cipher_bits_str = self.iv
        print("Cv_",cipher_bits_str)
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in plain_message:
            if i%100000==0: print("i: ",i)
            
            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')
            #xor with cipher_bits_str
            bits_str = self.xor_str(bits_str, cipher_bits_str)
            #encrypt binary representation with standar S-DES
            cipher_bits_list = self.std_encrypt(bits_str)
            
            # Converts encrypted binary representation list to byte
            cipher_byte = 0
            for j in cipher_bits_list:
                cipher_byte = cipher_byte*2 + j

            #convert cipher_bits_list from list to string upgrading it
            cipher_bits_str = self.list_to_str(cipher_bits_list)
            # Appends cipher byte to list of cipher message bytes
            cipher_message_bytes_list.append(cipher_byte)
            i+=1

        # Create bytes string from cipher message bytes list
        return bytes(cipher_message_bytes_list)
    
    def CBC_decrypt(self, cipher_message):
        # Create list of bytes of cipher message
        plain_message_bytes_list = []
        print("len_plain_message: ", len(cipher_message))

        #set first cipher_bits_list_0 as iv, used for xor
        cipher_bits_list_0 = self.str_to_list(self.iv)
        print("Cv_",cipher_bits_list_0)
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in cipher_message:
            if i%100000==0: print("i: ",i)
            
            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')

            #extract cipher_bits_list_1 for next round xor
            cipher_bits_list_1 = self.str_to_list(bits_str)

            #encrypt binary representation with standar S-DES
            plain_bits_list = self.std_decrypt(bits_str)
            
            #xor with cipher_bits_list
            plain_bits_list = self.xor(plain_bits_list, cipher_bits_list_0)

            # Converts encrypted binary representation list to byte
            plain_byte = 0
            for j in plain_bits_list:
                plain_byte = plain_byte*2 + j

            # Appends cipher byte to list of cipher message bytes
            plain_message_bytes_list.append(plain_byte)

            #takes cipher_bits_list_1 as cipher_bits_list_0 for next round xor
            cipher_bits_list_0  = cipher_bits_list_1
            i+=1

        # Create bytes string from cipher message bytes list
        return bytes(plain_message_bytes_list)

#OFB mode
    def OFB_encrypt(self, plain_message):
        # Create list of bytes of cipher message
        cipher_message_bytes_list = []
        print("len_plain_message: ", len(plain_message))

        cipher_bits_str_iv = self.iv
        print("Cv_",cipher_bits_str_iv)
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in plain_message:
            if i%100000==0: print("i: ",i)
            
            #encrypt binary representation with standar S-DES of cipher_bits_str_iv
            cipher_bits_list_iv = self.std_encrypt(cipher_bits_str_iv)
            #convert to str the previous list
            cipher_bits_str_iv = self.list_to_str(cipher_bits_list_iv)

            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')
            #xor with cipher_bits_str_iv
            bits_str = self.xor_str(bits_str, cipher_bits_str_iv)
            
            
            # Converts encrypted binary representation list to byte
            cipher_byte = 0
            for j in bits_str:
                cipher_byte = cipher_byte*2 + int(j)

            # Appends cipher byte to list of cipher message bytes
            cipher_message_bytes_list.append(cipher_byte)
            i+=1

        # Create bytes string from cipher message bytes list
        return bytes(cipher_message_bytes_list) 

#CTR mode
    def CTR_encrypt(self, plain_message):
        # Create list of bytes of cipher message
        cipher_message_bytes_list = []
        print("len_plain_message: ", len(plain_message))
        #we use iv as counter
        ctr = int(self.iv,2) 
        print("Cv_",ctr)
        i = 0
        # Iterate over each byte of plain message string of bytes
        for byte in plain_message:
            if i%100000==0: print("i: ",i)
            ctr_str = bin((ctr + i) % 256)[2:].zfill(8)
            
            #encrypt binary representation with standar S-DES of ctr_str
            cipher_bits_list_ctr = self.std_encrypt(ctr_str)
            #convert to str the previous list
            cipher_bits_str_ctr = self.list_to_str(cipher_bits_list_ctr)

            #Get the byte binary representation, remove the '0b' prefix, and ensure 8 characters
            bits_str = format(byte , '08b')
            #xor with cipher_bits_str_iv
            bits_str = self.xor_str(bits_str, cipher_bits_str_ctr)
            
            
            # Converts encrypted binary representation list to byte
            cipher_byte = 0
            for j in bits_str:
                cipher_byte = cipher_byte*2 + int(j)

            # Appends cipher byte to list of cipher message bytes
            cipher_message_bytes_list.append(cipher_byte)
            i+=1

        # Create bytes string from cipher message bytes list
        return bytes(cipher_message_bytes_list) 



