# Dictionary Checker

This project contains a script `check.py` that performs various checks on a dictionary file and a BIP-0039 word list.

## Files

- `check.py`: The main script that performs the checks.
- `src/dictionary.txt`: The dictionary file containing words and their corresponding numbers.
- `src/bip-0039.txt`: The BIP-0039 word list.
- `src/coolbit.json`: A JSON file containing a mapping of numbers to mnemonic words. (the conent of coolbit.json is copied from the repo https://github.com/CoolBitX-Technology/convertseed)

## Checks

The script performs the following checks:

1. **Duplicate Check**: Ensures there are no duplicate numbers or words in `src/dictionary.txt`.
2. **BIP-0039 Check**: Ensures all words in `src/dictionary.txt` are present in `src/bip-0039.txt`.
3. **Mnemonic Check**: Ensures the number-to-word mapping in `src/coolbit.json` matches the mapping derived from `src/dictionary.txt`.

## Usage

To run the checks, execute the script:

```sh
python check.py
```

# Mapping Generator
The main.py script generates mappings based on a secret.

Usage
To run the mapping generator, execute the script:
```sh
python main.py [--reverse true|false] [--mode n2n|w2w|n2w|w2n]
```

Arguments
- --reverse: choose to print out reverse mapping. Default is false.
- --mode: Mapping mode. Options are:
  - n2n: Number-to-number
  - w2w: Word-to-word
  - n2w: Number-to-word
  - w2n: Word-to-number

Example
```sh
python main.py --reverse=true --mode=n2w
```
This will generate a number-to-word mapping, reversed mapping.