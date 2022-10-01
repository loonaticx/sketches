@echo off
setlocal enabledelayedexpansion
set img=none
for %%x in (*.png) do (
    set img=%%~x
    echo !img!
    convert !img! -strip  !img!
)

