@echo off
setlocal enabledelayedexpansion
set img=none
for %%x in (%*) do (
    set img=%%~x
    magick convert "!img!" -resize 512 "!img!"
)
