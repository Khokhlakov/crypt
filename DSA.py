from Crypto.Hash import SHA256
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
import base64

class DSA_Signature:
    def __init__(self):
        self.key = None
        self.user_public_key = None
        self.user_private_key = None
        self.get_random_key(1024)

    def get_random_key(self,bits = 1024):
        self.key = DSA.generate(bits)
        return self.key
    
    def get_private_key(self):
        return base64.b64encode(self.key.export_key()).decode()

    def get_public_key(self):
        return base64.b64encode(self.key.publickey().export_key()).decode()

    def sign_message(self, message):
        h = SHA256.new(message)
        signer = DSS.new(self.key, 'fips-186-3')
        signature = signer.sign(h)
        return signature.hex()
    
    def sign_with_user_private_key(self, user_private_key, message):
        key = DSA.import_key(base64.b64decode(user_private_key))
        h = SHA256.new(message)
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(h)
        return signature.hex()

    def verify_signature(self, message, public_key, signature):
        h = SHA256.new(message)
        key = DSA.import_key(base64.b64decode(public_key))
        verifier = DSS.new(key, 'fips-186-3')
        try:
            verifier.verify(h, bytes.fromhex(signature))
            return True
        except ValueError:
            return False

    def leer_archivo_como_bytes(self,file_path):
        try:
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
                return file_bytes
        except FileNotFoundError:
            print("El archivo no se encontró o la ruta es incorrecta.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def test_dsa_signature():
    #creas un objeto
    dsa = DSA_Signature()

    #defines un mensaje que es una cadena de bytes, debes escribir el path del archivo como parametro
    message = dsa.leer_archivo_como_bytes('criptografia XI (1) (2).pdf')

    # Firmar el mensaje con la clave generada por la clase
    signature = dsa.sign_message(message)
    print("Firma con clave generada:", signature)

    # Obtener claves generadas por la clase
    private_key = dsa.get_private_key()
    public_key = dsa.get_public_key()
    print("Clave Privada generada:", private_key)
    print("Clave Pública generada:", public_key)

    # Verificar la firma con la clave pública generada
    result = dsa.verify_signature(message, public_key, signature)
    if result:
        print("La firma generada con clave generada es auténtica.")
    else:
        print("La firma generada con clave generada no es auténtica.")

    #Pedir al usuario que ingrese clave privada
    #private_key = input("ingrese la clave privada: ")

    # Firmar el mensaje con la clave proporcionada por el usuario
    user_signature = dsa.sign_with_user_private_key(private_key, message)
    print("Firma con clave proporcionada por el usuario:", user_signature)

    # Verificar la firma con la clave pública previamente generada
    result = dsa.verify_signature(message, public_key, user_signature)
    if result:
        print("La firma generada con clave proporcionada por el usuario es auténtica.")
    else:
        print("La firma generada con clave proporcionada por el usuario no es auténtica.")
    
    #Generar nuevas clave aleatoriamente
    #puedes escribir el tamaño en bits de la clave, por defecto: 1024, sugeridos: 2048,1024 (1024 más rápido)
    dsa.get_random_key() 
    print("NUEVA CLAVE GENERADA")

    # Obtener nuevas claves generadas por la clase
    private_key = dsa.get_private_key()
    public_key = dsa.get_public_key()
    print("Clave Privada generada:", private_key)
    print("Clave Pública generada:", public_key)
    
    # Verificar la firma con la clave pública generada
    result = dsa.verify_signature(message, public_key, signature)
    if result:
        print("La firma generada con clave generada es auténtica.")
    else:
        print("La firma generada con clave generada no es auténtica.")

    
# Ejecutar la función de testeo
#test_dsa_signature()
