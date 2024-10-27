import Crypto
import Crypto.Cipher.AES

def decryptor(key,video):
    de=Crypto.Cipher.AES.new(key,IV=b"0000000000000000",mode=Crypto.Cipher.AES.MODE_CBC)
    return de.decrypt(video)