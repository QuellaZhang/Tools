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
    if projectName in ["QT5"]:
        branch = "5.15"
    elif projectName in ["QT6"]:
        branch = "6.3"
    elif projectName in ["UnrealEngine"]:
        branch = "master"
    elif projectName in ["Sogou_Workflow"]:
        branch = "windows"
    else:
        branch = "default"
    
    if branch == "default":
        os.system(r"getLatestCommit.cmd" + " " + url + " " + r"origin HEAD")
    else:
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

    print("Note: For QT5 nad QT6, please use the latest stable branch, such as 5.15/5.16, 6.2/6.3\n")
    print("Note: Failed to update %s commit, please manually check\n" % manualCheckList)
    print("Note: The %s commit don't need to be updated\n" % fixedCommit)