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
        self.wantedColumns = set(["sample", "monomer1", "monomer2", "crosslinkermol"])
        self.wantedTypeDic = {
            "sample": str,
            "monomer1": str,
            "monomer2": str,
            "crosslinkermol": (int, float)
            
        }
        self.collectionDic = {
            "sample": [],
            "monomer1": [],
            "monomer2": [],
            "crosslinkermol": [],
            "monomer1mapped": [],
            "monomer2mapped": []
        }
        self.mappingHash = HashSetWithIndex("mapping")
        
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

# Finds the Columns of the wanted information
def findWantedColumn( dicDateinfo, df):
    maxRow = 0
    for rowindex, rowName in df.iterrows():
        for colIndex, colName in enumerate(df.columns):
            if not all(dicDateinfo[2] for dicDateinfo in dicDateinfo.values()):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str) and remSpecialCharacter(rowName[colName]) in usersWants.getWantSet():
                    dicDateinfo[remSpecialCharacter(rowName[colName])][0] = rowindex
                    dicDateinfo[remSpecialCharacter(rowName[colName])][1] = colIndex
                    dicDateinfo[remSpecialCharacter(rowName[colName])][2] = True
                    if maxRow < rowindex:
                        maxRow = rowindex
            else:
                scanWantedCol( maxRow, df, dicDateinfo)
                return

# ______ main _______

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
new_data_df = pd.DataFrame(usersWants.getCollectedData())
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
collectedData = {**usersWants.getMapDataSet()}

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
