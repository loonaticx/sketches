@echo off

rem Generate a hard link between two directories, a quick and easy way to tie a bundle of phase folders to a different project instead of having to copy&paste them.
rem An alternative (and safer way) of doing this is to edit your Panda's Config.prc and set the model-path to where ever appropriate.
rem Note that this script will replace all data within any "phase_x" folders in the target directory with the ones located in the source directory.
rem This will not necessarily "copy" all contents, but instead make a hard link or "junction" (like a shortcut) to that directory.

rem The example shown below will make a junction link of phase folders located in the C:\Panda3d-1.11.0\bin folder and place it in the C:\Data\Toontown\resources folder.
rem src dir --> target dir

echo WARNING: I WOULD BE EXTREMELY CAUTIOUS WHEN USING THIS SCRIPT!!
echo DATA LOST IS IMMINENT IF THE TARGET AND SRC DIR ARE IMPROPERLY CONFIGURED!!

echo .

echo \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ 
set target-dir="C:\Data\Toontown\resources\phase_
echo %target-dir%

echo .

echo \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ EDIT ME \/ 
set src-dir="C:\Panda3D-1.11.0\bin\phase_
echo %src-dir%

echo .

echo In order to use this script, remove "rem" off the line below me in the batch file when you have PROPERLY CONFIGURED THE TARGET AND SOURCE DIR.
rem for %%G IN (3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13, 14) do mklink /J %target-dir%%%G" %src-dir%%%G"

pause