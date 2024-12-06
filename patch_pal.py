import toml

# constants
ORIGINAL_BINARY_PATH = "./.data/orig.bin"
PATCHES_PATH = "./.data/patches"

def get_current_binary_path():
    with open("./.data/path", "r") as file:
        return file.read()

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
        current_binary_path = get_current_binary_path()

        # Open both files in binary read mode
        with open(ORIGINAL_BINARY_PATH, "rb") as original_file, open(current_binary_path, "rb") as current_file:
            original_data: bytes = original_file.read()
            current_data: bytes = current_file.read()

        # Compare byte by byte and collect differences
        differences = []
        max_len = max(len(original_data), len(current_data))

        for offset in range(max_len):
            original_byte: int = original_data[offset] if offset < len(original_data) else 0
            current_byte: int = current_data[offset] if offset < len(current_data) else 0

            if original_byte != current_byte:
                differences.append(offset, f'{hex(current_byte & 0xFF).strip("0x"):0>2}')

        return differences if len(differences) > 0 else None

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error while comparing binaries: {e}")
        return None
   

def restore_binary(): # overwrites get_current_binary_path binary with ORIGINAL_BINARY_PATH
    pass

def apply_patch(patch):
    """
    Reads in patch data from a TOML file and applies it to the current binary.

    Args:
        patch (str): Path to the TOML patch file.
    """
    try:
        # Load the TOML file
        with open(patch, "r") as patch_file:
            patch_data = toml.load(patch_file)

        # Extract content section
        name = patch_data.get("name", "Unnamed Patch")
        description = patch_data.get("description", "No description provided.")
        content = patch_data.get("content", {})
        offsets = content.get("offsets", [])
        bytes_to_write = content.get("bytes", [])

        if not offsets or not bytes_to_write or len(offsets) != len(bytes_to_write):
            raise ValueError("Invalid content format: offsets and bytes must be non-empty lists of the same length.")

        # Open the current binary file in binary read/write mode
        current_binary_path = get_current_binary_path()
        with open(current_binary_path, "r+b") as binary_file:
            for offset, byte_string in zip(offsets, bytes_to_write):
                # Convert offset and byte string
                offset = int(offset)  # Ensure offset is an integer
                byte_data = bytes.fromhex(byte_string)

                # Seek to the offset and write the byte data
                binary_file.seek(offset)
                binary_file.write(byte_data)

        print(f"Patch '{name}' applied successfully: {description}")

    except Exception as e:
        print(f"Error applying patch: {e}")

def display_patches(): # reads in title/description info from each patch file and displays it
    pass

def run_binary():
    proc = subproccess.Popen([get_current_binary_path()])
    proc.wait()

def setup(): 
    # check if .data directory has been set up yet
    # if it has, return
    # if not:
    # create directory structure
    # ask user for path to current binary
    # copy current binary to ORIGINAL_BINARY_PATH
    # save path to current binary to "./.data/path"
    pass

def save_patch(patch_name: str, patches: list[tuple]): # compares ORIGINAL_BINARY_PATH to get_current_binary_path, saving differences to new patch file
    for patch in patches:
        print(f"")

def main():
    setup()

    # check diff, returns patch or null

    # if there is a diff
    while True:
        print("It looks like you have modified the binary as it does not match the original. What would you like to do?")
        print("1 - Save the modifications as a new patch and revert the changes")
        print("2 - Revert the changes")
        match int(input()):
            case 1:
                # save patch
                # overwrite current binary with original binary. restore_binary()
                break
            case 2:
                # overwrite current binary with original binary. restore_binary()
                break
            case _:
                print("Please enter a valid choice.")

    while True:
        # display patches
        # select patch
        while True:
            print("What do you want to do with this patch?")
            print("1 - run it")
            print("2 - edit it (this will modify your binary with the selected patch and then terminate for you to edit)")
            choice = input()
            if choice == 1:
                # apply_patch()
                run_binary()
                restore_binary()
                break
            elif choice == 2:
                # apply_patch
                exit()
            else:
                print("Please enter a valid choice.")


if __name__ == "__main__":
    main()
