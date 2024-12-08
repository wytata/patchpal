#!/bin/bash

echo -e "#!/usr/bin/python3\n" > patchpal
chmod a+x patchpal
cat patch_pal.py >> patchpal
sudo mv patchpal /usr/local/bin
