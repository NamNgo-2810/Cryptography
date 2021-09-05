from DES import round_key_generate, encrypt, bin_to_hex
from AES import AES


# DES test
# des_plain_text = "123456ABCD132536"
# des_key = "AABB09182736CCDD"
# round_key_binary, round_key = round_key_generate(des_key)

# Encryption
# print("Encryption: ")
# des_cipher_text = bin_to_hex(encrypt(des_plain_text, round_key_binary, round_key))
# print("Cipher text: ", des_cipher_text)

# Decryption
# print("Decryption: ")
# round_key_binary_reversed = round_key_binary[::-1]
# round_key_reversed = round_key[::-1]
# text = bin_to_hex(encrypt(des_cipher_text, round_key_binary_reversed, round_key_reversed))
# print("Plain text: ", text)


# AES test
class test_aes_ecb:

    @staticmethod
    def test_hex(self):
        # Vector 128bit key
        aes_ecb_key = '000102030405060708090a0b0c0d0e0f'
        aes = AES(mode='ecb', input_type='hex')
        aes_ecb_cipher_text = aes.encryption('00112233445566778899aabbccddeeff', aes_ecb_key)
        print("Cipher text: ", aes_ecb_cipher_text)
        aes_ecb_plain_text = aes.decryption(aes_ecb_cipher_text, aes_ecb_key)
        print("Plain text: ", aes_ecb_plain_text)

    @staticmethod
    def test_string(self):
        # Test vector 128-bit key
        aes_ecb_key = '000102030405060708090a0b0c0d0e0f'
        # Ascii string test
        aes = AES(mode='ecb', input_type='text')
        aes_ecb_cipher_text = aes.encryption('root', aes_ecb_key)
        print("Cipher text: ", aes_ecb_cipher_text)
        aes_ecb_plain_text = aes.decryption(aes_ecb_cipher_text, aes_ecb_key)
        print("Plain text: ", aes_ecb_plain_text)


class test_aes_cbc:
    # AES CBC Mode Testing for hex string.
    @staticmethod
    def test_hex(self):
        # Test vector 128-bit key
        aes_cbc_key = '000102030405060708090a0b0c0d0e0f'
        aes = AES(mode='cbc', input_type='hex', iv='000102030405060708090A0B0C0D0E0F')
        # Random data to encrypt
        data = ['6bc1bee22e409f96e93d7e117393172a']
        aes_cbc_cipher_text = aes.encryption(data, aes_cbc_key)
        print("Cipher text: ", aes_cbc_cipher_text)
        aes_cbc_plain_text = aes.decryption(aes_cbc_cipher_text, aes_cbc_key)
        print("Plain text: ", aes_cbc_plain_text)


test_aes_ecb.test_hex(self=test_aes_ecb)
test_aes_ecb.test_string(self=test_aes_ecb)

test_aes_cbc.test_hex(self=test_aes_cbc)