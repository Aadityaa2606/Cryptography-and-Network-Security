import struct
from enum import Enum
from math import floor, sin
from bitarray import bitarray

# Define the four auxiliary functions that produce one 32-bit word.
def F(x, y, z):
    return x & y | ~x & z

def G(x, y, z):
    return x & z | y & ~z

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def rotate_left(x, n):
    return x << n | x >> 32 - n

def modular_add(a, b):
    return (a + b) % pow(2, 32)

# T table
T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

class MD5:
    input_string = None
    buffers = {
        "A": 0x67452301,
        "B": 0xEFCDAB89,
        "C": 0x98BADCFE,
        "D": 0x10325476,
    }

    def hash(self, string):
        self.input_string = string
        # convert string to bit array for easier operation and add padding
        temp = self.step_1()
        # Append length of message to end of data
        preprocessed_bit_array = self.step_2(temp)
        self.step_3(preprocessed_bit_array)
        return self.step_4()

    def step_1(self):
        bit_array = bitarray(endian="big")
        bit_array.frombytes(self.input_string.encode("utf-8"))
        bit_array.append(1)
        while len(bit_array) % 512 != 448:
            bit_array.append(0)
        # go back to littler endian for ease
        return bitarray(bit_array, endian="little")

    def step_2(self, step_1_result):
        # get length of message in bits
        length = (len(self.input_string) * 8) % pow(2, 64)
        length_bit_array = bitarray(endian="little")
        length_bit_array.frombytes(struct.pack("<Q", length))
        result = step_1_result.copy()
        result.extend(length_bit_array)
        return result

    def step_3(self, step_2_result):
        # The total number of 32-bit words to process
        N = len(step_2_result) // 32
        # Process each block
        for chunk_index in range(N // 16):
            # Break the chunk into 16 words of 32 bits in list X.
            start = chunk_index * 512
            X = [step_2_result[start + (x * 32) : start + (x * 32) + 32] for x in range(16)]
            # Convert the `bitarray` objects to integers to prevent errors in the F,G,H,I functions
            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]
            # Simplify
            A = self.buffers["A"]
            B = self.buffers["B"]
            C = self.buffers["C"]
            D = self.buffers["D"]
            # Execute the four rounds with 16 operations each.
            for i in range(4 * 16):
                if 0 <= i <= 15:
                    k = i
                    s = [7, 12, 17, 22]
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    k = ((5 * i) + 1) % 16
                    s = [5, 9, 14, 20]
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    k = ((3 * i) + 5) % 16
                    s = [4, 11, 16, 23]
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]
                    temp = I(B, C, D)
                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, A)
                temp = rotate_left(temp, s[i % 4])
                temp = modular_add(temp, B)
                A = D
                D = C
                C = B
                B = temp
                print("Round", i+1, "A:", A, "B:", B, "C:", C, "D:", D)
            # Final Updated for this chunk
            self.buffers["A"] = modular_add(self.buffers["A"], A)
            self.buffers["B"] = modular_add(self.buffers["B"], B)
            self.buffers["C"] = modular_add(self.buffers["C"], C)
            self.buffers["D"] = modular_add(self.buffers["D"], D)
            print("Buffers:", self.buffers)
            print(f"Block {chunk_index + 1} done")

    def step_4(self):
        # Convert the buffers to little-endian to make it easier
        A = struct.unpack("<I", struct.pack(">I", self.buffers["A"]))[0]
        B = struct.unpack("<I", struct.pack(">I", self.buffers["B"]))[0]
        C = struct.unpack("<I", struct.pack(">I", self.buffers["C"]))[0]
        D = struct.unpack("<I", struct.pack(">I", self.buffers["D"]))[0]
        # return all the blocks joined together
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"

if __name__ == "__main__":
    print("Exactly 448 Bits: 56 characters")
    string1 = "This is aadityaa 21BCE1964 studying in VIT Chennai India"
    print("Input Message: ", string1)
    print("Hash:", MD5().hash(string1))

    print("\nLess than 448 Bits: 11 characters")
    string2 = "Aadityaa .N"
    print("Input Message: ", string2)
    print("Hash:", MD5().hash(string2))

    print("\nGreater than 448 bits: 118 characters")
    string3 = "This is Aadityaa Nagarajan 21BCE1964 studying in vit chennai India i like programming and this is a wonderfull world ."
    print("Input Message: ", string3)
    print("Hash:", MD5().hash(string3))