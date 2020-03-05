import os, sys
import tkinter
from glob import glob
from pprint import pprint
#import pandas as pd
#help(tkinter)

CurrenPath = os.path.dirname(sys.argv[0])  # retreives the script's path
print (CurrenPath)
#newpath=CurrenPath+'\Ornit' # builds name for a new path
#os.makedirs(newpath)        # creates the new path
os.chdir(CurrenPath)

#------------------------------------------------------------------------------   
def FromGalToList(GalPath):
    keys=None
    ListedGal=[]
    with open(GalPath,'r') as galfile:  #opens the file as read only
        
        count=0
        for row in galfile:
            #print(row)
            count+=1
            rowdict={}              #restarts dictionary
            #row=row.replace('\n','')  # removes the \n character
            if keys!=None:
               values = row.split('\t')
               for i in range(0,5):
                   rowdict.setdefault(keys[i],values[i])    

               ListedGal.append(rowdict)
                           
            else: ListedGal.append(row)
            
            if row==('Block	Row	Column	ID	Name\n'):
               titlesrow=count
               keys = row.split('\t')
               
              # print(keys)
    
    
    return ListedGal ,titlesrow

#------------------------------------------------------------------------------   

def SimilarFormat(gal1,gal2):  # arguments are gal list + titles row#
    answer=True
    len1=len(gal1[0])-1
    len2=len(gal2[0])-1
    print('Len of gal1 is: ',len1, '\nLen of gal2 is: ',len2)
    print(gal1[0][len1]['Row'] ,'***', gal1[0][len2]['Row'])
    if gal1[1] != gal2[1]:
        print('\n******\nWARNING:\nThe Gal different number of starting rows\nCheck the files and try again\nByeBye')
        return False
    elif len1 != len2:
        print('\n******\nWARNING:\nThe Gal Files have a different length\nCheck the files and try again\nByeBye')
        return False
    elif gal1[0][len1]['Row']!=gal2[0][len1]['Row']:
        print('\n******\nWARNING:\nThe Gal Files are in different format (differen row#)\nCheck the files and try again\nByeBye')
        return False
    elif gal1[0][len1]['Column']!=gal2[0][len1]['Column']:
        print('\n******\nWARNING:\nThe Gal Files are in different format (different column #)\nCheck the files and try again\nByeBye')
        return False
    elif gal1[0][len1]['Block']!=gal2[0][len1]['Block']:
        print('\n******\nWARNING:\nThe Gal Files have a different number of blocks\nCheck the files and try again\nByeBye')
        return False
    else:
        print('Files formats are similar!')
        return True
#------------------------------------------------------------------------------   

def ListFilePath():   # lists the names of all the gal files to merge
    DirList=[]
    BatchNumber= input("What is the batch name and number?\n")
    DirPath= input("please insert the full path and name of  files folder\n")
    for FileName in glob(DirPath+'\\*'):
        #print(FileName)
        DirList.append(FileName)
    return DirList, DirPath, BatchNumber
#------------------------------------------------------------------------------   

def UniteGals(Gal1,Gal2):  #gal files in format of list of dictionaries
    NewGal=[]
    for g1,g2 in zip(Gal1,Gal2):
             
        if cmp(g1,g2) == True :
            NewGal.append(g1)
            continue  # similar rows
        elif g1['ID'] == 'Empty' :  #different but only the first one is the empty
            NewGal.append(g2)   #take the one that is not
        else: NewGal.append(g1)   
    return NewGal            


#------------------------------------------------------------------------------   

def cmp(dict1,dict2):
    if type(dict1) == type (str()):
        if dict1!=dict2: return False
    elif type(dict1) == type (dict()):
        for it1,it2 in zip(dict1.items(),dict2.items()):
            if it1 != it2 : return False
    return True

            


#------------------------------------------------------------------------------   
def PrintList(List):
    for row in List:
        print (row)
        

#------------------------------------------------------------------------------   
   
#####main######
        
DirList, DirPath ,BatchNumber = ListFilePath()   #ListFilePath is a function with 3 returned values

print ('DirList= ',DirList)  
print ('DirPath= ',DirPath)
print ('BatchNumber= ',BatchNumber)
NumberOfFiles = len(DirList)
print('NumberOfFiles: ',NumberOfFiles)


InitialFile = FromGalToList(DirList[0])  # 0= the gal content in dictionary list format , 1=the titles line number

#print('Initial Gal File is :')
#PrintList(DirList[0])

UnitedGal=InitialFile[0]

print('titles row# :',InitialFile[1])


for i in (1, NumberOfFiles-1):
     NextFile = FromGalToList(DirList[i])   # 0= the gal content in dictionary list format , 1=the titles line number
     if SimilarFormat(InitialFile,NextFile) == True:
         UnitedGal = UniteGals(UnitedGal,NextFile[0])
         FilesAreGood = True
     else:
         FilesAreGood = False
         print('\n******\nWARNING:\nThe Gal Files are in different format\nCheck the files and try again\nByeBye')
         break
        
if FilesAreGood == True:
    NameForFinalGal=  BatchNumber+' Final GAL' +  '.gal'
    print(NameForFinalGal)

    os.chdir(DirPath)

    with open(NameForFinalGal, 'w') as NameForFinalGal:

        for row in UnitedGal:
            
            if type(row) == type (str()): NameForFinalGal.write(row)
            else:
                NameForFinalGal.write(row['Block'])
                NameForFinalGal.write('\t')
                NameForFinalGal.write(row['Row'])
                NameForFinalGal.write('\t')
                NameForFinalGal.write(row['Column'])
                NameForFinalGal.write('\t')
                NameForFinalGal.write(row['ID'])
                NameForFinalGal.write('\t')
                NameForFinalGal.write(row['Name\n'])






        
