import os

len1 = len(r"v-zhyi\cpp20\tests") + 1
len2 = len(r"v-zhyi") + 1
suitname = ""

def rewrite_file(newFile, line):
    with open(newFile, 'a+') as file:
        file.write(line)

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件

        if (not str(root).endswith("accept")) and (not str(root).endswith("reject")) and (not str(root).endswith("runtime")):
            suitname = root[len1:]
            rewrite_file(r"test.lst", '\n')
            rewrite_file(r"test.lst", "# " + suitname + " tests" + '\n')
            continue

        if len(files) == 0:
            continue

        suitpath = root[len2:]
        rewrite_file(r"test.lst", suitname + ",P0	"+ suitpath + '\n')

file_name(r"v-zhyi\cpp20\tests")