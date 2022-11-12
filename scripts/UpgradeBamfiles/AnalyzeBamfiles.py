"""
AnalyzeBamfiles
Used p3bamboo library to comb through all the phase folders to collect information of all the bamfiles.
This is useless if all the bamfiles are built all at once.

Author: Loonatic
Date: 10/15/2022
"""


from p3bamboo.BamFile import BamFile
import sys, os

# https://rdb.name/bam-format.md.html
LATEST_BAMVER = [6, 45]  # 6.45, reads up to version 6.14 bamfiles. released during 1.10.9.

"""
majorVersion: {
        minorVersion: [numHits, [filenames]]
}
"""
global BamVers
BamVers = dict()

# BamVers = {
#     6: {
#         45: [0, []]
#         },
#     3: {
#         45: [0, []]
#         }
#     }

# print(bam.bam_major_ver)
# print(bam.bam_minor_ver)

def traverseBam(bam):
    global BamVers
    if not BamVers.get(bam.bam_major_ver):
        # Register the major version if it isn't in our master dict yet
        BamVers[bam.bam_major_ver] = {bam.bam_minor_ver : [0, []]}
    elif not BamVers[bam.bam_major_ver].get(bam.bam_minor_ver):
        # Register the minor version if it isn't in our major versions dict yet
        BamVers[bam.bam_major_ver][bam.bam_minor_ver] = [0, []]
    BamVers[bam.bam_major_ver][bam.bam_minor_ver][0] += 1
    BamVers[bam.bam_major_ver][bam.bam_minor_ver][1].append(bam.get_filename())

selectedPhases = ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
allFiles = []
modelFiles = {}
verbose = False

for phase in selectedPhases:
    if not os.path.exists('phase_%s' % phase):
        continue
    for root, _, files in os.walk('phase_%s' % phase):
        for file in files:
            if not file.endswith(".bam"):  # Input file
                continue
            # print("Adding %s" % file)
            file = os.path.join(root, file)
            allFiles.append(file)

resourceDir = os.getcwd()
for file in allFiles:
    if os.path.isfile(os.path.join(resourceDir, file)):
        if not file.endswith(".bam"):
            continue  # We only want bam files
        modelFiles[str(file)] = str(os.path.splitext(file)[0])

for model in modelFiles.items():
    bam = BamFile()
    with open(model[0], 'rb') as f:
        bam.load(f)
    bam.set_filename(model[0])
    traverseBam(bam)

# Sort our major versions to be in numerical order.
BamVers = dict(sorted(BamVers.items()))
for majorVersion in list(BamVers):
    # Sort our minor versions to be in numerical order.
    BamVers[majorVersion] = dict(sorted(BamVers[majorVersion].items()))
    for minorVersion in BamVers[majorVersion]:
        print(f"Total count for {majorVersion}.{minorVersion} = {BamVers[majorVersion][minorVersion][0]}")

# to get details:
# print(BamVers[majorVersion][minorVersion])
