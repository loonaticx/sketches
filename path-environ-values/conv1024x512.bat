@echo off
setlocal enabledelayexpansion
set img=none
for %%x in (%*) do (
    set img=%%~x
    magick convert !img! -resize 1024 512 !img!
)

