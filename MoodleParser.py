import filecmp
import argparse
import os
from zipfile import ZipFile
from rarfile import RarFile

parser = argparse.ArgumentParser()

parser.add_argument("--folderParsing", type=str, help="iterate through a folder of text files")
parser.add_argument("--deleteCompressed", type=bool, help="deletes compressed format after uncompressing")

args = parser.parse_args()

folder = args.folderParsing
deleteCompr = args.deleteCompressed

def unzipMoodleContent(moodleFolderPath, delete):
    listOfCompromisedZips = []
    for root, dirs, files in os.walk(moodleFolderPath):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            fileType = file[-4:]
            fileToUnpack = root + '/' + file
            if fileType == ".zip":
                try:
                    with ZipFile(fileToUnpack, 'r') as zipObj:
                        zipObj.extractall(root)
                        os.remove(fileToUnpack)
                except:
                    listOfCompromisedZips.append(fileToUnpack)
            elif fileType == ".rar":
                try:
                    with RarFile(fileToUnpack) as rarObj:
                        rarObj.extractall(root)
                        os.remove(fileToUnpack)
                except:
                    listOfCompromisedZips.append(fileToUnpack)
    return listOfCompromisedZips

def checkForFormat(moodleFolderPath):
    listOfDirectories = []
    for root, dirs, files in os.walk(moodleFolderPath):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            possibleFileTypes = ['.txt', '.py', '.md']
            fileType = os.path.splitext(file)
            if fileType[1] not in possibleFileTypes:
                if root not in listOfDirectories:   
                    listOfDirectories.append(root)
    return listOfDirectories

def main():
    problematicFolders = unzipMoodleContent(folder, deleteCompr)
    wrongFormatFiles = checkForFormat(folder)
    print("There are {} unexplandable archives.".format(len(problematicFolders)))
    print("There are {} wrong files.".format(len(wrongFormatFiles)))

if __name__ == "__main__":
    main()