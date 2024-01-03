from ecdsa import SigningKey, SECP256k1
import binascii

# Generar la llave privada y pública usando ECDSA (SECP256k1)
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

# Convertir las llaves a formato hexadecimal
private_key_hex = private_key.to_string().hex()
public_key_hex = public_key.to_string().hex()

# Imprimir las llaves en formato hexadecimal
print("Llave Privada:", private_key_hex)
print("Llave Pública:", public_key_hex)