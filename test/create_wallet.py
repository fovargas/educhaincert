from bit import PrivateKeyTestnet

# Generar una nueva clave privada para Testnet
testnet_key = PrivateKeyTestnet()

# Imprimir la clave privada (WIF) y la dirección SegWit
print("Clave privada (formato WIF):", testnet_key.to_wif())
print("Dirección SegWit:", testnet_key.segwit_address)