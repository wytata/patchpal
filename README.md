# Patch Pal

Patch Pal is a reverse engineering tool for managing executable patches. The tool makes it easy to keep track of various patches that a reverser may make to a binary, keeping them from having to keep multiple copies of a potentially large binary.
This is done by maintaining binary patches as patch-set files, which maintain offsets and corresponding byte values that convey what the patches are and where they are made. While simple in design, the tool can make reverse engineering project 
simpler and more organized.

The install script installs both the patch_pal script and, optionally, the Ghidra plugin script. The usage of the main patch_path script is as follows:
```shell
patchpal <path_to_binary>
```
This of course requires the install script to have run first.

The first time the program is run, the project directory structure will be set up. In the directory of the binary program, a hidden directory will be created, maintaining the user-created patches, as well as a copy of the original binary. 
After the first run, the user will be prompted to select a patch to apply to their program from the existing patches. If the binary has been modified in any way, the program will first warn the user, allowing them to optionally save the 
modifications as a patch file in their project structure. This is the typical workflow for a reverser making direct modifications to their binary using programs such as radare2. For a Ghidra user, patch files can be generated through Ghidra,
while the process of running the binary with patches is otherwise the same through the Patch Pal command line interface.

Demonstrations of the tool can be found in the test directory, which contains example directories that show the project structure resulting from using the tool as well as videos in which the tool is used to create these directories.

We hope you enjoy Patch Pal. Happy hacking!
