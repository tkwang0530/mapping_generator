import hashlib
import hmac
import re

def deterministic_secure_shuffle(arr, secret):
    # Use the secret to generate a key
    key = hashlib.sha256(secret.encode('utf-8')).digest()
    
    # Apply Fisher-Yates Shuffle, using HMAC(key, index) to generate random numbers
    # The array will be shuffled in place
    for i in range(len(arr)-1, 0, -1):
        # Use i as the counter, generate a cryptographic hash value using HMAC(key, i)
        counter_bytes = i.to_bytes((i.bit_length() + 7) // 8, 'big', signed=False)
        if not counter_bytes:  # If i=0, to_bytes would be empty, handle manually
            counter_bytes = b'\x00'
        
        digest = hmac.new(key, counter_bytes, hashlib.sha256).digest()
        # Extract a portion of the digest and convert it to an integer to determine the swap index
        rnd_int = int.from_bytes(digest, 'big')
        
        j = rnd_int % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


def validate_secret(secret):
    # Rule 1: Length must be at least 20, and not exceed 36
    if len(secret) < 20:
        return "secret must be at least 20 characters long."
    if len(secret) > 36:
        return "secret must not exceed 36 characters."

    # Rule 2: Must contain at least three types of characters
    char_types = 0
    if re.search(r'[A-Z]', secret):  # At least one uppercase letter
        char_types += 1
    if re.search(r'[a-z]', secret):  # At least one lowercase letter
        char_types += 1
    if re.search(r'[0-9]', secret):  # At least one number
        char_types += 1
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|]', secret):  # At least one special symbol
        char_types += 1
    if char_types < 3:
        return "secret must include at least three types of characters (uppercase letters, lowercase letters, numbers, or special symbols)."

    # Rule 3: Must not contain whitespace or special escape characters
    if re.search(r'\s', secret):
        return "secret must not contain whitespace or escape characters."

    # Passed all checks
    return None

# Main function
def main():
    isReverse = False
    # get the reverse and mode arguments
    while True:
        print("Select the operation:")
        print("1. Generate secret dictionary to encrypt mnemonic")
        print("2. Generate reverse secret dictionary to recover mnemonic")
        answer = input("Enter the number corresponding to the operation (1 or 2): ").strip()
        if answer == '1':
            isReverse = False
            break
        elif answer == '2':
            isReverse = True
            break
        else:
            print("Please enter '1' or '2'.")

    while True:
        print("Select the mode:")
        print("1. n2n (Number-to-number)")
        print("2. w2w (Word-to-word)")
        print("3. n2w (Number-to-word)")
        print("4. w2n (Word-to-number)")
        modeInput = input("Enter the number corresponding to the mode (1, 2, 3, 4): ").strip()
        if modeInput == '1':
            modeInput = 'n2n'
            break
        elif modeInput == '2':
            modeInput = 'w2w'
            break
        elif modeInput == '3':
            modeInput = 'n2w'
            break
        elif modeInput == '4':
            modeInput = 'w2n'
            break
        else:
            print("Please enter '1', '2', '3', or '4'.")

    # Step 1: Read data from the file, also store to the numberStrWordMap
    with open('src/dictionary.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    numberStrWordMap = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        numStr, word = line.split(maxsplit=1)
        entries.append(numStr)
        numberStrWordMap[numStr] = word

    # Step 2: Sort to obtain originalNumbers
    originalNumbers = sorted(entries)
    # Step 3: Create a copy as newNumbers
    newNumbers = originalNumbers[:]

    # Prompt the user to enter a secret
    while True:
        secret = input("Please enter a secret: ")
        error = validate_secret(secret)
        if error is None:
            # Compute checksum (numeric)
            checksumBytes = hashlib.sha256(secret.encode('utf-8')).digest()
            checksumNum = int.from_bytes(checksumBytes, 'big')
            # Show only first 5 digits
            checksumStr = str(checksumNum)
            shortChecksum = checksumStr[:5]
            print("Your secret's checksum:", shortChecksum)
            
            confirm = input("Is this correct? (y/n): ").strip().lower()
            if confirm == 'y':
                break
            elif confirm == 'n':
                # User wants to re-enter secret
                continue
            else:
                print("Please enter 'y' or 'n' to confirm.")
                continue
        else:
            print("Error:", error)

    # Step 4: Use the above deterministic_secure_shuffle to shuffle securely and reproducibly
    newNumbers = deterministic_secure_shuffle(newNumbers, secret)

    # Step 5: if user wants to reverse the mapping, print the pairs (new, original) instead of (original, new)
    output = zip(originalNumbers, newNumbers)
    if isReverse:
        output = sorted(zip(newNumbers, originalNumbers), key=lambda x: x[0])

    # Step 6: Print the mapping depend on the mode
    outputLines = []
    for a, b in output:
        if modeInput == "n2n":
            outputLines.append(f"{a} => {b}")
        elif modeInput == "w2w":
            outputLines.append(f"{numberStrWordMap[a]} => {numberStrWordMap[b]}")
        elif modeInput == "n2w":
            outputLines.append(f"{a} => {numberStrWordMap[b]}")
        elif modeInput == "w2n":
            outputLines.append(f"{numberStrWordMap[a]} => {b}")

    # Write to file named ".map-{5 checksum digits}"
    if shortChecksum is not None:
        filename = f".map-{shortChecksum}"
        with open(filename, 'w', encoding='utf-8') as f:
            for line in outputLines:
                f.write(line + '\n')
        print(f"Mapping results have been written to {filename}")

if __name__ == "__main__":
    main()