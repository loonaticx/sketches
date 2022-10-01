@echo off

rem This will clear Panda3D's model cache.
rem This is useful when you want to see error info (eg "Texture cannot be found ....") when opening up bam/egg files again.
rem This can also potentially fix issues with models/textures not updating after modifying them.

for /d %%G in ("C:\Users\%username%\AppData\Local\Panda3D-*") do echo Removing %%G & rd /s /q %%G
