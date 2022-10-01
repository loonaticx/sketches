@echo off
set dir=./phase_"

for %%G IN (3, 3.5, 4, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 13, 14) do multify -x -f %dir%%%G.mf"

pause