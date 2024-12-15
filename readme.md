# Dictionary Checker and Mapping Generator

This project contains scripts for checking a dictionary file against a BIP-0039 word list and generating mappings based on a secret.

## Background
In cyptocurrency, a wallet seed is often represented as a list of mnemonic words (also known as a mnemonic phrase). To make it secure, users are usually recommended to store the seed in a offline storage (e.g. a piece of paper or a steel plate).

However, it is possible that storage can be peeked by someone else. That's why it is important to use a passphrase to encrypt the seed.

In this project, we use a secret to generate a specific mapping that is used to encrypt the seed.

A w2w mapping (w2w mapping, a.k.a word to word mapping) is a list of mnemonic word and their corresponding new mnemonic word. For example, the mapping can be like this:

```text
abandon => alarm
ability => want
able => opinion
about => quick
...
```

If the true seed is `abandon ability able about ...`, the encrypted seed will be `alarm want opinion quick ...`.

User can then store the encrypted seed in a their trusted offline storage (e.g. a piece of paper or a steel plate) and put the offline storage to trusted places (e.g. family's house, bank's safe box). The main idea is that even if the offline storage is peeked by someone else, the wallet is still secure because the seed is encrypted.



## Files

- `check.py`: The main script that performs various checks.
- `main.py`: The script that generates mappings based on a secret.
- `src/dictionary.txt`: The dictionary file containing words and their corresponding numbers.
- `src/bip-0039.txt`: The BIP-0039 word list.
- `src/coolbit.json`: A JSON file containing a mapping of numbers to mnemonic words. (The content of `coolbit.json` is copied from the repo [CoolBitX-Technology/convertseed](https://github.com/CoolBitX-Technology/convertseed))

## Checks

The `check.py` script performs the following checks:

1. **Duplicate Check**: Ensures there are no duplicate numbers or words in `src/dictionary.txt`.
2. **BIP-0039 Check**: Ensures all words in `src/dictionary.txt` are present in `src/bip-0039.txt`.
3. **Mnemonic Check**: Ensures the number-to-word mapping in `src/coolbit.json` matches the mapping derived from `src/dictionary.txt`.

## Usage

To run the checks and the mapping generator, you can use the provided `Makefile`.

To run the checks, use the following command:

```sh
make check
```

To generate mappings based on a secret, use the following command:
```sh
make map
```

## Different Modes
### w2w
In this mode, the script will generate a word to word mapping based on the secret. 

### n2n
The CoolBitX wallet use numbers to represent mnemonic words. So for the users using CoolBitX wallet, they need to generate a number to number mapping based on the secret.

### w2n
In this mode, the script will generate a word to number mapping based on the secret. Then it will convert the word mapping to number mapping based on the CoolBitX mapping.

### n2w
In this mode, the script will generate a number to word mapping based on the secret. Then it will convert the number mapping to word mapping based on the CoolBitX mapping.

## Reverse Mapping
When the user wants to decrypt the seed, they can use the reverse mapping. In order words, if the user's stored encrypted seed is `alarm want opinion quick ...`, they can use the reverse mapping to get the true seed `abandon ability able about ...`.

```text
alarm => abandon
want => ability
opinion => able
quick => about
```

## Example
Suppose the secret is `this-is-a-secret-for-demo@202412`, the generated mapping is like this:
```text
abandon => enroll
ability => little
able => mammal
about => hope
above => barely
...
```
If the user's mnemonic seed is `abandon ability able about above ...`, the encrypted seed will be `enroll little mammal hope barely ...`.
And the user could then store the encrypted seed in a offline storage.

One day, if the user wants to recover the wallet, they can use the reverse mapping to get the true seed `abandon ability able about above ...`.

To use the script:
```sh
make map
```

output is like this:
```text
Do you want to reverse the mapping? (y/n): n
Enter the mode (n2n, w2w, n2w, w2n): w2w
Please enter a secret: this-is-a-secret-for-demo@202412
Your secret's checksum: 12513
Is this correct? (y/n): y
Mapping results have been written to .map-12513
```
