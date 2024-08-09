import base64

import rsa
from django.conf import settings


def encrypt_for_db(data):
    public_key = settings.PUBLIC_KEY.replace("\\n", "\n")
    crypt = rsa.encrypt(data.encode(), rsa.PublicKey.load_pkcs1(public_key))
    return base64.b64encode(crypt).decode()


def decrypt_from_db(crypted_data):
    crypted_data = base64.b64decode(crypted_data.encode())

    private_key = settings.PRIVATE_KEY.replace("\\n", "\n")

    return rsa.decrypt(crypted_data, rsa.PrivateKey.load_pkcs1(private_key)).decode()


def verify_encryption(crypted_data) -> bool:

    try:
        decrypt_from_db(crypted_data)
    except rsa.pkcs1.DecryptionError:
        return False

    return True
