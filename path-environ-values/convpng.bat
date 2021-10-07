@echo off
setlocal enabledelayedexpansion
set img = none
for %%x in (%*) do (
    set img=%%~x
    set conv=!img:jpg=png!
    magick convert !img! !conv!
    del %img%
)
