import toml
import os
import sys
import shutil
import subprocess

# constants
ORIGINAL_BINARY_PATH = "/.data/orig.bin"
PATCHES_PATH = "/.data/patches"
user_binary = ""
user_working_directory = ""

def get_diff() -> list[tuple] | None:
    """
    Compares the binary contents of the current binary file and the original binary file.
    
    Returns:
        list[tuple]: A list of tuples where each tuple contains the offset and 
                     the pair of differing bytes (original, current).
                     Example: [(offset1, (original_byte, current_byte)), ...]
        None: If there are no differences.
    """
    try:
        current_binary_path = user_binary

        # Open both files in binary read mode
        with open(user_working_directory + ORIGINAL_BINARY_PATH, "rb") as original_file, open(current_binary_path, "rb") as current_file:
            original_data: bytes = original_file.read()
            current_data: bytes = current_file.read()

        # Compare byte by byte and collect differences
        differences = []
        max_len = max(len(original_data), len(current_data))

        for offset in range(max_len):
            original_byte: int = original_data[offset] if offset < len(original_data) else 0
            current_byte: int = current_data[offset] if offset < len(current_data) else 0

            if original_byte != current_byte:
                differences.append((offset, f'{hex(current_byte & 0xFF).strip("0x"):0>2}'))

        return differences if len(differences) > 0 else None

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error while comparing binaries: {e}")
        return None
   

def restore_binary(): # overwrites get_current_binary_path binary with ORIGINAL_BINARY_PATH
    shutil.copy(user_working_directory + ORIGINAL_BINARY_PATH, user_binary)

def apply_patch(patch):
    """
    Reads in patch data from a TOML file and applies it to the current binary.

    Args:
        patch (str): Path to the TOML patch file.
    """
    try:
        # Ensure the patch file path is valid
        if not patch or not isinstance(patch, (str, bytes, os.PathLike)):
            print(f"Error: Invalid patch file path provided: {patch}")
            return

        # Ensure the patch file exists
        if not os.path.isfile(patch):
            print(f"Error: Patch file '{patch}' not found.")
            return

        # Load the TOML file
        patch_data = None
        try:
            with open(patch, "r") as patch_file:
                patch_data = toml.load(patch_file)
        except toml.TomlDecodeError as e:
            print(f"Error: Failed to parse the TOML file '{patch}' - {e}")
            return
        except Exception as e:
            print(f"Error: Unable to open or read the patch file '{patch}' - {e}")
            return

        # Extract patch metadata and content
        name = patch_data.get("name", "Unnamed Patch")
        description = patch_data.get("description", "No description provided.")
        content = patch_data.get("content", {})
        offsets = content.get("offsets", [])
        bytes_to_write = content.get("bytes", [])

        # Validate the content structure
        if not isinstance(offsets, list) or not isinstance(bytes_to_write, list):
            print("Error: 'offsets' and 'bytes' must be lists.")
            return
        if len(offsets) != len(bytes_to_write):
            print("Error: 'offsets' and 'bytes' lists must be of the same length.")
            return
        if not offsets or not bytes_to_write:
            print("Error: Patch content is empty or invalid.")
            return

        # Validate the binary file path
        if not user_binary or not isinstance(user_binary, (str, bytes, os.PathLike)):
            print(f"Error: Invalid binary file path provided: {user_binary}")
            return

        if not os.path.isfile(user_binary):
            print(f"Error: The binary file '{user_binary}' does not exist.")
            return

        # Open the current binary file in binary read/write mode
        try:
            with open(user_binary, "r+b") as binary_file:
                for offset, byte_string in zip(offsets, bytes_to_write):
                    try:
                        # Convert offset and byte string
                        offset = int(offset)  # Ensure offset is an integer
                        byte_data = bytes.fromhex(byte_string)  # Convert hex string to bytes

                        # Check if the offset is within the file bounds
                        binary_file.seek(0, os.SEEK_END)
                        file_size = binary_file.tell()
                        if offset < 0 or offset >= file_size:
                            print(f"Warning: Offset {offset} is out of bounds for the binary file.")
                            continue

                        # Seek to the offset and write the byte data
                        binary_file.seek(offset)
                        binary_file.write(byte_data)
                    except ValueError as ve:
                        print(f"Error: Invalid offset or byte format in patch - {ve}")
                    except Exception as e:
                        print(f"Error: Failed to apply patch at offset {offset} - {e}")
        except IOError as ioe:
            print(f"Error: Unable to open or write to the binary file '{user_binary}' - {ioe}")
            return

        print(f"Patch '{name}' applied successfully: {description}")

    except Exception as e:
        print(f"An unexpected error occurred while applying the patch: {e}")


def display_patches(): # reads in title/description info from each patch file and displays it
    if os.listdir(user_working_directory + PATCHES_PATH) == []:
        print("It looks like you don't yet have any patches. Get to reversing!")
        sys.exit(1)

    patch_choices = {}
    for root, dirs, files in os.walk(user_working_directory + PATCHES_PATH):
        for i, file in enumerate(files):
            file_path = os.path.join(root, file)
            patch_choices[i] = file_path
            # Load the TOML file
            with open(file_path, "r") as patch_file:
                patch_data = toml.load(patch_file)

            # Extract content section
            name = patch_data.get("name", "Unnamed Patch")
            description = patch_data.get("description", "No description provided.")

            print(str(i + 1) + ". " + name + "\n" + description + "\n\n-----\n\n")

    patch_choice = input("Input a number to select a patch (or q to quit): ")
    if patch_choice == 'q':
        exit()
    while not patch_choice.isnumeric():
        patch_choice = input("Input a number to select a patch (or q to quit): ")
        if patch_choice == 'q':
            exit()

    try:
        print(patch_choices[int(patch_choice)-1])
        return patch_choices[int(patch_choice)-1]
    except Exception as e:
        return None


def run_binary():
    proc = subprocess.Popen([user_binary, *sys.argv[2:]])
    proc.wait()

def setup():
    if os.path.isdir(".data"):
        return

    try:
        directory = os.path.join(user_working_directory, ".data")
        os.mkdir(directory)
        os.mkdir(directory + "/patches")
        original_bin_path = directory + "/orig.bin"
        shutil.copy(user_binary, original_bin_path)
        print("Your patch pal project directory has been set up. You can now create patches!")

    except Exception as e:
        print(e)

def save_patch(patch_name: str, description: str | None, patches: list[tuple]) -> None: # compares ORIGINAL_BINARY_PATH to get_current_binary_path, saving differences to new patch file
    file: str = patch_name.replace(' ', '-')
    filepath = os.path.join(user_working_directory + PATCHES_PATH, f"{file}.ps")

    with open(filepath, "a+") as patch_file:
        patch_file.write(f'name = "{patch_name}"\n')
        if (description): 
            patch_file.write(f'description = "{description}"\n')
        patch_file.write('\n')
        patch_file.write("[content]\n")

        offsets, bytes = zip(*patches)
        patch_file.write(f"offsets = [{', '.join([f"{off}" for off in offsets])}]\n")
        patch_file.write(f"bytes = [{', '.join([f'"{byte}"' for byte in bytes])}]\n")

def main():

    global user_binary
    global user_working_directory
    # grab args
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print("Usage: patchpal <binary_file_to_reverse>")

    user_binary = os.path.abspath(sys.argv[1])
    print("USER BINARY GIVEN: " + user_binary)
    user_working_directory = os.path.dirname(user_binary)

    setup()

    diffs: list[tuple] | None = get_diff()
    if diffs:
        while True:
            print("It looks like you have modified the binary as it does not match the original. What would you like to do?")
            print("1 - Save the modifications as a new patch and revert the changes")
            print("2 - Revert the changes")
            match input():
                case '1':
                    # save patch
                    name: str = input("What would you like to name this patch? ")
                    opt_description: str = input("Message (optional) ")
                    description: str | None = opt_description if opt_description != "" else None

                    save_patch(name, description, diffs)
                    # overwrite current binary with original binary. 
                    restore_binary()
                    break
                case '2':
                    # overwrite current binary with original binary. 
                    restore_binary()
                    break
                case _:
                    print("Please enter a valid choice.")

    print("\n\nWelcome to PatchPal!\n\nHere are your current patches:\n")

    while True:
        # display patches
        patch_file = display_patches()
        # select patch
        while True:
            print("What do you want to do with this patch?")
            print("1 - run it")
            print("2 - edit it (this will modify your binary with the selected patch and then terminate for you to edit)")
            choice = input()
            if choice == '1':
                apply_patch(patch_file)
                run_binary()
                restore_binary()
                break
            elif choice == '2':
                apply_patch(patch_file)
                exit()
            elif choice == "q":
                exit()
            else:
                print("Please enter a valid choice.")


if __name__ == "__main__":
    main()
