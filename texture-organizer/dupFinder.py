# dupFinder.py
import os, sys
import hashlib

"""
  Duplicate Texture Finder
  Good for examining what textures are used more than once in a batch of egg files. (Ex: dropshadow)
  Original author: Andres Torres
  https://www.pythoncentral.io/finding-duplicate-files-with-python/
  Modified: 11/25/2020
  Created: 4/26/2013
"""

def findDup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        #print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def joinDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize = 65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()

with open('dupeList.txt', 'w+') as f:
    pass

def printResults(dict1, verbose): # verbose would be good if print to a file instead
    #if not verbose: # lazy
    #    return
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    with open('dupeList.txt', 'a') as f:
        if len(results) > 0:
            print('Duplicates Found:', file=f)
            print('The following files are identical. The name could differ, but the content is identical', file=f)
            print('___________________', file=f)
            for result in results:
                for subresult in result:
                    print('\t\t%s' % subresult, file=f)
                print('___________________', file=f)

        else:
            print('No duplicate files found.', file=f)


def findDuplicates(folders, verbose):
    dups = {}
    for i in folders:
        # Iterate the folders given
        if os.path.exists(i):
            # Find the duplicated files and append them to the dups
            joinDicts(dups, findDup(i))
        else:
            print('%s is not a valid path, please verify' % i)
            sys.exit()
    printResults(dups, verbose)
    #if outputFile:
    #    with open('dupeList.txt', 'w+') as f:
    #        print("%s\n" % printResults(dups, verbose, outputFile), file=f)
