import os
import pandas as pd

labResLocation = "./data_from_Synthesis_Lab_Spring_2024"
outputLocation = "./rowFilter.csv"
mappedoutputLocation = "./legendRowMapping.csv"


###########

def contains(input, findWord, errorRange):
    trig = set()
    
    #print("input "+str(input) + " findword " + findWord )
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
                
            if findWordsIndex == len(findWord) and errors == 0:
                #print("found")
                return ((True,True), findWord)
                
            elif findWordsIndex == len(findWord) and errors <= errorRange:
                #print("found")
                return ((True,False), findWord)
                
    return ((False,False), findWord)

#############      


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
    
    def mostSimilar(self, listWords):
        foundword = ""
        
        # Iterate over indices of the longest word in listWords
        max_length = max(len(word) for word in listWords)
        for index in range(max_length):
            count = {}
            
            # Count occurrences of each character at position `index`
            for word in listWords:
                if index < len(word):
                    letter = word[index]
                    if letter in count:
                        count[letter] += 1
                    else:
                        count[letter] = 1
            
            # Find the most occurred character at position `index`
            max_occurred = ("", 1)
            for letter, cnt in count.items():
                if cnt > max_occurred[1]:
                    max_occurred = (letter, cnt)
            
            # Append the most occurred letter to `foundword`
            foundword += max_occurred[0]
        #print(listWords)
        #print(foundword)
        
        return foundword


                
            
        
    def getWantSet(self):
        return self.wantedColumns
    
    def getWantTypes(self):
        return self.wantedTypeDic
    
    def getCollectedData(self):
        return self.collectionDic
    
    def swellAvg(self, key):
        #print("inbox")
        #print(key in self.elementMap)
        #print(self.elementMap)
        #print(len(self.elementMap[key]) >= 3)
        if key in self.wantedColumns and len(self.collectionDic[key]) >= 3:
            #print("hi")
            pointer = [0,1,2]
            
            
            #print(len(self.elementMap[key]))
            while max(pointer) < len(self.collectionDic[key]):
                collData = list()
                collPoz = list()
                baseWord = self.mostSimilar([self.collectionDic["sample"][pointer[0]],
                                             self.collectionDic["sample"][pointer[1]],
                                             self.collectionDic["sample"][pointer[2]]
                                             ])
                
                
                for poz in pointer:
                    if contains(self.collectionDic["sample"][poz],baseWord,1 )[0][0]:
                        collData.append(self.collectionDic[key][poz])
                        collPoz.append(poz)
                        
                '''''''''      
                print("_______________")
                print(baseWord)
                if (baseWord == "NBBB1_r1"):
                    print(pointer)
                    print(collPoz)
                    print(contains("KL1_1",baseWord,1 ))
                print()
                '''''
                
                if  collData != []:
                    average = sum(collData) / len(collData)
                    for index in collPoz:
                        self.collectionDic[key][index] = average
                        
                for inc in range(len(collPoz)):
                    pointer[inc] += len(pointer)
                    
        #print("return/2")
        return self
    
    def getMapDataSet(self):
        return self.mappingHash.getDataSet()
        


usersWants = InputClass()
            
        
    
    
        

            
            
    


# Checks if the input for data is the valid type and not null
def checkVariables(key, append):
    try:
        if usersWants.getWantTypes()[key] == str:
            return isinstance(append, str) and append.lower() not in ["-", "none", key.lower()]
        elif usersWants.getWantTypes()[key] == (int, float):
            return isinstance(append, (int, float)) and not pd.isna(append)
        return False
    except Exception as e:
        return False

    
        
    

    
# Makes sure that there's input for all information provided
def checkForNulls(hash):
    return all(valueArray[2] for valueArray in hash.values())

def scanWantedCol(maxRow, df, dataTupple):
    increment = 1
    
    while (maxRow + increment) < df.shape[0]:
        collectedData = []
        validCollection = True
        
        for name, hashInfo in dataTupple.items():
            #print(hashInfo)
            row_index = int(hashInfo[0]) + increment
            col_index = int(hashInfo[1])
            
            # Check if the cell is not NaN and passes the validity check
            if pd.notna(df.iat[row_index, col_index]) and checkVariables(name, df.iat[row_index, col_index]):
                collectedData.append(df.iat[row_index, col_index])
            else:
                validCollection = False
                break  # Exit the loop early if any invalid data is found
        
        # If all data for this row is valid, add to usersWants
        if validCollection and len(collectedData) == len(usersWants.getWantSet()):
            index = 0 
            for name in dataTupple.keys():
                usersWants.addInfo(name, collectedData[index])
                index += 1
        
        increment += 1




##############
# Finds the Columns of the wanted information
def findWantedColumn(dicDateinfo, df):
    maxRow = 0
    
    for rowindex, rowName in df.iterrows():
        dicDateinfo = {wanted: [None, None, False] for wanted in usersWants.getWantSet()}
        
        for colIndex, colName in enumerate(df.columns):
            if not all(dicDateinfo[wanted][2] for wanted in dicDateinfo):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str):
                    dicKey = remSpecialCharacter(rowName[colName])
                    #print()
                    #print(dicDateinfo)
                    #print ( dicKey)
                    #print(dicKey in usersWants.getWantSet())
                    
                    #print( dicDateinfo["rswell"][2])
                    #print( not dicDateinfo["rswell"][2])
                    #print ( not dicDateinfo["sswell"][2])
                    
                    
                    
                    # Check if dicKey or its variations ('rswell', 'sswell') are in wanted columns
                    print()
                    if  ((contains(dicKey, "rswell", 1)[0][0]) and (not (contains(dicKey, "sswell", 1)[0][1]) and not dicDateinfo["rswell"][2])): 
                        dicKey = "rswell"
                        if checkVariables(dicKey, df.iat[rowindex+1, colIndex]):
                            
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex         
                    elif((contains(dicKey, "sswell", 1)[0]) and not dicDateinfo["sswell"][2]):
                        dicKey = "sswell"
                        if checkVariables(dicKey, df.iat[rowindex+1, colIndex]):
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex
                    elif (dicKey in usersWants.getWantSet()):
                        #print("raba")
                        if checkVariables(dicKey, df.iat[rowindex+1, colIndex]):
                            #print("crab")
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex
                      
                                
            else:
                #print('All columns found in row:', rowindex)
                scanWantedCol(maxRow, df, dicDateinfo)
                return
            
        # Output invalid rows if needed
        '''''''''
        collect = {key for key, value in dicDateinfo.items() if value[2] == False}
        if collect:
            print(f"Invalid row: {rowindex}, Missing columns: {collect}")
        

            

    # Call scanWantedCol outside the loop to process collected data
    

    # Output invalid rows if needed
    if not all(dicDateinfo[wanted][2] for wanted in dicDateinfo):
        print(f"Invalid row: {rowindex}")
    '''''''''

    # Process the found columns
    

            
    #print("invalide row" + str({key for key, value in dicDateinfo.items() if value[2] == False})) 
            
            #fullcollect = {key for key, value in dicDateinfo.items()}
            #print("invalide row" + str(collect))
            #collect = {dicDateinfo[2] == False for dicDateinfo in dicDateinfo.values()}
###############    

# ______ main _______/
#gets the users wants
#usersWants.collectUserInputs()


print((contains("laingrswell", "rswell", 1))[0][0])