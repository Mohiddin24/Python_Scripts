##############################################################################
# Author         : M Mohammed Mohiddin                                         #
# Python version : v3.7 above                                                #
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
import xlsxwriter
from xlsxwriter import Workbook

############################################ Function to remove comments ################################################################

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
    ## Defining input parameter variables
    oldDirectory = input("Enter old directory path:")
    newDirectory = input("Enter new directory path:")
        
        
    print("Comparing Directories: " + oldDirectory + " and " + newDirectory)
       
    oldLines       = []
    newLines       = []
    oldfilename    = []
    newfilename    = []
    percentage     = []
    ReusePercent   = []
    LineDifference = []
    Format         = []
    modlist        = []
    Modulename     = []
    sym = '%'
    
############################################ Function to Export data to Excel ################################################################    
    
    def ParsetoExcel(oldfilename,newfilename,Format,oldLines,newLines,LineDifference,percentage):
        outworkbook     = Workbook('CodeTracker_Mohiddin.xlsx', {'strings_to_numbers': True})
        DataSheet       = outworkbook.add_worksheet()
        cell_format     = outworkbook.add_format({'bold': True,'bg_color': '#e6f2ff','border':1,'border_color':'#000000'})
        #Datacell_format     = outworkbook.add_format({'border':1,'border_color':'#000000'})
        DataSheet.write(0, 0, 'OLDFILENAME',cell_format)
        DataSheet.write(0, 1, 'NEWFILENAME',cell_format)
        DataSheet.write(0, 2, 'EXTENSION_FORMAT',cell_format)
        DataSheet.write(0, 3, 'NO_OF_OLDLINES',cell_format)
        DataSheet.write(0, 4, 'NO_OF_NEWLINES',cell_format)
        DataSheet.write(0, 5, 'LINE_DIFFERENCE',cell_format)
        DataSheet.write(0, 6, 'CHANGE_PERCENTAGE',cell_format)
        DataSheet.write(0, 7, 'RE_USE_PERCENTAGE',cell_format)
        DataSheet.write(0, 8, 'MODULE_NAME',cell_format)

        for row_index, row_value in enumerate(zip(oldfilename,newfilename,Format,oldLines,newLines,LineDifference,percentage,ReusePercent,Modulename)):
            
            for col_index, col_value in enumerate(row_value):
                DataSheet.write(row_index + 1, col_index, col_value)
        
        outworkbook.close()
        
############################################ Function to calculate change percentage ################################################################

    def CalculatePercentage(oldLines,newLines,sflag):
        if(sflag == 0):
            for x,y in zip(oldLines,newLines):
                sub = (y-x) 
                try:                    
                    div   =  ((sub)/(x))*100
                    reuse =  100 - div 
                except ZeroDivisionError:
                    div = 0
                per = (float)('%.2f'%(div))
                reusef = (float)('%.2f'%(reuse))
                #pct =  "{}%".format(per)
                percentage.append(per)
                LineDifference.append(sub)
                ReusePercent.append(reusef)

        if(sflag == 1):
            percent = (float)('%.2f'%(100))
            percentage.append(percent) 
            ReusePercent.append(percent)                  
          
                
        
############################################ function for CSV ( Reserved for Future use) #########################################################

    def ParsetoCsv(oldfilename,newfilename,oldLines,newLines,percentage):
        with open('CodeTracker.csv','w',newline='') as csvfile:
            fieldnames = ["OLDFILENAME","NEWFILENAME","EXTENSIONFORMAT","NO_OF_OLDLINES","NO_OF_NEWLINES","LINEDIFFERENCE","PERCENTAGE","RE_USE_PERCENTAGE","MODULE_NAME"]
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for (p,q,r,s,t,u,v,w,x) in zip(oldfilename,newfilename,Format,oldLines,newLines,LineDifference,percentage,ReusePercent,Modulename):
                writer.writerow({'OLDFILENAME':p,'NEWFILENAME':q,'EXTENSIONFORMAT':r,'NO_OF_OLDLINES':s,'NO_OF_NEWLINES':t,'LINEDIFFERENCE':u,'PERCENTAGE':v,'RE_USE_PERCENTAGE':w,'MODULE_NAME':x})
                
############################################ Function to for fetching Module Name ################################################################
                
    def ModuleName(module_flag,fullname):
        if(module_flag == 1):
            flag = 0
            pattern1 = re.compile(r'([a-z_\dA-Z\\:]*)\bsource\b')
            pattern2 = re.compile(r'([a-z_\dA-Z\\:]*)\bconfig\b')
            matches1 = pattern1.finditer(fullname)
            matches2 = pattern2.finditer(fullname)
            if(re.search(pattern1,fullname)):
                for match1 in matches1:
                    str = match1.group(1)
                    modlist.append(match1.group(1))
                for x in modlist:
                    k = x.strip("\\")
                    flag = 1
                    path = k                  
                if(flag == 1):
                    module = path.split("\\")
                    Modulename.append(module.pop())
            elif(re.search(pattern2,fullname)):
                for match2 in matches2:
                    str = match2.group(1)
                    modlist.append(match2.group(1))
                for x in modlist:
                    k = x.strip("\\")
                    flag = 1
                    path = k
                    
                if(flag == 1):
                    module = path.split("\\")
                    Modulename.append(module.pop())
        
            else:
                Modulename.append("NA")
        
############################################ Function to for parsing New File Contents ################################################################
    def ParseNewFile(fullname):
        if(fullname!=0):
            with open(fullname,'r') as infile:
                NewLineNo = 0
                code_w_comments = open(fullname,encoding="cp437",errors='ignore').read()
                x = remove_comments(code_w_comments)                        
                for line in x.splitlines():
                    NewLineNo = NewLineNo+1
                         
                newLines.append(NewLineNo)
                newfilename.append(fullname)              
                    
############################################ Function to for parsing Old File Contents ################################################################  
      
    def ParseOldFile(fullname):
        if(fullname!=0):
            with open(fullname,'r') as infile:
                NewLineNo = 0
                code_w_comments = open(fullname,encoding="cp437",errors='ignore').read()
                x = remove_comments(code_w_comments)                        
                for line in x.splitlines():
                    NewLineNo = NewLineNo+1
                         
                oldLines.append(NewLineNo)
                oldfilename.append(fullname)
        else:
            string1 = 'NewFile_or_NewLocation'
            oldfilename.append(string1)
        
############################################ Function to Save Format ###################################################################################
    def ExtensionFormat(fullname):
        if(fullname.endswith('.cpp')):
            Format.append("cpp")
 
        elif(fullname.endswith('.c')):
            Format.append(".c")
                
        elif(fullname.endswith('.hpp')):
            Format.append(".hpp")
        else:
            Format.append(".h")
                
        
############################################ Function to for Read New File Contents ################################################################          
    def Read_NewFile_Content(dir4,dir3,New_flag):
        pad = 0
        name = 0
        global BUILD_FOLDER
        global INSTALL_FOLDER
        for (dirpath, dirnames, filenames) in os.walk(dir4):
            for filename in filenames:
                fullname = os.path.join(dirpath, filename)
                if(filename.endswith('.cpp') or filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.hpp')):
                    relative_path = dirpath.replace(dir4, "")
                    if(New_flag == 0):
                        if os.path.exists( dir3 + relative_path + '\\' +  filename) == True:
                            #fullname = os.path.join(dirpath, filename)
                            ModuleName(1,fullname)
                            ParseNewFile(fullname)
                            ExtensionFormat(fullname)
                    if(New_flag == 1):
                        if os.path.exists( dir3 + relative_path + '\\' +  filename) == False:
                            #fullname = os.path.join(dirpath,filename)                         
                            ModuleName(1,fullname)
                            ParseNewFile(fullname)
                            oldLines.append(pad)
                            ParseOldFile(name)
                            ExtensionFormat(fullname)
        return    
                        
############################################ Function to for Read Old File Contents ################################################################  
              
    def Read_OldFile_Content(dir3,dir4,Old_flag):
        global BUILD_FOLDER
        global INSTALL_FOLDER
        for (dirpath, dirnames, filenames) in os.walk(dir3):
            for filename in filenames:
                fullname = os.path.join(dirpath, filename) 
                if(filename.endswith('.cpp') or filename.endswith('.c') or filename.endswith('.h') or filename.endswith('.hpp')):
                    relative_path = dirpath.replace(dir3,"") 
                    if os.path.exists( dir4 + relative_path + '\\' +  filename) == True:
                        #fullname = os.path.join(dirpath, filename)                       
                                #ModuleName(1,fullname)
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

    print("Generating Consolidated Excel file.....")
        
    #ParsetoCsv(oldfilename,newfilename,oldLines,newLines,percentage)
    ParsetoExcel(oldfilename,newfilename,Format,oldLines,newLines,LineDifference,percentage)
        
    print("Excel File Generated Successfully.....")
        
except IOError:
    print("ERROR!! Can't find file. Please enter a valid file name/path OR Close the Excel file")