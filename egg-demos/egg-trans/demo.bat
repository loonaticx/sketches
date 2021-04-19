rmdir /S /Q output
mkdir output
cd input
egg-trans -N -c -C -mesh -no -t -td ../output/ -te jpg carnation.egg -o ../output/carnation.egg
pause