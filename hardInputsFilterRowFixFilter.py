import os
import pandas as pd

labResLocation = "./data_from_Synthesis_Lab_Spring_2024"
outputLocation = "./rowFilter.csv"
mappedoutputLocation = "./legendRowMapping.csv"


###########
def contains(input, findWord, errorRange):
    output = ((False, False), findWord)
    
    for i in range(len(input) - len(findWord) + 1):
        errors = 0
        match = True
        
        for j in range(len(findWord)):
            if input[i + j] != findWord[j]:
                errors += 1
                if errors > errorRange:
                    match = False
                    break
        
        if match:
            if errors == 0:
                return ((True, True), findWord)
            elif errors <= errorRange:
                output = ((True, False), findWord)
    
    return output

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
        #print("where here")
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
                    #print (contains(self.collectionDic["sample"][poz],baseWord,1 )[0][0])
                    if contains(self.collectionDic["sample"][poz], baseWord, 1)[0][0]:
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
    print("here")
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
        #dicDateinfo = {wanted: [None, None, False] for wanted in usersWants.getWantSet()}
        
        for colIndex, colName in enumerate(df.columns):
            print([(wanted, dicDateinfo[wanted][2]) for wanted in dicDateinfo if not dicDateinfo[wanted][2]])

            if not all(dicDateinfo[wanted][2] for wanted in dicDateinfo):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str):
                    dicKey = remSpecialCharacter(rowName[colName])
                    ''''''''''
                    if (contains(dicKey, "rswell", 1)[0][0] and not dicDateinfo["rswell"][2] and ( contains(dicKey, "rswell", 1)[0][1] or (not contains(dicKey, "sswell", 1)[0][1]))) or ( contains(dicKey, "sswell", 1)[0][0] and not dicDateinfo["sswell"][2]):
                        print( contains(dicKey, "rswell", 1)[0][0] and not dicDateinfo["rswell"][2] and ( contains(dicKey, "rswell", 1)[0][1] or (not contains(dicKey, "sswell", 1)[0][1]))) 
                        print( contains(dicKey, "sswell", 1)[0][0] and not dicDateinfo["sswell"][2])
                    '''''''''
                    if contains(dicKey, "rswell", 2)[0][0] and not dicDateinfo["rswell"][2]:
                        dicKey = "rswell"
                        # print("0000000")
                        if checkVariables(dicKey, df.iat[rowindex + 1, colIndex]):
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex
                    elif contains(dicKey, "sswell", 2)[0][0] and not dicDateinfo["sswell"][2]:
                        dicKey = "sswell"
                        # print("11111111")
                        if checkVariables(dicKey, df.iat[rowindex + 1, colIndex]):
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex
                    elif dicKey in usersWants.getWantSet():
                        # print("2222222")
                        # print("raba")
                        if checkVariables(dicKey, df.iat[rowindex + 1, colIndex]):
                            # print("crab")
                            dicDateinfo[dicKey] = [rowindex, colIndex, True]
                            if maxRow < rowindex:
                                maxRow = rowindex           
            else:
                print('All columns found in row:', rowindex)
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



# Loops through all the information in the dataset 
for file in os.listdir(labResLocation):
    file_path = os.path.join(labResLocation, file)
    if os.path.isfile(file_path) and file_path.endswith(('.xls', '.xlsx', '.csv')) and not file.startswith('~$'):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, header=0)
            else:
                df = pd.read_excel(file_path, header=0, engine='openpyxl')
            
            dataTupple = {wanted: [None, None, False] for wanted in usersWants.getWantSet()}
            #df = df.drop(df.index)
            findWantedColumn(dataTupple, df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
    else:
        print(f"Overlooking {file} due to invalid file.")
        continue
    
    # Makes sure that all the collected information has the same length
    lengths = [len(usersWants.getCollectedData()[col]) for col in usersWants.getWantSet()]
    if len(set(lengths)) != 1:
        print(f"Skipping {file} due to inconsistent data lengths.")
        continue
    
    
    # Output of the collected information
    
''''''''''
for key, value in usersWants.getCollectedData().items():
    print(key + ": " + str(value))
'''''''''''
outputDf = usersWants.swellAvg("rswell").swellAvg("sswell")
new_data_df = pd.DataFrame(outputDf.getCollectedData())
try:
    if os.path.exists(outputLocation):
        if os.path.getsize(outputLocation) > 0:  # Check if file is not empty
            existing_df = pd.read_csv(outputLocation, header=0)
            updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        else:
            updated_df = new_data_df
    else:
        updated_df = new_data_df
    updated_df.to_csv(outputLocation, index=False)
except Exception as e:
    print(f"Error writing to {outputLocation}: {e}")

# Output for the mapped data for the legend
#print("here")
outputDf = usersWants.swellAvg("rswell").swellAvg("sswell")
collectedData = {**outputDf.getCollectedData()}

try:
    new_data_df = pd.DataFrame(collectedData)
    if os.path.exists(mappedoutputLocation):
        if os.path.getsize(mappedoutputLocation) > 0:  # Check if file is not empty
            existing_df = pd.read_csv(mappedoutputLocation, header=0)
            updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        else:
            updated_df = new_data_df
    else:
        updated_df = new_data_df
    updated_df.to_csv(mappedoutputLocation, index=False)
except Exception as e:
    print(f"Error writing to {mappedoutputLocation}: {e}")

print("Data added successfully.")
