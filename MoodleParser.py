import filecmp
import argparse
import os
from zipfile import ZipFile
from rarfile import RarFile

parser = argparse.ArgumentParser()

parser.add_argument("--folderParsing", type=str, help="iterate through a folder of text files")

args = parser.parse_args()

folder = args.folderParsing

def unzipMoodleContent(moodleFolderPath):
    for root, subdirs, files in os.walk(folder):
        for file in files:
            fileType = file[-4:]
            fileToUnpack = root + '/' + file
            if fileType == ".zip":
                try:
                    with ZipFile(fileToUnpack, 'r') as zipObj:
                        zipObj.extractall(root)
                except:
                    print("This file is unzippable: {}".format(fileToUnpack)) 
            elif fileType == ".rar":
                try:
                    with RarFile(fileToUnpack) as rarObj:
                        rarObj.extractall(root)
                except:
                    print ("This file is unrarrable: {}".format(fileToUnpack))
            
def main():
    unzipMoodleContent(folder)

if __name__ == "__main__":
    main()