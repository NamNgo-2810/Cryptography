from DESPermutation import initial_permutation, expansion_d_box, final_permutation, straight_permutation, s_box, \
    key_parity, shift_table, key_compression


def hex_to_bin(s):
    """
    Convert hashcode to binary code
    :param s: string
    :return: string
    """
    mp = {
        '0': "0000",
        '1': "0001",
        '2': "0010",
        '3': "0011",
        '4': "0100",
        '5': "0101",
        '6': "0110",
        '7': "0111",
        '8': "1000",
        '9': "1001",
        'A': "1010",
        'B': "1011",
        'C': "1100",
        'D': "1101",
        'E': "1110",
        'F': "1111"
    }

    binary = ""
    for i in range(len(s)):
        binary += mp[s[i]]

    return binary


def bin_to_hex(s):
    """
    Convert binary code to hashcode
    :param s: string
    :return: string
    """
    mp = {
        "0000": '0',
        "0001": '1',
        "0010": '2',
        "0011": '3',
        "0100": '4',
        "0101": '5',
        "0110": '6',
        "0111": '7',
        "1000": '8',
        "1001": '9',
        "1010": 'A',
        "1011": 'B',
        "1100": 'C',
        "1101": 'D',
        "1110": 'E',
        "1111": 'F'
    }

    hashcode = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch += s[i]
        ch += s[i + 1]
        ch += s[i + 2]
        ch += s[i + 3]
        hashcode += mp[ch]

    return hashcode


def bin_to_dec(binary):
    """
    Convert binary number to decimal number
    :param binary: int
    :return: int
    """
    dec, i, n = 0, 0, 0
    while binary is not 0:
        num = binary % 10
        dec += num * pow(2, i)
        binary //= 10
        i += 1

    return dec


def dec_to_bin(dec):
    """
    Convert decimal number to binary string
    :param dec: int
    :return: string
    """
    res = bin(dec).replace("0b", "")
    if len(res) % 4 != 0:
        div = int(len(res) / 4)
        count = (4 * (div + 1)) - len(res)
        for i in range(0, count):
            res = '0' + res

    return res


def permute(k, arr, n):
    """
    Shuffle and extend or shrink string k according to defined order and number of bits
    :param k: string
    :param arr: permutation order array
    :param n: int - depend on phase, n can be 48 or 64
    :return: shuffled string
    """
    permutation = ""
    for i in range(n):
        permutation += k[arr[i] - 1]

    return permutation


def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1, len(k)):
            s += k[j]
        s += k[0]
        k = s
        s = ""

    return k


def xor(a, b):
    ans = ""
    for i in range(len(a)):
        ans += "0" if a[i] == b[i] else "1"

    return ans


def round_key_generate(key):
    key = hex_to_bin(key)
    permute(key, key_parity, 56)
    
    left = key[0:28]
    right = key[28:56]

    round_key_binary = []
    round_key = []
    for i in range(16):
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        combination = left + right
        rk = permute(combination, key_compression, 48)

        round_key_binary.append(rk)
        round_key.append(bin_to_hex(rk))


def encrypt(plain_text, round_key_binary, round_key):
    plain_text = hex_to_bin(plain_text)

    # Initial permute
    plain_text = permute(plain_text, initial_permutation, 64)
    print("After initial permutation: ", bin_to_hex(plain_text))

    # Split to left and right part
    left = plain_text[0:32]
    right = plain_text[32:64]

    # Round process
    for i in range(16):
        # Feistel function
        # Expand Ri-1 from 32bit to 48bit
        right_expanded = permute(right, expansion_d_box, 48)

        # Ri-1 XOR key
        xor_x = xor(right_expanded, round_key_binary[i])

        # Replace with S-box
        s_box_str = ""
        for j in range(8):
            # Split to 6-bit blocks
            row = bin_to_dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin_to_dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))

            # Append to result string
            val = s_box[j][row][col]
            s_box_str += dec_to_bin(val)

        # Straight permute from 48bit to 32bit
        s_box_str = permute(s_box_str, straight_permutation, 32)

        # Li-1 XOR f(Ri-1, K)
        result = xor(left, s_box_str)
        left = result

        # Swap left and right
        if i != 15:
            left, right = right, left
        print("Round ", i + 1, ": ", bin_to_hex(left), " ", bin_to_hex(right), " ", round_key[i])

    combination = left + right

    cipher_text = permute(combination, final_permutation, 64)
    return cipher_text
