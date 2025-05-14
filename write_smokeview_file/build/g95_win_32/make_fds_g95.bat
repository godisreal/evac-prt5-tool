@echo off

Title Building FDS for 32 bit Windows

make VPATH="..\..\Source2008" -f ..\..\makefile_2008 g95_win_32
pause