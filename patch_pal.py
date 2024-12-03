# constants
ORIGINAL_BINARY_PATH = "./.data/orig.bin"
PATCHES_PATH = "./.data/patches"

def get_current_binary_path():
    with open("./.data/path", "r") as file:
        return file.read()

def check_diff(): # compare get_current_binary_path binary with ORIGINAL_BINARY_PATH binary. returns true if difference present
    pass

def restore_binary(): # overwrites get_current_binary_path binary with ORIGINAL_BINARY_PATH
    pass

def apply_patch(patch): # reads in patch data from patch file and writes it to get_current_binary_path
    pass

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

def save_patch(patch_name): # compares ORIGINAL_BINARY_PATH to get_current_binary_path, saving differences to new patch file
    pass

def main():
    setup()

    # check diff, returns patch or null

    # if there is a diff
    while True:
        print("It looks like you have modified the binary as it does not match the original. What would you like to do?")
        print("1 - Save the modifications as a new patch and revert the changes")
        print("2 - Revert the changes")
        choice = input()
        if choice == 1:
            # save patch
            # overwrite current binary with original binary. restore_binary()
            break
        elif choice == 2:
            # overwrite current binary with original binary. restore_binary()
            break
        else:
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
                # apply_patch
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
