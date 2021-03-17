##############################################################################
# Author : Mohammed Mohiddin                                                 #
# This Script is created to compare the source code between two directories  #
# and calculate the change percentage and generate a consolidated CSV report.#
#                                                                            #
##############################################################################


from __future__ import division
import os
import csv
import sys
import re
import os.path


def remove_comments(text):
    """ remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
    """
    pattern = r"""
                            ##  --------- COMMENT ---------
           //.*?$           ##  Start of // .... comment
         |                  ##
           /\*              ##  Start of /* ... */ comment
           [^*]*\*+         ##  Non-* followed by 1-or-more *'s
           (                ##
             [^/*][^*]*\*+  ##
           )*               ##  0-or-more things which don't start with /
                            ##    but do end with '*'
           /                ##  End of /* ... */ comment
         |                  ##  -OR-  various things which aren't comments:
           (                ##
                            ##  ------ " ... " STRING ------
             "              ##  Start of " ... " string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^"\\]       ##  Non "\ characters
             )*             ##
             "              ##  End of " ... " string
           |                ##  -OR-
                            ##
                            ##  ------ ' ... ' STRING ------
             '              ##  Start of ' ... ' string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^'\\]       ##  Non '\ characters
             )*             ##
             '              ##  End of ' ... ' string
           |                ##  -OR-
                            ##
                            ##  ------ ANYTHING ELSE -------
             .              ##  Anything other char
             [^/"'\\]*      ##  Chars which doesn't start a comment, string
           )                ##    or escape
    """
    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]
    noncommentsText = "".join(noncomments)
    noncommentsText = re.sub("^(\+|-)$|^(\+|-) $", "", noncommentsText, flags=re.MULTILINE)
    noncommentsText = "\n".join([ll.strip() for ll in noncommentsText.splitlines() if ll.strip()])
    return noncommentsText

#Stripping operations on Files

try:  
    ## Defining parameter variables
    oldDirectory = input("Enter old directory path:")
    newDirectory = input("Enter new directory path:")
        
        
    print("Comparing Directories: " + oldDirectory + " and " + newDirectory)
    
        
    oldLines       = []
    newLines       = []
    oldfilename    = []
    newfilename    = []
    percentage     = []
    LineDifference = []
    Format         = []
    sym = '%'
        
    ##Calculate the Change Percentage
    def CalculatePercentage(oldLines,newLines,sflag):
        if(sflag == 0):
            for x,y in zip(oldLines,newLines):
                sub = (y-x) 
                try:                    
                    div =  ((sub)/(y))*100
                except ZeroDivisionError:
                    div = 0
                per = (float)('%.2f'%(div))
                pct =  "{}%".format(per)
                percentage.append(pct)
                LineDifference.append(sub)
 
        if(sflag == 1):
            percent = (float)('%.2f'%(100))
            percentage.append(str(percent)+sym)            
                
        
    ## Exporting the DATA to CSV File
    def ParsetoCsv(oldfilename,newfilename,oldLines,newLines,percentage):
        with open('Code_Comparision.csv','w',newline='') as csvfile:
            fieldnames = ["OLDFILENAME","NEWFILENAME","EXTENSIONFORMAT","NO_OF_OLDLINES","NO_OF_NEWLINES","LINEDIFFERENCE","PERCENTAGE"]
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for (p,q,r,s,t,u,v) in zip(oldfilename,newfilename,Format,oldLines,newLines,LineDifference,percentage):
                writer.writerow({'OLDFILENAME':p,'NEWFILENAME':q,'EXTENSIONFORMAT':r,'NO_OF_OLDLINES':s,'NO_OF_NEWLINES':t,'LINEDIFFERENCE':u,'PERCENTAGE':v})
        
    ## Parsing logic handled here
    def ParseNewFile(fullname):
        if(fullname!=0):
            with open(fullname,'r') as infile:
                NewLineNo = 0
                code_w_comments = open(fullname).read()
                x = remove_comments(code_w_comments)                        
                for line in x.splitlines():
                    NewLineNo = NewLineNo+1
                         
                newLines.append(NewLineNo)
                newfilename.append(fullname)              
                    
    ## Parsing logic handled here        
    def ParseOldFile(fullname):
        if(fullname!=0):
            with open(fullname,'r') as infile:
                NewLineNo = 0
                code_w_comments = open(fullname).read()
                x = remove_comments(code_w_comments)                        
                for line in x.splitlines():
                    NewLineNo = NewLineNo+1
                         
                oldLines.append(NewLineNo)
                oldfilename.append(fullname)
        else:
            string1 = ['NewFile_or_NewLocation']
            oldfilename.append(string1)
        
    ## Save Format
    def ExtensionFormat(fullname):
        if(fullname.endswith('.cpp')):
            Format.append("cpp")
 
        elif(fullname.endswith('.c')):
            Format.append(".c")
                
        elif(fullname.endswith('.hpp')):
            Format.append(".hpp")
        else:
            Format.append(".h")
                
        
    ## Reading NewDirectory Files            
    def Read_NewFile_Content(dir4,dir3,New_flag):
        pad = 0
        name = 0
        for (dirpath, dirnames, filenames) in os.walk(dir4):
            for filename in filenames:
                if(filename.endswith('.cpp') or filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.hpp')):
                    relative_path = dirpath.replace(dir4, "")
                    if(New_flag == 0):
                        if os.path.exists( dir3 + relative_path + '\\' +  filename) == True:
                            fullname = os.path.join(dirpath, filename)
                            ParseNewFile(fullname)
                            ExtensionFormat(fullname)
                    if(New_flag == 1):
                        if os.path.exists( dir3 + relative_path + '\\' +  filename) == False:
                            fullname = os.path.join(dirpath,filename)
                            ParseNewFile(fullname)
                            oldLines.append(pad)
                            ParseOldFile(name)
                            ExtensionFormat(fullname)
        return    
                        
    ## Reading OldDirectory Files                
    def Read_OldFile_Content(dir3,dir4,Old_flag):
        for (dirpath, dirnames, filenames) in os.walk(dir3):
            for filename in filenames:
                if(filename.endswith('.cpp') or filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.hpp')):
                    relative_path = dirpath.replace(dir3,"") 
                    if os.path.exists( dir4 + relative_path + '\\' +  filename) == True:
                        fullname = os.path.join(dirpath, filename)
                        ParseOldFile(fullname)                                                                 
                        
        return
                        
        
    if(oldDirectory == newDirectory):
           
        print("Reading Old Directory Contents.....")
        
        Read_OldFile_Content(oldDirectory,newDirectory,Old_flag=0)
            
        print("Reading New Directory Contents.....")
        
        Read_NewFile_Content(newDirectory,oldDirectory,New_flag=0)        
            
        CalculatePercentage(oldLines,newLines,sflag=0)             
            
        
    if(oldDirectory != newDirectory): 
            
        print("Reading Old Directory Contents.....")            
        
        Read_OldFile_Content(oldDirectory,newDirectory,Old_flag=0)
            
        print("Reading New Directory Contents.....")
            
        Read_NewFile_Content(newDirectory,oldDirectory,New_flag=0)
            
        print("Reading NewDirectory Files not present in OldDirectory.....")
          
        Read_NewFile_Content(newDirectory,oldDirectory,New_flag=1)
            
        CalculatePercentage(oldLines,newLines,sflag=0)
            
        CalculatePercentage(oldLines,newLines,sflag=1)            

    print("Generating Consolidated CSV file.....")
        
    ParsetoCsv(oldfilename,newfilename,oldLines,newLines,percentage)
        
    print("CSV File Generated Successfully.....")
        
except IOError:
    print("ERROR!! Can't find file. Please enter a valid file name/path OR Close the CSV file")