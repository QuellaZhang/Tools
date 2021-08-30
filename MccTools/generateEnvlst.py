import os
import shutil

firstLine = "RUNALL_INCLUDE ..\..\..\..\globalenv_cpp20.lst"

def rewrite_file(newFile, line):
    with open(newFile, 'a+') as file:
        file.write(line)

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件
        
        if len(files) != 0:
            rewrite_file(r"env.lst", firstLine + '\n' + '\n')
            for file in files:
                if file == "env.lst":
                    continue
                if str(root).endswith("reject"):
                    rewrite_file(r"env.lst", ('SOURCE="%s" CFLAGS="/TP /c /w" ERRCHK="AnyCompiler" # %s') % (str(file), str(file)) + '\n')
                elif str(root).endswith("accept"):
                    rewrite_file(r"env.lst", ('SOURCE="%s" CFLAGS="/TP /c" # %s') % (str(file), str(file)) + '\n')
                elif str(root).endswith("runtime"):
                    rewrite_file(r"env.lst", ('SOURCE="%s" CFLAGS="/TP" # %s') % (str(file), str(file)) + '\n')
                #print(file)

            shutil.copyfile((r'env.lst'), os.path.join(root,'env.lst'))
            os.remove(r'env.lst')

file_name(r"v-zhyi\cpp20\tests")