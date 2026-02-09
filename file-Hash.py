import hashlib
import json
import os

hashSave="hashes.json"

def generate_hash_table(directory):
    hash_table = traverse_directory(directory)

    with open("hashes.json", "w") as f:
        json.dump(hash_table, f, indent=4)

    print("Hash table generated.")

def traverse_directory(directory):
    hash_table = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = hash_file(filepath)
            if file_hash:
                hash_table[filepath] = file_hash

    return hash_table


def hash_file(filepath):
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Could not hash {filepath}: {e}")
        return None

def verify_hashes(directory):
    try:
        with open(hashSave, "r") as f:
            stored_hashes = json.load(f)
    except FileNotFoundError:
        print("No hash table found. Generate one first.")
        return

    for filepath, old_hash in stored_hashes.items():
        if not os.path.exists(filepath):
            print(f"Can't Find: {filepath}")
            continue

        new_hash = hash_file(filepath)

        if new_hash == old_hash:
            print(f"Valid: {filepath}")
        else:
            print(f"Invalid: {filepath}")


def main():
    print("1 - Generate new hash table")
    print("2 - Verify hashes")

    choice = input("Enter your choice: ")

    directory = input("Enter directory path: ")

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    if choice == "1":
        generate_hash_table(directory)
        print(hashSave)
    elif choice == "2":
        verify_hashes(directory)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
