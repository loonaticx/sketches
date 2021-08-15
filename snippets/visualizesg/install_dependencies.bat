set /P PPYTHON_DIR=<PPYTHON_DIR
ps choco install graphviz
%PPYTHON_DIR%/ppython.exe -m pip install -r requirements.txt
pause