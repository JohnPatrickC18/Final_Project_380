from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# We assume that after the victim paid the attacker
# The attacker gave the private key to decrypt


def load_private_key():
    with open("attacker_private_key.pem", "rb") as file:
        private_key = serialization.load_pem_private_key(file.read(), password=None)
    return private_key


def decrypt_file(filepath):
    if not filepath.endswith(".lab"):
        return  # Basically skips the any files that are not .lab

    print("Decrypting", filepath)

    with open(filepath, "rb") as file:
        key_len = int.from_bytes(file.read(4), "big")
        encrypted_aes_key = file.read(key_len)
        nonce = file.read(12)
        ciphertext = file.read()

    private_key = load_private_key()
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    output_name = filepath[:-4]

    with open(output_name, "wb") as f:
        f.write(plaintext)

    os.remove(filepath)


"""
def decrypt_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith(".lab"):
                continue

            filepath = os.path.join(root, file)

            print("Decrypting", filepath)

            plaintext = decrypt_file(filepath)

            output_name = file[:-4]

            output_path = os.path.join(folder_path, output_name)

            with open(output_path, "wb") as f:
                f.write(plaintext)

            os.remove(filepath)

"""

# decrypt_file("Important_Folder\home-banner-imgtxt.jpg.lab")
# decrypt_file(
#    r"C:\Users\JohnPatrick\Documents\MacEwan University Classes\CMPT 380\Final_Project_Code\Important_Folder\Important_Document2.txt.lab"
# )
# decrypt_file(
#    r"C:\Users\JohnPatrick\Documents\MacEwan University Classes\CMPT 380\Final_Project_Code\Important_Folder\w02_312_mcu_F.pdf.lab"
# )
