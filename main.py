import hashlib
import hmac
import re
import argparse

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
    # Argument parsing
    parser = argparse.ArgumentParser(description="A program to shuffle and map numbers or words deterministically.")
    parser.add_argument("--reverse", type=str, choices=['true', 'false'], default='false', help="reverse the mapping or not.")
    parser.add_argument("--mode", type=str, choices=['n2n', 'w2w', 'n2w', 'w2n'], default='n2n', help="Mapping mode (n2n: number-to-number, w2w: word-to-word, etc.).")
    args = parser.parse_args()

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
            checksum_bytes = hashlib.sha256(secret.encode('utf-8')).digest()
            checksum_num = int.from_bytes(checksum_bytes, 'big')
            # Show only first 5 digits
            checksum_str = str(checksum_num)
            short_checksum = checksum_str[:5]
            print("Your secret's checksum:", short_checksum)
            
            confirm = input("Is this correct? (y/n): ").strip().lower()
            if confirm == 'y':
                break
            elif confirm == 'n':
                # User wants to re-enter secret
                continue
            else:
                print("Please enter 'y' or 'n'.")
                continue
        else:
            print("Error:", error)

    # Step 4: Use the above deterministic_secure_shuffle to shuffle securely and reproducibly
    newNumbers = deterministic_secure_shuffle(newNumbers, secret)

    # Step 5: if run with python main.py --reverse=True, sort by originalNumbers and print in reverse order
    output = zip(originalNumbers, newNumbers)
    if args.reverse == 'true':
        output = sorted(zip(newNumbers, originalNumbers), key=lambda x: x[0])

    # Step 6: Print the mapping depend on the mode
    print() # Print a newline for better readability
    for a, b in output:
        if args.mode == "n2n":
            print(f"{a} => {b}")
        elif args.mode == "w2w":
            print(f"{numberStrWordMap[a]} => {numberStrWordMap[b]}")
        elif args.mode == "n2w":
            print(f"{a} => {numberStrWordMap[b]}")
        elif args.mode == "w2n":
            print(f"{numberStrWordMap[a]} => {b}")

if __name__ == "__main__":
    main()