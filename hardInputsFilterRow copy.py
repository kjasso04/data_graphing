import os
import pandas as pd

labResLocation = "./data_from_Synthesis_Lab_Spring_2024"
outputLocation = "./rowFilter.csv"
mappedoutputLocation = "./legendRowMapping.csv"


# Remove special characters and turn string to lowercase 
def remSpecialCharacter(colName):
    newName = ''.join([letter.lower() for letter in colName if letter.isalnum()])
    return newName

# A class that allows for the collection of info that then get mapped to a number
class HashSetWithIndex:
    def __init__(self, name: str):
        self.name = name
        self.elementMap = {}
        self.elementSet = set()

    def add(self, elem):
        fixedElem = remSpecialCharacter(elem)
        if fixedElem not in self.elementSet:
            self.elementSet.add(fixedElem)
            self.elementMap[fixedElem] = len(self.elementSet) - 1

    def indexOf(self, elem):
        return self.elementMap.get(remSpecialCharacter(elem), -1)

    def getDataSet(self):
        collectionData = {
            (self.name + " collName"): [],
            (self.name + " assined"): []
        }
        for name, index in self.elementMap.items():
            collectionData[(self.name + " collName")].append(name)
            collectionData[(self.name + " assined")].append(index)
        return collectionData

# Input Class
class InputClass:
    def __init__(self):
        self.wantedColumns = set(["sample", "monomer1", "monomer2", "crosslinkermol","rswell", "sswell"])
        self.wantedTypeDic = {
            "sample": str,
            "monomer1": str,
            "monomer2": str,
            "crosslinkermol": (int, float),
            "rswell": (int, float),
            "sswell": (int, float)
            
        }
        self.collectionDic = {
            "sample": [],
            "monomer1": [],
            "monomer2": [],
            "crosslinkermol": [],
            "monomer1mapped": [],
            "monomer2mapped": [],
            "rswell": [],
            "sswell":[]
        }
        self.mappingHash = HashSetWithIndex("mapping")
    ''''''''''
    def collectUserInputs(self):
        userInput = input("What information do you want (type 'done' when you're finished): ")
        while userInput != "done":
            typeInput = input("What is the type of the information (number or characters): ")
            if typeInput == "number":
                self.establishVariables(userInput, (int, float))
            elif typeInput == "characters":
                self.establishVariables(userInput, str)
                if userInput.lower() != "sample":
                    self.collectionDic[userInput + "mapped"] = []
            else:
                print("That's not a valid input")
            userInput = input("What information do you want (type 'done' when you're finished): ")
    '''''''''''
    def establishVariables(self, userInput, types):
        self.wantedColumns.add(userInput)
        self.wantedTypeDic[userInput] = types
        self.collectionDic[userInput] = []
        
    def addInfo(self, key, information):
        self.collectionDic[key].append(information)
        if key.lower() != "sample" and self.wantedTypeDic[key] == str:
            self.mappingHash.add(information)
            if key + "mapped" in self.collectionDic:
                self.collectionDic[key + "mapped"].append(self.mappingHash.indexOf(information))
            else:
                self.collectionDic[key + "mapped"] = [self.mappingHash.indexOf(information)]
        
    def getWantSet(self):
        return self.wantedColumns
    
    def getWantTypes(self):
        return self.wantedTypeDic
    
    def getCollectedData(self):
        return self.collectionDic
    def getMapDataSet(self):
        return self.mappingHash.getDataSet()
        


usersWants = InputClass()


###########

def contains(input, findWord, errorRange):
    trig = set()
    
    print("input "+str(input) + " findword " + findWord )
    for x in range(errorRange):
        trig.add(findWord[x])
    
    #print(trig)
    #print( )
    
    for i in range(len(input) - len(findWord) + 1):
        
        errors = 0
        findWordsIndex = 0
        inputIndex = i
        
        if input[i] in trig:
            #print("trigger")
            #print( )
            while findWordsIndex < len(findWord) and inputIndex < len(input) and errors <= errorRange:
                
                #print("findWordsIndex "+ str(findWord[findWordsIndex]) )
                #print("inputIndex " +  str(input[inputIndex]))
                
                if findWord[findWordsIndex] != input[inputIndex]:
                    errors += 1
                findWordsIndex += 1
                inputIndex += 1
                #print("errors " + str(errors))
                #print("--------")
                
            
            if findWordsIndex == len(findWord) and errors <= errorRange:
                #print("found")
                return (True, findWord)
                
    return (False, findWord)

#############      
            
        
    
    
        

            
            
    


# Checks if the input for data is the valid type and not null
def checkVariables(key, append):
    if usersWants.getWantTypes()[key] == str:
        return isinstance(append, str) and append.lower() not in ["-", "none", key.lower()]
    elif usersWants.getWantTypes()[key] == (int, float):
        return isinstance(append, (int, float))
    return False

# Makes sure that there's input for all information provided
def checkForNulls(hash):
    return all(valueArray[2] for valueArray in hash.values())

def scanWantedCol( maxRow, df, dataTupple):
    # The variable that causes to look at the next row
    increment = 1 
    #print("jkjkljl")
    # The loop that goes down every row in the excel file starting from the wanted cell
    while (maxRow + increment) < df.shape[0]:
        
        # The data that is collected which will later be graphed
        collectedData = []
        
        # This is the bool that is used to check if all the needed information is found
        validCollection = True
        
        for name, hashInfo in dataTupple.items():
            # Info is the value collected in the cell
            info = df.iat[int(hashInfo[0]) + increment, int(hashInfo[1])]
            
            # This checks that this is not null and not a null
            if validCollection and not pd.isna(info) and checkVariables(name, info):
                # Adds that info to the arraylist
                collectedData.append(info)
            else:
                # This is used so we know that this is not a valid input for our graph
                validCollection = False
        
        # Adds the info to the hashset
        if validCollection and len(collectedData) == len(usersWants.getWantSet()):
            index = 0 
            for name in dataTupple.keys():
                usersWants.addInfo(name,collectedData[index])
                index += 1

        increment += 1



##############
# Finds the Columns of the wanted information
def findWantedColumn( dicDateinfo, df):
    maxRow = 0
    #print("plee")
    baseDic = dicDateinfo
    for rowindex, rowName in df.iterrows():
        dicDateinfo = {wanted: [None, None, False] for wanted in usersWants.getWantSet()}
        print(rowName)
        for colIndex, colName in enumerate(df.columns):
            #print("hjkhlfc")
            if not all(dicDateinfo[2] for dicDateinfo in dicDateinfo.values()):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str) :
                #print("hjhyouvuyo")
                    dicKey = remSpecialCharacter(rowName[colName])
                    #print(dicKey)
                    (idk, key) = contains(dicKey, 'rswell',  2)  
                    (TorF, fjdaksl) = contains(dicKey, 'sswell',  2)
                        
                    
                    if idk:
                        dicKey = key
                        #print()
                    elif TorF:
                        dicKey = fjdaksl
                        #print()
                    #print("goof")
                    #print("blbl")
                   
                    if (remSpecialCharacter(rowName[colName]) in usersWants.getWantSet() or TorF  or idk ) and checkVariables(dicKey, df.iat[ rowindex+1, colIndex] ):
                        #print("fhgfghfhg")
                        dicDateinfo[dicKey]= [ rowindex, colIndex,True]
                        if maxRow < rowindex:
                            maxRow = rowindex
                    collect = {key for key, value in dicDateinfo.items() if value[2] == False}
                    print("invalide row" + str(collect))       
            else:
                print('here')
                scanWantedCol( maxRow, df, dicDateinfo)
                return
            
            #fullcollect = {key for key, value in dicDateinfo.items()}
            #print("invalide row" + str(collect))
            #collect = {dicDateinfo[2] == False for dicDateinfo in dicDateinfo.values()}
###############    

# ______ main _______/a
#gets the users wants
#usersWants.collectUserInputs()



# Loops through all the information in the dataset 

print(remSpecialCharacter("Mass-swollen"))
print(remSpecialCharacter("Monomer 2"))
print( "monomer2" == "monomer2")
print(contains(remSpecialCharacter("swelliing"), 'rswell',  2))
print(checkVariables("rswell", 1))
print(isinstance(1, int))
print(remSpecialCharacter("Crosslinker mol%"))