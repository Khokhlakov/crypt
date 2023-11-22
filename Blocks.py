#Before: pip install cryptography

# Had to use: pip install pycryptodome ~JJ

from Crypto.Cipher import AES, DES3
from S_DES import SDES
from Crypto.Random import get_random_bytes
from PIL import Image
import numpy as np
import imageio.v3 as iio

class Blocks:
    def __init__(self, cipher_type, mode, key_length, key=None, iv = None):
        self.cipher_type = cipher_type
        self.mode = mode
        self.key = key
        self.key_length = key_length
        self.iv = iv
        self.plain_image = None
        self.plain_image_code = None
        self.ciphered_image_code = None
        self.ciphered_image = None
        self.cipher = None
        self.width = None
        self.height = None
        self.plain_image_path = "plain_image.png"
        self.ciphered_image_path = "ciphered_image.png"

        self.plain_image_output = None
        self.plain_image_path_output = "plain_image_output.png"

#image proccessing
    def load_plain_image(self):
        # Load a plain image in PNG format, and sets width and height
        self.plain_image = Image.open(self.plain_image_path)
        self.width, self.height = self.plain_image.size

    def plain_image_to_code(self):
        # Convert the PNG image to a byte string (plain_image_code)
        self.plain_image_code = self.plain_image.tobytes()

    def load_ciphered_image(self):
        # Load a ciphered image in PNG format, and sets width and height
        self.ciphered_image = Image.open(self.ciphered_image_path)
        self.width, self.height = self.ciphered_image.size

    def ciphered_image_to_code(self):
        # Convert the PNG ciphered image to a byte string (ciphered_image_code)
        self.ciphered_image_code = self.ciphered_image.tobytes()

    def create_plain_image(self):
        #Create a plain_image in PNG format from a byte string (plain_image_code)
        self.plain_image_output = Image.frombytes('RGB', (self.width, self.height), self.plain_image_code)
        self.plain_image_output.save(self.plain_image_path_output)
    
    def create_ciphered_image(self):
        #Create a ciphered_image in JPEG format from a byte string (ciphered_image_code)
        self.ciphered_image = Image.frombytes('RGB', (self.width, self.height), self.ciphered_image_code)
        self.ciphered_image.save(self.ciphered_image_path)
    
#random key and IV vector
    def generate_random_key(self):
        # Generate a random key based on the key length
        self.key = get_random_bytes(self.key_length)
    
    def generate_random_iv(self):
        # Generate a random iv vector based of 16 bytes
        self.iv= get_random_bytes(16)

#encrypt and decrypt
    def encrypt(self):
        # Encrypt plain_image_code to ciphered_image_code
        if self.cipher_type == "AES":
            self.AES_modes()
        elif self.cipher_type == "S-DES":
            self.SDES_modes()
        elif self.cipher_type == "T-DES":
            self.DES3_modes()
        self.load_plain_image()
        self.plain_image_to_code()
        self.ciphered_image_code = self.cipher.encrypt(self.plain_image_code)
        self.create_ciphered_image()

    def decrypt(self):
        # Decrypt ciphered_image_code to plain_image_code
        if self.cipher_type == "AES":
            self.AES_modes()
        elif self.cipher_type == "S-DES":
            self.SDES_modes()
        elif self.cipher_type == "T-DES":
            self.DES3_modes()
        self.load_ciphered_image()
        self.ciphered_image_to_code()
        self.plain_image_code = self.cipher.decrypt(self.ciphered_image_code)
        self.create_plain_image()

#cipher types setting modes
    def AES_modes(self):
        #Sets AES mode (key lengths: 16,24 or 32 bytes)
        if self.key == None:
            self.generate_random_key()
        if self.mode == "ECB":
            self.cipher = AES.new(self.key, AES.MODE_ECB)
        else:
            if self.iv == None:
                self.generate_random_iv()
            if self.mode == "CBC":
                self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            elif self.mode == "OFB":
                self.cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            elif self.mode == "CTR":
                self.cipher = AES.new(self.key, AES.MODE_CTR, nonce = self.iv[:8])
    
    def DES3_modes(self):
        #Sets T-DES mode (key lengths: 16 or 24 bytes)
        if self.key == None:
            self.generate_random_key()
        if self.mode == "ECB":
            self.cipher = DES3.new(self.key, DES3.MODE_ECB)
        else:
            if self.iv == None:
                self.generate_random_iv()
            if self.mode == "CBC":
                self.cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv[:8])
            elif self.mode == "OFB":
                self.cipher = DES3.new(self.key, DES3.MODE_OFB, self.iv[:8])
            elif self.mode == "CTR":
                self.cipher = DES3.new(self.key, DES3.MODE_CTR, nonce = self.iv[:4])

    def SDES_modes(self):
        #Sets S-DES mode (key length: 10 bits)
        if self.mode == "ECB":
            self.cipher = SDES(self.key, "ECB")
        else:
            if self.mode == "CBC":
                self.cipher = SDES(self.key, "CBC", self.iv) # iv must be an 8 bits string
            elif self.mode == "OFB":
                self.cipher = SDES(self.key, "OFB", self.iv)
            elif self.mode == "CTR":
                self.cipher = SDES(self.key, "CTR", self.iv)
            if self.iv == None:
                self.iv = self.cipher.generate_random_iv()
        if self.key == None:
            self.key = self.cipher.generate_random_key()

def getRandAES(keyLen):
    key = get_random_bytes(keyLen)
    return key


def encrypt_image_AES(image_path, mode, key):
    # Read image to NumPy array
    img = np.array(iio.imread(image_path))

    # Pad rows of zeros in case number of bytes is not a multiple of 16
    if img.size % 16 > 0:
        row = img.shape[0]
        pad = 16 - (row % 16)  # Number of rows to pad
        img = np.pad(img, ((0, pad), (0, 0), (0, 0)))  # Pad rows at the bottom
        img[-1, -1, 0] = pad  # Store the pad value in the last element
        print("preasd", pad)
    # Otherwise store pad value of 0
    else:
        img[-1, -1, 0] = 0

    img_bytes = img.tobytes()  # Convert NumPy array to sequence of bytes 

    # Encrypt the array of bytes.
    iv = b'0000000000000000'
    if mode == "ECB":
        enc_img_bytes = AES.new(key, AES.MODE_ECB).encrypt(img_bytes)
    elif mode == "CBC":
        enc_img_bytes = AES.new(key, AES.MODE_CBC, iv).encrypt(img_bytes) 
    elif mode == "OFB":
        enc_img_bytes = AES.new(key, AES.MODE_OFB, iv).encrypt(img_bytes) 
    elif mode == "CTR":
        enc_img_bytes = AES.new(key, AES.MODE_CTR, nonce = iv[:8]).encrypt(img_bytes) 
     

    # Convert the encrypted buffer to NumPy array and reshape to the shape of the padded image 
    enc_img = np.frombuffer(enc_img_bytes, np.uint8).reshape(img.shape)

    # Save the image 
    iio.imwrite('aes_output.png', enc_img)


def decrypt_image_AES(image_path, mode, key):
    enc_img = iio.imread(image_path)

    iv = b'0000000000000000'
    if mode == "ECB":
        dec_img_bytes = AES.new(key, AES.MODE_ECB).decrypt(enc_img.tobytes())
    elif mode == "CBC":
        dec_img_bytes = AES.new(key, AES.MODE_CBC, iv).decrypt(enc_img.tobytes())
    elif mode == "OFB":
        dec_img_bytes = AES.new(key, AES.MODE_OFB, iv).decrypt(enc_img.tobytes())
    elif mode == "CTR":
        dec_img_bytes = AES.new(key, AES.MODE_CTR, nonce = iv[:8]).decrypt(enc_img.tobytes()) 

    dec_img = np.frombuffer(dec_img_bytes, np.uint8).reshape(enc_img.shape)  # The shape of the encrypted and decrypted image is the same

    pad = int(dec_img[-1, -1, 0])  # Get the stored padding value
    if pad != 0:
        dec_img = dec_img[0:-pad, :, :].copy()  # Remove the padding rows when pad is different from 0

    iio.imwrite('aes_output.png', dec_img) 


# TDES:
def getRandTDES(keyLen):
    key = get_random_bytes(keyLen)
    return key


def encrypt_image_TDES(image_path, mode, key):
    # Read image to NumPy array
    img = np.array(iio.imread(image_path))

    # Pad rows of zeros in case number of bytes is not a multiple of 16
    if img.size % 16 > 0:
        row = img.shape[0]
        pad = 16 - (row % 16)  # Number of rows to pad
        img = np.pad(img, ((0, pad), (0, 0), (0, 0)))  # Pad rows at the bottom
        img[-1, -1, 0] = pad  # Store the pad value in the last element
        print("preasd", pad)
    # Otherwise store pad value of 0
    else:
        img[-1, -1, 0] = 0

    img_bytes = img.tobytes()  # Convert NumPy array to sequence of bytes 

    # Encrypt the array of bytes.
    iv = b'0000000000000000'
    if mode == "ECB":
        enc_img_bytes = DES3.new(key, DES3.MODE_ECB).encrypt(img_bytes)
    elif mode == "CBC":
        enc_img_bytes = DES3.new(key, DES3.MODE_CBC, iv[:8]).encrypt(img_bytes) 
    elif mode == "OFB":
        enc_img_bytes = DES3.new(key, DES3.MODE_OFB, iv[:8]).encrypt(img_bytes) 
    elif mode == "CTR":
        enc_img_bytes = DES3.new(key, DES3.MODE_CTR, nonce = iv[:4]).encrypt(img_bytes) 
     

    # Convert the encrypted buffer to NumPy array and reshape to the shape of the padded image 
    enc_img = np.frombuffer(enc_img_bytes, np.uint8).reshape(img.shape)

    # Save the image 
    iio.imwrite('TDES_output.png', enc_img)


def decrypt_image_TDES(image_path, mode, key):
    enc_img = iio.imread(image_path)

    iv = b'0000000000000000'
    if mode == "ECB":
        dec_img_bytes = DES3.new(key, DES3.MODE_ECB).decrypt(enc_img.tobytes())
    elif mode == "CBC":
        dec_img_bytes = DES3.new(key, DES3.MODE_CBC, iv[:8]).decrypt(enc_img.tobytes())
    elif mode == "OFB":
        dec_img_bytes = DES3.new(key, DES3.MODE_OFB, iv[:8]).decrypt(enc_img.tobytes())
    elif mode == "CTR":
        dec_img_bytes = DES3.new(key, DES3.MODE_CTR, nonce = iv[:4]).decrypt(enc_img.tobytes()) 

    dec_img = np.frombuffer(dec_img_bytes, np.uint8).reshape(enc_img.shape)  # The shape of the encrypted and decrypted image is the same

    pad = int(dec_img[-1, -1, 0])  # Get the stored padding value
    if pad != 0:
        dec_img = dec_img[0:-pad, :, :].copy()  # Remove the padding rows when pad is different from 0

    iio.imwrite('TDES_output.png', dec_img) 

#README
    #Put an image in the folder where the code is located, name it "plain_image.png"
    #Define a Blocks object: name_objetc = Blocks(TYPE_CIPHER, OPERATION_MODE, KEY_LENGTH, KEY*, IV*)
    #Use encrypt and decrypt methods
        #encrypt will create an image named "ciphered_image.png" in path folder
        #decrypt will take an image named "ciphered_image.png" ...
        #    ... in path folder and create an image named "plain_image_output.png" in path folder too
#PARAMETERS
    #Only Parameters with * are optional
    #If not KEY or IV are given they will be created randomly
#TYPE CIPHER: 
    # "AES"
    # "T-DES"
    # "S-DES"
#OPERATION MODE
    # "ECB"
    # "CBC"
    # "OFB"
    # "CTR"
#KEYS LENGTH
    #AES: 16, 24 or 32 bytes (give bytes string)
    #T-DES: 16 or 24 bytes
    #S-DES: 1 byte (give 8 bit string)

#IMPORTANT CONSTRAINTS
    #Plain_image.png is always a image in png format
    #Plain_image dimensions must satisfy: 16 | (heigth * width) for AES and TDES ciphers, no problem for SDES

#EXTRA INFORMATION
    #Error handling needs to be inplemented
    #SDES cipher is slow

# EXAMPLE OF USAGE

# block = Blocks("AES", "CTR", 16)
# block.encrypt()
# print("key: ",block.key)
# block.decrypt()
# print("process completed")

