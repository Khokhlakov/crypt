import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


class RSAEncryption:
    def __init__(self, key_size=2048):
        self.private_key = None
        self.public_key = None
        self.private_key_base64 = None
        self.public_key_base64 = None
        self.encrypted_message = None
        self.plain_message = None
        self.decrypted_message = None

        # Generar claves al inicializar el objeto
        self.generate_keys(key_size)

    def generate_keys(self, key_size):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

        # Convertir las claves a base64 y almacenarlas en los atributos correspondientes
        self.private_key_base64 = self.private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        self.private_key_base64 = base64.b64encode(self.private_key_base64).decode()

        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key_base64 = base64.b64encode(public_key_bytes).decode()

    def encrypt_message(self, message):
        self.plain_message = message
        encrypted = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.encrypted_message = base64.b64encode(encrypted).decode()

    def decrypt_message(self):
        encrypted_bytes = base64.b64decode(self.encrypted_message)
        decrypted = self.private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.decrypted_message = decrypted.decode()

    def set_private_key(self, private_key_b64):
        private_key_bytes = base64.b64decode(private_key_b64)
        self.private_key = serialization.load_der_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )
        self.private_key_base64 = private_key_b64

    def set_public_key(self, public_key_b64):
        public_key_bytes = base64.b64decode(public_key_b64)
        self.public_key = serialization.load_der_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        self.public_key_base64 = public_key_b64


def test_rsa_encryption():
    # Crear una instancia de RSAEncryption con un key_size por defecto de 2048
    rsa_obj = RSAEncryption()

    # Mostrar la clave privada y pública generadas aleatoriamente
    print("Clave privada generada aleatoriamente en base64:\n", rsa_obj.private_key_base64)
    print("\nClave pública generada aleatoriamente en base64:\n", rsa_obj.public_key_base64)

    # Actualizar la clave privada y pública con valores proporcionados por el usuario
    user_private_key = input("\nIngresa la clave privada en base64 para actualizarla: ")
    rsa_obj.set_private_key(user_private_key)

    user_public_key = input("\nIngresa la clave pública en base64 para actualizarla: ")
    rsa_obj.set_public_key(user_public_key)

    # Cifrar un mensaje proporcionado por el usuario y mostrar el texto cifrado
    message_to_encrypt = input("\nIngresa un mensaje para cifrar con la clave pública: ")
    rsa_obj.encrypt_message(message_to_encrypt)
    print("\nMensaje cifrado con la clave pública proporcionada:\n", rsa_obj.encrypted_message)

    # Descifrar un texto cifrado proporcionado por el usuario y mostrar el mensaje descifrado
    encrypted_text = input("\nIngresa un texto cifrado para descifrar con la clave privada: ")
    rsa_obj.encrypted_message = encrypted_text  # Actualizar el texto cifrado en los atributos de la clase
    rsa_obj.decrypt_message()
    print("\nMensaje descifrado con la clave privada proporcionada:\n", rsa_obj.decrypted_message)

#INFORMACION EXTRA
def componentes_clave():
    # Generar las claves
    rsa_obj = RSAEncryption()
    rsa_obj.generate_keys(2048)

    # Acceder a los valores específicos de la clave pública y privada
    public_key = rsa_obj.public_key.public_numbers()
    private_key = rsa_obj.private_key.private_numbers()
    

    # Obtener los componentes principales
    modulus_n = public_key.n  # Módulo (n) de la clave pública
    exponent_e = public_key.e  # Exponente de cifrado (e) de la clave pública

    private_exponent_d = private_key.d  # Exponente de descifrado (d) de la clave privada

    # Imprimir los componentes de la clave
    print("Componentes de la clave pública:")
    print(f"Módulo (n): {modulus_n}")
    print(f"Exponente de cifrado (e): {exponent_e}")

    print("\nComponentes de la clave privada:")
    print(f"Exponente de descifrado (d): {private_exponent_d}")


# Ejecutar el test
#test_rsa_encryption()
#componentes_clave()