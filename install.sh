#!/bin/bash

echo "If you wish to install the ghidra script, it will be installed to $HOME/ghidra_scripts"
echo "Install ghidra script? (Y/N)"
read answer

if [ "$answer" = "Y" ]; then
	cp ghidra_script.py $HOME/ghidra_scripts/PatchPal.py
fi

echo -e "#!/usr/bin/python3\n" > patchpal
chmod a+x patchpal
cat patch_pal.py >> patchpal
sudo mv patchpal /usr/local/bin
