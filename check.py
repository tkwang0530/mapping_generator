# read dictionary from src/dictionary.txt and check if there are any duplicates numbers or words

def checkDuplicate():
    print('Checking duplicates...')
    with open('src/dictionary.txt', 'r') as f:
        lines = f.readlines()
        numSet = set()
        wordSet = set()
        for line in lines:
            number, word = line.split()
            if word == "English":
                print(number)
            if number in numSet:
                print('Duplicate number:', number)
            else:
                numSet.add(number)

            if word in wordSet:
                print('Duplicate word:', word)
            else:
                wordSet.add(word)
        print('Total numbers:', len(numSet))
        print('Total words:', len(wordSet))
        # failed if there are duplicates
        if len(numSet) != len(lines) or len(wordSet) != len(lines) or len(numSet) != len(wordSet) or len(numSet) != 2048:
            print('failed checkDuplicate !!')
        else:
            print("pass checkDuplicate !!")

def checkWithBIP39():
    print('Checking duplicates with BIP39...')
    bip39 = set()
    with open('src/bip-0039.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            word = line.strip()
            bip39.add(word)

    with open('src/dictionary.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            _, word = line.split()
            if word not in bip39:
                print('unknown word:', word)
                # failed if there are unknown words
                print('failed checkWithBIP39 !!')
                return

    print("pass checkWithBIP39 !!")
if __name__ == '__main__':
    checkDuplicate()
    print("------------------------------")
    checkWithBIP39()