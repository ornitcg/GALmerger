import os, sys
#import tkinter
from glob import glob
from pprint import pprint

currPath = os.path.dirname(sys.argv[0])  # retreives the script's path
print (currPath)
#newpath=currPath+'\Ornit' # builds name for a new path
#os.makedirs(newpath)        # creates the new path
os.chdir(currPath)

#------------------------------------------------------------------------------   
def fromGalToList( galPath ):
    keys=None
    listedGal=[]
    with open(galPath,'r') as galfile:  #opens the file as read only
        
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

               listedGal.append(rowdict)
                           
            else: listedGal.append(row)
            
            if row==('Block	Row	Column	ID	Name\n'):
               titlesrow=count
               keys = row.split('\t')
               

    return listedGal ,titlesrow

#------------------------------------------------------------------------------   

def similarFormat(gal1,gal2):  # arguments are gal list + titles row#
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

def listFilePath():   # lists the names of all the gal files to merge
    dirList=[]
    batchNumber= input("What is the batch name and number?\n")
    dirPath= input("please insert the full path and name of  files folder\n")
    for FileName in glob(dirPath+'\\*'):
        dirList.append(FileName)
    return dirList, dirPath, batchNumber
#------------------------------------------------------------------------------   

def uniteGals(gal1,gal2):  #gal files in format of list of dictionaries
    newGal=[]
    for g1,g2 in zip(gal1,gal2):
             
        if compareDicts(g1,g2) == True :
            newGal.append(g1)
            continue  # similar rows
        elif g1['ID'] == 'Empty' :  #different but only the first one is the empty
            newGal.append(g2)   #take the one that is not
        else: newGal.append(g1)
    return newGal


#------------------------------------------------------------------------------   


def compareDicts(dict1,dict2):
    if dict1.isinstance(str()):
        if dict1 != dict2:
            return False
    elif dict1.isinstance(dict()):
        for it1,it2 in zip(dict1.items(), dict2.items()):
            if it1 != it2: return False
    return True

            


#------------------------------------------------------------------------------   
def PrintList(List):
    for row in List:
        print (row)
        

#------------------------------------------------------------------------------   
   
#####main######
        
dirList, dirPath ,batchNumber = listFilePath()   #listFilePath is a function with 3 returned values

print ('dirList= ',dirList)
print ('dirPath= ',dirPath)
print ('batchNumber= ',batchNumber)
numberOfFiles = len(dirList)
print('numberOfFiles: ',numberOfFiles)


initialFile = fromGalToList(dirList[0])  # 0= the gal content in dictionary list format , 1=the titles line number

#print('Initial Gal File is :')
#PrintList(dirList[0])

unitedGal=initialFile[0]

print('titles row# :',initialFile[1])


for i in (1, numberOfFiles-1):
     nextFile = fromGalToList(dirList[i])   # 0= the gal content in dictionary list format , 1=the titles line number
     if similarFormat(initialFile,nextFile) == True:
         unitedGal = uniteGals(unitedGal,nextFile[0])
         filesAreGood = True
     else:
         filesAreGood = False
         print('\n******\nWARNING:\nThe Gal Files are in different format\nCheck the files and try again\nByeBye')
         break
        
if filesAreGood == True:
    nameForFinalGal= batchNumber + ' Final GAL' + '.gal'
    print(nameForFinalGal)

    os.chdir(dirPath)

    with open(nameForFinalGal, 'w') as nameForFinalGal:

        for row in unitedGal:
            
            if type(row) == type (str()): nameForFinalGal.write(row)
            else:
                nameForFinalGal.write(row['Block'])
                nameForFinalGal.write('\t')
                nameForFinalGal.write(row['Row'])
                nameForFinalGal.write('\t')
                nameForFinalGal.write(row['Column'])
                nameForFinalGal.write('\t')
                nameForFinalGal.write(row['ID'])
                nameForFinalGal.write('\t')
                nameForFinalGal.write(row['Name\n'])






        
