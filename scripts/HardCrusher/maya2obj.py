"""
file -force -type "OBJexport" -exportAll "test.obj"

mayabatch -file AA_test.mb -command "file -force -type \"OBJexport\" -exportAll \"test2.obj\"" 
"""
progs = [
    '-file',
    'fileName',
    '-command',
]

import subprocess
import os
import time
import sys
import psutil
import argparse

# todo:
#   custom maya arg(s) incl. file convert (bam2maya, etc.)
#   support for panda args, i.e. with bam2egg -h
#   warn the user if the maya2egg_server / client is missing so we dont run into an infinite loop

"""
 # Argument Handler #
 Example usage: convert.py --egg2maya --mayaver 2016 -r -v
"""
parser = argparse.ArgumentParser()

parser.add_argument(
    '--all-phases',
    '--all_phases',
    action = 'store_true',
    help = 'Convert all phase files folders. (3 to 14)'
)
parser.add_argument(
    '--selected_phases',
    '--phase',
    action = 'extend',
    nargs = '+',
    type = str,
    metavar = '3 3.5 4',
    help = 'List phase files folders to convert.'
)
parser.add_argument(
    '--selected_folders',
    '--folder',
    '--folders',
    action = 'extend',
    nargs = '+',
    type = str,
    metavar = 'models/',
    help = 'List of folders with subfolders to convert.'
)
parser.add_argument(
    '--rootonly',
    '--root',
    action = 'store_true',
    help = 'Just convert files in the root of the working directory.'
)
parser.add_argument(
    '--bindir',
    '-bin',
    '-b',
    action = 'store',
    type = str,
    help = 'Set folder path to desired Panda3D bin location',
    default = "bin/"
)
parser.add_argument(
    '--fromfile',
    '--file',
    '-f',
    action = 'store_true',
    help = 'Use this flag to read the path from the PANDA_BIN_PATH folder.'
)

## Bam
parser.add_argument(
    '--bam2egg',
    '--to_egg',
    '--to-egg',
    action = 'store_true',
    help = 'Convert BAM file(s) into EGG file(s).'
)
parser.add_argument(
    '--egg2bam',
    '--to_bam',
    '--to-bam',
    action = 'store_true',
    help = 'Convert EGG file(s) into BAM file(s).'
)

## Maya
parser.add_argument(
    '--egg2maya',
    action = 'store_true',
    help = 'Convert EGG file(s) into Maya Binary files.'
)
parser.add_argument(
    '--egg2maya_legacy',
    action = 'store_true',
    help = 'Convert EGG file(s) into Maya Binary files. [LEGACY]'
)

parser.add_argument(
    '--maya2egg',
    action = 'store_true',
    help = 'Convert Maya Binary file(s) into EGG files.'
)
parser.add_argument(
    '--maya2egg_legacy',
    action = 'store_true',
    help = 'Convert Maya Binary files into EGG file(s). [LEGACY]'
)
parser.add_argument(
    '--mayaver',
    '--mayaversion',
    '-mv',
    action = 'store',
    nargs = '?',
    type = str,
    default = '2016',
    metavar = 'MayaVersion',
    help = 'Use specific maya version. (Default is 2016)'
)

## Obj
parser.add_argument(
    '--obj2egg',
    action = 'store_true',
    help = 'Convert OBJ files into EGG files.'
)
parser.add_argument(
    '--egg2obj',
    action = 'store_true',
    help = 'Convert EGG files into OBJ files.'
)

## Fbx
parser.add_argument(
    '--fbx2egg',
    action = 'store_true',
    help = 'Convert FBX files into EGG files.'
)
parser.add_argument(
    '--egg2fbx',
    action = 'store_true',
    help = 'Convert EGG files into FBX files.'
)

## Misc
parser.add_argument(
    '--verbose',
    '-v',
    action = 'store_true',
    help = 'Enable verbose output.'
)
parser.add_argument(
    '--overwrite',
    '-o',
    action = 'store_true',
    help = 'Overwrite preexisting files.'
)
parser.add_argument(
    '--recursive',
    '-r',
    action = 'store_true',
    help = 'Convert all folders in the directory, recursively.'
           ' Typically used if there are models outside of "phase" folders.'
)

args = parser.parse_args()

### End of argparse configuring ###

# If the user gave us particular folders, let's not consider them to be phase files.
selectedFolders = args.selected_folders

# Config #
# mayaArgs = "-a -m" ?
allFiles = []

if not selectedFolders:
    if args.all_phases:
        args.selected_phases = ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
else:
    args.selected_phases = None
    args.all_phases = None


# Overwrite arg
overwriteArg = []
if args.overwrite:
    overwriteArg.append('-o')
####

inputFile, outputFile = ['.mb', '.obj']
verbose = args.verbose
recursive = args.recursive
selectedPhases = args.selected_phases
rootOnly = args.rootonly

if (not recursive) and (selectedPhases or selectedFolders):
    recursive = True  # we're gonna do recursion on the phases anyway

if rootOnly and (selectedPhases or selectedFolders):
    print("Error: You can't specify rootOnly and selected phases or folders.")
    sys.exit()

# Let's list the folders we're gonna iterate through if we wanna be verbose.
if verbose and selectedPhases:
    print(selectedPhases)
elif verbose and selectedFolders:
    print(selectedFolders)

####

def configureArgs(inputFile, outputFile):
        return [
        '-file',
        inputFile,
        '-command',
        f"file -force -options \"groups=1;ptgroups=1;materials=1;smoothing=1;normals=1\" -type \"OBJexport\" -exportAll \"{outputFile}\"",
    ]


def convertPhases(phases):
    global maya_legacy
    global maya_mode
    if recursive:  # Recursion time!
        for phase in phases:
            if not os.path.exists('phase_%s' % phase):
                continue
            for root, _, files in os.walk('phase_%s' % phase):
                for file in files:
                    if not file.endswith(inputFile):  # Input file
                        if verbose:
                            print("Skipping %s" % file)
                        continue
                    if verbose:
                        print("Adding %s" % file)
                    file = os.path.join(root, file)
                    allFiles.append(file)
    else:
        for file in os.listdir('.'):
            if not file.endswith(inputFile):
                if verbose:
                    print("Skipping %s" % file)
                continue
            if verbose:
                print("Adding in %s" % file)
            allFiles.append(file)
    for file in allFiles:
        newFile = file.replace(inputFile, outputFile)
        if os.path.exists(newFile) and not args.overwrite:
            print('Warning: %s already exists' % newFile)
            continue
        if verbose:
            print("Converting %s..." % file)
        batchArgs = configureArgs(file, newFile)
        print(batchArgs)
        # subprocess.run(['mayabatch'] + batchArgs)


def convertFolders(folders):
    global maya_mode
    global maya_legacy
    if recursive:  # Recursion time!
        for folder in folders:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                for file in files:
                    if not file.endswith(inputFile):  # Input file
                        if verbose:
                            print("Skipping %s" % file)
                        continue
                    if verbose:
                        print("Adding %s" % file)
                    file = os.path.join(root, file)
                    allFiles.append(file)
    else:
        for file in os.listdir('.'):
            if not file.endswith(inputFile):
                if verbose:
                    print("Skipping %s" % file)
                continue
            if verbose:
                print("Adding in %s" % file)
            allFiles.append(file)
    for file in allFiles:
        newFile = file.replace(inputFile, outputFile)
        if os.path.exists(newFile) and not args.overwrite:
            print('Warning: %s already exists' % newFile)
            continue
        if verbose:
            print("Converting %s..." % file)
        batchArgs = configureArgs(file, newFile)
        print(batchArgs)
        # subprocess.run(['mayabatch'] + batchArgs)

def convertRoot():
    global maya_mode
    global maya_legacy
    if recursive:  # Recursion time!
        for root, _, files in os.walk('.'):
            for file in files:
                if not file.endswith(inputFile):  # Input file
                    if verbose:
                        print("Skipping %s" % file)
                    continue
                if verbose:
                    print("Adding %s" % file)
                file = os.path.join(root, file)
                allFiles.append(file)
    else:
        for file in os.listdir('.'):
            if not file.endswith(inputFile):
                if verbose:
                    print("Skipping %s" % file)
                continue
            if verbose:
                print("Adding in %s" % file)
            allFiles.append(file)
    for file in allFiles:
        newFile = file.replace(inputFile, outputFile)
        if os.path.exists(newFile) and not args.overwrite:
            print('Warning: %s already exists' % newFile)
            continue
        if verbose:
            print("Converting %s..." % file)
        batchArgs = configureArgs(file, newFile)
        # print(batchArgs)
        subprocess.run(['mayabatch'] + batchArgs)


# Startup #

# Uses milliseconds for now.
start = int(round(time.time() * 1000))

# Which operation are we gonna run?
if selectedPhases:
    convertPhases(selectedPhases)
elif selectedFolders:
    convertFolders(selectedFolders)
elif rootOnly:
    convertRoot()
else:
    # Uhm, user should not get here. Probably a good idea to yell at 'em for invalid arguments.
    print("Error: You need to include either the selectedPhases or selectedFolders arg, but not both!")
    # We can safely call sys.exit() as we never called the maya server to init.
    sys.exit()

# Cleanup #


print("Conversion complete. Total time elapsed: %d ms" % (int(round(time.time() * 1000)) - start))
