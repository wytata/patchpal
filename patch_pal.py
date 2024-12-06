import toml
import os
import sys
import shutil

# constants
ORIGINAL_BINARY_PATH = "./.data/orig.bin"
PATCHES_PATH = "./.data/patches"
user_binary = ""

def get_current_binary_path():
    with open("./.data/path", "r") as file:
        return file.read()

def get_diff() -> list[tuple] | None: # compare get_current_binary_path binary with ORIGINAL_BINARY_PATH binary. returns true if difference present
    pass 

def restore_binary(): # overwrites get_current_binary_path binary with ORIGINAL_BINARY_PATH
    shutil.copy(ORIGINAL_BINARY_PATH, user_binary)

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
    for root, dirs, files in os.walk(PATCHES_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            # Load the TOML file
            with open(file, "r") as patch_file:
                patch_data = toml.load(patch_file)

            # Extract content section
            name = patch_data.get("name", "Unnamed Patch")
            description = patch_data.get("description", "No description provided.")

            print(name + "\n" + description + "\n\n-----\n\n")


def run_binary():
    proc = subproccess.Popen([get_current_binary_path()])
    proc.wait()

def setup():
    if os.path.isdir(".data"):
        return

    try:
        absolute_file_path = os.path.abspath(user_binary)
        directory = os.path.join(os.path.dirname(absolute_file_path), ".data")
        os.mkdir(directory)
        os.mkdir(directory + "/patches")
        original_bin_path = directory + "/orig.bin"
        shutil.copy(absolute_file_path, original_bin_path)
        sys.exit(0)

    except Exception as e:
        print(e)
    # check if .data directory has been set up yet
    # if it has, return
    # if not:
    # create directory structure
    # ask user for path to current binary
    # copy current binary to ORIGINAL_BINARY_PATH
    # save path to current binary to "./.data/path"

def save_patch(patch_name: str, description: str, patches: list[tuple]) -> None: # compares ORIGINAL_BINARY_PATH to get_current_binary_path, saving differences to new patch file
    file: str = patch_name.replace(' ', '-')
    filepath = os.path.join(PATCHES_PATH, f"{file}.ps")

    tmp: int = 15
    hex_str: str = hex(tmp & 0xFF).strip('0x')

    print(f"{hex_str:0>2}")

    with open(filepath, "a+") as patch_file:
        patch_file.write(f'name = "{patch_name}"\n')
        patch_file.write(f'description = "{description}"\n')
        patch_file.write('\n')
        patch_file.write("[content]\n")

        offsets, bytes = zip(*patches)
        patch_file.write(f"offsets = [{', '.join(offsets)}]\n")
        patch_file.write(f"bytes = [{', '.join(bytes)}]\n")

def main():
    # grab args
    if (len(sys.argv) != 2):
        print("Please provide the path to your binary as a command line argument.");
    user_binary = sys.argv[1]
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
                save_patch(get_diff())
                # overwrite current binary with original binary. 
                restore_binary()
                break
            case 2:
                # overwrite current binary with original binary. 
                restore_binary()
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
