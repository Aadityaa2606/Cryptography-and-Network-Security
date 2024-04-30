# SHA-512

The SHA hashing algorithm accepts inputs of varying lengths and produces a fixed-size output of 128 bits.

## Working of the SHA-512 Algorithm

The SHA-512 hashing algorithm works in the following way:

1. **Padding**: The input message is padded to make its length a multiple of 1024 bits.
2. **Initialization**: The SHA-512 algorithm initializes eight 64-bit variables.
3. **Processing**: The input message is processed in 80-word blocks.
4. **Output**: The final output is a 512-bit message digest.

## Pseudocode

The following pseudocode describes the working of the SHA-512 hashing algorithm:

```plaintext
SHA-512 (message)
  Initialize variables
  Append padding bits
  Process the message in 80-word blocks
  Output the message digest
```

## Inputs

The input to the MD5 hashing algorithm can be:

- Exactly 896 bits, which is equivalent to 56 characters.
- Less than 896 bits, which is less than 56 characters.
- More than 896 bits, which is more than 56 characters.

## Outputs

The output from the MD5 hashing algorithm can be:

- 1 block of 80 rounds.
- 2 blocks of 80 rounds each.
- More than 2 blocks, each of 80 rounds.

## Examples 

Consider the following input message:

```plaintext
"Hello, World!"
```

The SHA-512 hash of the input message is:

```plaintext
2c74fd17edafd80e8447b0d46741ee243b7eb74dd2149a0ab1b9246fb30382f27e853d8585719e0e67cbda0daa8f51671064615d645ae27acb15bfb1447f459b
```
