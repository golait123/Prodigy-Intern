def caesar_cipher(text, shift, mode='encrypt'):
    result = ''
    for char in text:
        if char.isalpha():
            shift_amount = shift if mode == 'encrypt' else -shift
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift_amount) % 26 + base)
        else:
            result += char
    return result

def main():
    print("Welcome to Caesar Cipher Tool!")
    mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").strip().lower()
    if mode not in ['encrypt', 'decrypt']:
        print("Invalid mode selected.")
        return

    text = input("Enter your message: ")
    try:
        shift = int(input("Enter shift value (e.g., 3): "))
    except ValueError:
        print("Shift must be an integer.")
        return

    output = caesar_cipher(text, shift, mode)
    print(f"\nResult ({mode}ed): {output}")

if __name__ == '__main__':
    main()