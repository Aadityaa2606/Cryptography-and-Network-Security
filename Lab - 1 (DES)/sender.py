import socket

# CONSTANTS

S_BOX_STRING = '63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76' \
               'ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0' \
               'b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15' \
               '04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75' \
               '09 83 2c 1a 1b 6e 5a a0 52 3b d6 b3 29 e3 2f 84' \
               '53 d1 00 ed 20 fc b1 5b 6a cb be 39 4a 4c 58 cf' \
               'd0 ef aa fb 43 4d 33 85 45 f9 02 7f 50 3c 9f a8' \
               '51 a3 40 8f 92 9d 38 f5 bc b6 da 21 10 ff f3 d2' \
               'cd 0c 13 ec 5f 97 44 17 c4 a7 7e 3d 64 5d 19 73' \
               '60 81 4f dc 22 2a 90 88 46 ee b8 14 de 5e 0b db' \
               'e0 32 3a 0a 49 06 24 5c c2 d3 ac 62 91 95 e4 79' \
               'e7 c8 37 6d 8d d5 4e a9 6c 56 f4 ea 65 7a ae 08' \
               'ba 78 25 2e 1c a6 b4 c6 e8 dd 74 1f 4b bd 8b 8a' \
               '70 3e b5 66 48 03 f6 0e 61 35 57 b9 86 c1 1d 9e' \
               'e1 f8 98 11 69 d9 8e 94 9b 1e 87 e9 ce 55 28 df' \
               '8c a1 89 0d bf e6 42 68 41 99 2d 0f b0 54 bb 16'.replace(" ", "")
S_BOX = bytearray.fromhex(S_BOX_STRING)


def sub_word(word: [int]) -> bytes:
    substituted_word = bytes(S_BOX[i] for i in word)
    return substituted_word


def rcon(i: int) -> bytes:
    rcon_lookup = bytearray.fromhex('01020408102040801b36')
    rcon_value = bytes([rcon_lookup[i-1], 0, 0, 0])
    return rcon_value


def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes([x ^ y for (x, y) in zip(a, b)])


def rot_word(word: [int]) -> [int]:
    return word[1:] + word[:1]


def key_expansion(key: bytes, nb: int = 4) -> [[[int]]]:

    nk = len(key) // 4

    key_bit_length = len(key) * 8

    if key_bit_length == 128:
        nr = 10
    elif key_bit_length == 192:
        nr = 12
    else:  # 256-bit keys
        nr = 14

    w = state_from_bytes(key)

    for i in range(nk, nb * (nr + 1)):
        temp = w[i-1]
        if i % nk == 0:
            temp = xor_bytes(sub_word(rot_word(temp)), rcon(i // nk))
        elif nk > 6 and i % nk == 4:
            temp = sub_word(temp)
        w.append(xor_bytes(w[i - nk], temp))

    return [w[i*4:(i+1)*4] for i in range(len(w) // 4)]


def add_round_key(state: [[int]], key_schedule: [[[int]]], round: int):
    round_key = key_schedule[round]
    for r in range(len(state)):
        state[r] = [state[r][c] ^ round_key[r][c] for c in range(len(state[0]))]


def sub_bytes(state: [[int]]):
    for r in range(len(state)):
        state[r] = [S_BOX[state[r][c]] for c in range(len(state[0]))]


def shift_rows(state: [[int]]):
    state[0][1], state[1][1], state[2][1], state[3][1] = state[1][1], state[2][1], state[3][1], state[0][1]
    state[0][2], state[1][2], state[2][2], state[3][2] = state[2][2], state[3][2], state[0][2], state[1][2]
    state[0][3], state[1][3], state[2][3], state[3][3] = state[3][3], state[0][3], state[1][3], state[2][3]


def xtime(a: int) -> int:
    if a & 0x80:
        return ((a << 1) ^ 0x1b) & 0xff
    return a << 1


def mix_column(col: [int]):
    c_0 = col[0]
    all_xor = col[0] ^ col[1] ^ col[2] ^ col[3]
    col[0] ^= all_xor ^ xtime(col[0] ^ col[1])
    col[1] ^= all_xor ^ xtime(col[1] ^ col[2])
    col[2] ^= all_xor ^ xtime(col[2] ^ col[3])
    col[3] ^= all_xor ^ xtime(c_0 ^ col[3])


def mix_columns(state: [[int]]):
    for r in state:
        mix_column(r)


def state_from_bytes(data: bytes) -> [[int]]:
    state = [data[i*4:(i+1)*4] for i in range(len(data) // 4)]
    return state


def bytes_from_state(state: [[int]]) -> bytes:
    return bytes(state[0] + state[1] + state[2] + state[3])


def aes_encryption(data: bytes, key: bytes) -> bytes:
    state = state_from_bytes(data)
    key_schedule = key_expansion(key)
    add_round_key(state, key_schedule, round=0)

    for round in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, key_schedule, round)
        print("Round ", round, " : ", state)

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, key_schedule, round=10)

    cipher = bytes_from_state(state)
    return cipher




if __name__ == "__main__":
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 1234)
    s.connect(server_address)
    # Get input from the user
    plaintext = input("Enter the plaintext: ")

    # Pad the plaintext if needed
    block_size = 16
    padding_length = block_size - (len(plaintext) % block_size)
    plaintext += chr(padding_length) * padding_length

    # Convert the plaintext to bytes
    plaintext_bytes = plaintext.encode()

    # Perform AES encryption
    key = bytearray.fromhex('000102030405060708090a0b0c0d0e0f')
    ciphertext = aes_encryption(plaintext_bytes, key)
    print("Ciphertext (hex): ", ciphertext.hex())
    s.sendall(ciphertext)


