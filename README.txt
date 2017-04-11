This is skeleton for readme time until creation of properer installation file.

For anaconda installation we propose You usage of miniconda3.
Download links:

win64 - exe:
https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe

win32 - exe:
https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86.exe

linux64 - bash:
https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

linux32 - bash:
https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86.sh

macOSX64 - bash:
https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

#########URGENT#########
WE ADVICE YOU TO USE SUITABLE PATH COMMANDS IN .sh SCRIPT FOR FURTHER COMFORT OF CONDA USAGE

URL for instalation guide:
https://conda.io/docs/install/quick.html

environment_setup/environment.yml is an Anaconda env config file.
To use this, you need to(after installation of anaconda):

> conda env create -n pytnam -f environment.yml --force


Activate the new environment:

Linux, OS X:
>source activate pytnam

Windows:
>activate pytnam

Verify that the new environment was installed correctly:
>conda list

Tutorial for setting conda env in your IDE:
https://docs.continuum.io/anaconda/ide_integration