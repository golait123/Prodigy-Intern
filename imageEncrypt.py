from PIL import Image, ImageChops
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog


# --- Step 1: File Picker ---
def choose_image_file(prompt="Select an image"):
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title=prompt,
            filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp")]
        )
        if not file_path:
            raise Exception("No file selected.")
        return file_path
    except:
        print("❌ Popup failed or cancelled.")
        return input("Enter full image path manually: ").strip()


# --- Step 2: Pixel Operations ---
def apply_operation(pixels, key, operation, mode='encrypt'):
    if operation == 'XOR':
        return pixels ^ key
    elif operation == 'ADD':
        return (pixels + key) % 256 if mode == 'encrypt' else (pixels - key) % 256
    elif operation == 'SUBTRACT':
        return (pixels - key) % 256 if mode == 'encrypt' else (pixels + key) % 256
    elif operation == 'MULTIPLY':
        if mode == 'encrypt':
            return (pixels * key) % 256
        else:
            try:
                inv_key = pow(key, -1, 256)
                return (pixels * inv_key) % 256
            except ValueError:
                raise ValueError("Use an odd key (has mod inverse under 256).")
    else:
        raise ValueError("❌ Invalid operation selected.")


# --- Step 3: Flip ---
def swap_pixels(pixels):
    return np.flip(pixels, axis=1)


# --- Encrypt ---
def encrypt_image(input_path, output_path, key, operation):
    img = Image.open(input_path)
    pixels = np.array(img)
    manipulated = apply_operation(pixels, key, operation, mode='encrypt')
    manipulated = swap_pixels(manipulated)
    Image.fromarray(manipulated.astype('uint8')).save(output_path)
    print(f"🔐 Encrypted image saved to: {output_path}")


# --- Decrypt ---
def decrypt_image(input_path, output_path, key, operation):
    img = Image.open(input_path)
    pixels = np.array(img)
    manipulated = swap_pixels(pixels)
    original = apply_operation(manipulated, key, operation, mode='decrypt')
    Image.fromarray(original.astype('uint8')).save(output_path)
    print(f"🔓 Decrypted image saved to: {output_path}")


# --- Verification ---
def compare_images(original_path, decrypted_path):
    img1 = Image.open(original_path).convert("RGB")
    img2 = Image.open(decrypted_path).convert("RGB")

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    if img1.size != img2.size:
        print("❌ Size mismatch between images.")
        return

    total_pixels = arr1.size
    diff_pixels = np.count_nonzero(arr1 != arr2)
    match_pixels = total_pixels - diff_pixels
    match_percent = (match_pixels / total_pixels) * 100

    print(f"\n📊 Verification Report:")
    print(f"   Total Pixels     : {total_pixels}")
    print(f"   Matching Pixels  : {match_pixels}")
    print(f"   Difference Pixels: {diff_pixels}")
    print(f"   Match Percentage : {match_percent:.2f}%")

    diff_img = ImageChops.difference(img1, img2)
    diff_img.save("difference.png")
    print("🖼  Difference image saved as: difference.png")


# --- Main ---
def main():
    print("🖼 Step 1: Select your image file to begin.")
    input_path = choose_image_file("Select the image you want to encrypt/decrypt")
    if not os.path.exists(input_path):
        print("❌ File not found.")
        return

    # Step 2: Now ask the user for the action
    print("\n📦 Step 2: Choose Action")
    action = input("Do you want to (E)ncrypt or (D)ecrypt the image? ").strip().upper()

    output_path = input("Enter output image filename (e.g., result.png): ").strip()

    try:
        key = int(input("Enter numeric key (1-255): "))
        if not (1 <= key <= 255):
            raise ValueError
    except:
        print("❌ Invalid key.")
        return

    print("\n🎛 Step 3: Choose Pixel Operation")
    print("1. XOR")
    print("2. ADD")
    print("3. SUBTRACT")
    print("4. MULTIPLY")
    op_choice = input("Enter choice (1-4): ").strip()
    operations = {'1': 'XOR', '2': 'ADD', '3': 'SUBTRACT', '4': 'MULTIPLY'}
    operation = operations.get(op_choice)

    if not operation:
        print("❌ Invalid operation.")
        return

    try:
        if action == 'E':
            encrypt_image(input_path, output_path, key, operation)
        elif action == 'D':
            decrypt_image(input_path, output_path, key, operation)

            verify = input("🔍 Do you want to verify with the original image? (y/n): ").strip().lower()
            if verify == 'y':
                original_path = choose_image_file("Select the original image for verification")
                if os.path.exists(original_path):
                    compare_images(original_path, output_path)
                else:
                    print("❌ Original file not found.")
        else:
            print("❌ Invalid action selected.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
