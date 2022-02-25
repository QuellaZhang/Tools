import re
import os
import shutil
from datetime import datetime

global manualCheckList

class Projects:
    name = ''
    url = ''

    def __init(self, name, url):
        self.name = name
        self.url = url

def getLatestCommit(projectName, url):
    if projectName in ["Outcome", "KTL", "SOL2"]:
        branch = "develop"
    elif projectName in ["Facebook_ZSTD", "LZ4"]:
        branch = "dev"
    elif projectName in ["WebKit", "LLVM", "VCPKG_Tool", "CoreCLR", "Git", "Python3", "React_Native_Windows", "LibJPEG_Turbo", "Electron", "Google_RE2", 
                        "Terminal", "Netplus", "Libigl", "RxCpp", "Azure_iot_sdk_c", "Google_Snappy", "Tesseract", "LevelDB", "Crunch", "ONNX","STL", 
                        "Mixxx", "Cppcheck", "Box2d"]:
        branch = "main"
    elif projectName in ["CryEngine"]:
        branch = "release"
    elif projectName in ["LAME"]:
        branch = "origin"
    elif projectName in ["MySQL"]:
        branch = "8.0"
    elif projectName in ["QT5"]:
        branch = "5.15"
    elif projectName in ["QT6"]:
        branch = "6.3"
    elif projectName in ["LUA"]:
        branch = "lua-5.1"
    elif projectName in ["LUAJIT"]:
        branch = "v2.1"
    elif projectName in ["Cocos2dx"]:
        branch = "v4"
    elif projectName in ["CppCoro"]:
        branch = "vs2019"
    elif projectName in ["Capemon"]:
        branch = "capemon"
    elif projectName in ["Catch2"]:
        branch = "devel"
    elif projectName in ["Renderdoc"]:
        branch = "v1.x"
    else:
        branch = "master"

    os.system(r"getLatestCommit.cmd" + " " + url + " " + r"refs/heads/" + branch)

    with open(r'commit.txt', 'r') as file:
        line = file.readline()
        commit = line[:7]
        return commit

def rewriteFile(newFile, line):
    with open(newFile, 'a+') as file:
        file.write(line)

def updateSHA(filename):

    project = Projects()

    with open(filename, 'r+') as file:
        while True:
            line = file.readline()
            if not line:
                break

            if "Location=\"git\"" in line or "Location=\"gclient\"" in line:  
                Name = (re.compile('"(.*)" L')).findall(line) # match name
                project.name = str(Name[0])
                # print(project.name)

            if project.name not in manualCheckList and project.name not in fixedCommit:
                if r"<url>" in line:
                    URL = (re.compile('>(.*)<')).findall(line) # match url
                    project.url = str(URL[0])
                    # print(project.url)

                if r"<commit>" in line:
                    Commit = (re.compile('>(.*)<')).findall(line) # match commit
                    oldCommit = str(Commit[0])
                    newCommit = getLatestCommit(project.name, project.url)
                    if (oldCommit == '' or newCommit == ''):
                        manualCheckList.append(project.name)
                    else:
                        line = line.replace(oldCommit, newCommit)
                        # print(newCommit)

            rewriteFile(r"TestAssets_new.xml", line)

if __name__ == "__main__":

    manualCheckList  = []
    fixedCommit = ["Chrome", "Cutlass", "Benchstone", "Geekbench4", "Storage-XEngSys", "Storage-XStore", "CoreMark"]

    updateSHA("TestAssets.xml")

    str = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.mkdir(str)
    shutil.move(r"TestAssets_new.xml", str)

    print("Note: Failed to update %s commit, please manually check" % manualCheckList)
    print("Note: The %s commit don't need to be updated" % fixedCommit)