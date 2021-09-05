import random


def GCD(a, b):
    while True:
        temp = a % b
        if temp == 0:
            return b
        a = b
        b = temp


def xGCD(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0

    while b != 0:
        q = a // b
        a, b = b, a - q * b
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    return a, old_x, old_y


def chooseE(phi):
    while True:
        e = random.randrange(2, phi)
        if GCD(e, phi) == 1:
            return e


def chooseKey():
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    fo = open('primes-to-100k.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    n = prime1 * prime2
    phi = (prime1 - 1) * (prime2 - 1)
    e = chooseE(phi)

    gcd, x, y = xGCD(e, phi)

    d = x if x > 0 else x + phi

    # write the public keys n and e to a file
    f_public = open('public_key.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()


def encrypt(message, file_name='public_key.txt', block_size=2):
    try:
        fo = open(file_name, 'r')
    except FileNotFoundError:
        print('That file is not found.')

    else:
        n = int(fo.readline())
        e = int(fo.readline())
        fo.close()

        encrypted_blocks = []
        ciphertext = -1

        if len(message) > 0:
            # initialize ciphertext to the ASCII of the first character of message
            ciphertext = ord(message[0])

        for i in range(1, len(message)):
            # add ciphertext to the list if the max block size is reached
            # reset ciphertext so we can continue adding ASCII codes
            if i % block_size == 0:
                encrypted_blocks.append(ciphertext)
                ciphertext = 0

            # multiply by 1000 to shift the digits over to the left by 3 places
            # because ASCII codes are a max of 3 digits in decimal
            ciphertext = ciphertext * 1000 + ord(message[i])

        # add the last block to the list
        encrypted_blocks.append(ciphertext)

        # encrypt all of the numbers by taking it to the power of e
        # and modding it by n
        for i in range(len(encrypted_blocks)):
            encrypted_blocks[i] = str((encrypted_blocks[i] ** e) % n)

        # create a string from the numbers
        encrypted_message = " ".join(encrypted_blocks)

        return encrypted_message


def decrypt(blocks, block_size=2):

    fo = open('private_keys.txt', 'r')
    n = int(fo.readline())
    d = int(fo.readline())
    fo.close()

    # turns the string into a list of ints
    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    # converts each int in the list to block_size number of characters
    # by default, each int represents two characters
    for i in range(len(int_blocks)):
        # decrypt all of the numbers by taking it to the power of d
        # and modding it by n
        int_blocks[i] = (int_blocks[i] ** d) % n

        tmp = ""
        # take apart each block into its ASCII codes for each character
        # and store it in the message string
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000
        message += tmp

    return message


def main():
    # we select our primes and generate our public and private keys,
    # usually done once
    choose_again = input('Do you want to generate new public and private keys? (y or n) ')
    if choose_again == 'y':
        chooseKey()

    instruction = input('Would you like to encrypt or decrypt? (Enter e or d): ')
    if instruction == 'e':
        message = input('What would you like to encrypt?\n')
        option = input('Do you want to encrypt using your own public key? (y or n) ')

        if option == 'y':
            print('Encrypting...')
            print(encrypt(message))
        else:
            file_option = input('Enter the file name that stores the public key: ')
            print('Encrypting...')
            print(encrypt(message, file_option))

    elif instruction == 'd':
        message = input('What would you like to decrypt?\n')
        print('Decryption...')
        print(decrypt(message))
    else:
        print('That is not a proper instruction.')


main()
