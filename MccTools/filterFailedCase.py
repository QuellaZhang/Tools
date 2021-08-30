import os

f1 = open(r'v-zhyi\results.log', 'r')
lines = f1.readlines();
f2 = open(r'v-zhyi\failed.log', 'w')

for line in lines:
    if '-- failed' in line:     
        f2.writelines(line)
        print(line)
    
