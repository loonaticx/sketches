# i was able to write this script faster than github desktop could do its freakin job

import os
import shutil
import sys
from pathlib import Path
import subprocess

# git restore phase_x/folder

selectedPhases = ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13', '14']

def restoreFolder(folder):
    # print(folder)
    param = [
        'restore',
        folder
    ]
    subprocess.run(["git"] + param)
    
def traverseFolder(folderDir):
    # Let folder be like phase_3/maps/whatever
    restoreFolder(folderDir)
    subcontents = os.listdir(folderDir)
    if len(subcontents) != 0:
        # We've got subcontent
        for content in subcontents:
            currentFolder = folderDir + '/' + content
            if os.path.exists(currentFolder) and not os.path.isfile(currentFolder):
                traverseFolder(currentFolder)

for phase in selectedPhases:
    phaseFolder = 'phase_%s' % phase
    if os.path.exists(phaseFolder):
        traverseFolder(phaseFolder)
        
