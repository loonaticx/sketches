@echo off
rmdir /s /q sdf
mkdir sdf
echo Generating signed distance field text > sdf/info.txt
egg-mkfont -sdf Comedy.ttf -o sdf/output.egg 1>> sdf/info.txt 2>>&1

rmdir /s /q nopal
mkdir nopal
echo Generating with no palette > nopal/info.txt
egg-mkfont -nopal Comedy.ttf -o nopal/output.egg 1>> nopal/info.txt 2>>&1

rmdir /s /q hq
mkdir hq
echo Generating using 100 pixels per unit (default is 40) > hq/info.txt
echo Generating using size 40 point font (default is 10) >> hq/info.txt
egg-mkfont -ppu 100 -ps 40 Comedy.ttf -o hq/output.egg 1>> hq/info.txt 2>>&1

rmdir /s /q gp
mkdir gp
egg-mkfont -gp %03d Comedy.ttf -o gp/output.egg 1> gp/info.txt 2>&1
rem Different results happen if you append the -nopal flag here. (Not suppose to be using this without nopal flag technically)

rmdir /s /q unicode
mkdir unicode
echo Generating currency Unicode symbols in Times New Roman font. > unicode/info.txt
echo https://www.utf8-chartable.de/unicode-utf8-table.pl?utf8=0x >> unicode/info.txt
egg-mkfont -chars 0x20A0-0x20BF times.ttf -o unicode/output.egg 1>> unicode/info.txt 2>>&1

rmdir /s /q default
mkdir default
echo Generating with no special flags. > default/info.txt
egg-mkfont Comedy.ttf -o default/output.egg 1>> default/info.txt 2>>&1

pause