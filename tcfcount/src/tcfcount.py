import os
from os import listdir
from os.path import isfile, join
import csv
from getpass import getpass

line_number = 62
Total = 0
count = 0
while(count!=3):
    OriginPass = "Tc7!430"
    print("Enter the password")
    password = getpass()
    if(OriginPass == password):
        OriginalPath = os.getcwd()

        dirpath = input("Enter the path:")

        os.chdir(dirpath)

        mypath = os.walk(dirpath)
 
        mytest =[]
        myname =[]
        for path,subd,fils in mypath :
            for name in fils:
                fullname = os.path.join(path,name)
                with open(fullname,'r',encoding='utf-8') as infile:
                    current_line = 1
                    for line in infile:
                        if current_line == line_number:
                            for s in line.split():
                                if s.isdigit():
                                    mytest.append(s)
                                    myname.append(name)
                                    Total = Total + int(s)
                                    break 
                            break
                        current_line += 1
                
        os.chdir(OriginalPath)
        newfile = input("Enter the file name to save:")
        tcffile = newfile + '.csv'
        with open(tcffile,'w',newline='') as csvfile:
            fieldnames = ['FileName','TestCases']
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for x,y in zip(myname,mytest):
                writer.writerow({'FileName':x,'TestCases':y})   
        print("Test case count generated successfully...")
        break
    else:
        print("Wrong Password Entered...Try again...")
        count = count+1
if(count==3):  
    print("Your password limit has ended")
