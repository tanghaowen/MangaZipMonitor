import os
import json
from psutil import Popen
import subprocess
import sys
KCC_PATH=r"E:\Program Files\kcc"

def getMonitorPaths():
    savePath = None
    paths = []
    f = open("PathsToMonitor","r",encoding="utf-8")
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.replace("\n","")
        if "#" in line: savePath=line.replace("#","")
        else: paths.append(line)

    return [savePath,paths]

def getConvertArgrments():
    f = open("ConvertArgument","r",encoding="utf-8")
    argus = f.readline().replace("\n","")
    f.close()
    return argus
def getAllFiles(paths):
    filePaths=[]

    for path in paths:
        list_dirs = os.walk(path)
        for root, dirs, files in list_dirs:
            for f in files:
                if ".rar" in f or ".zip" in f:
                    filePaths.append(os.path.join(root,f))
    return filePaths

def saveConvertedFileList(convertedFileList):
    f = open("converted_files.json","w",encoding="utf-8")
    json.dump(convertedFileList,f)
    f.close()
def getConvertedFileList():
    try:
        f = open("converted_files.json", "r", encoding="utf-8")
        filelist = json.load(f)
        f.close()
        return filelist
    except (FileExistsError,FileNotFoundError) as e:
        print("converted_files.json not exits, return blank list")
        return []

convertedFileList = getConvertedFileList()

savePath,pathsToMonite = getMonitorPaths()
print(savePath)
print()
files = getAllFiles(pathsToMonite)
arguments=getConvertArgrments()


for idx,file in enumerate(files):
    file_name = os.path.basename(file)
    if file_name in convertedFileList: continue

    print("%d/%d. Start to converting file" % (idx+1,len(files)))
    print(file)

    if savePath is not None: arguments+=" -o "+savePath

    script_path = os.path.join(KCC_PATH,"kcc-c2e.py")
    cmd = 'python "%s" %s "%s"' % (script_path,arguments,file)
    subprocess.call(cmd)

    convertedFileList.append(file_name)
    saveConvertedFileList(convertedFileList)