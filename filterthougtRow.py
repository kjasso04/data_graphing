import os
import pandas as pd

labResLocation = "./data_from_Synthesis_Lab_Spring_2024"
outputLocation = "./test_filtered_data.xlsx"
mappedoutputLocation = "./filtered_data.xlsx"
wantedColumns = {"sample", "monomer1", "monomer2", "crosslinkermol"}

# A class that allow for the collection of info that then get mapped to a number
class HashSetWithIndex:
    def __init__(self, name: str):
        self.name = name
        self.elementMap = {}
        self.elementSet = set()

    def add(self, elem):
        if elem not in self.elementSet:
            self.elementSet.add(elem)
            self.elementMap[elem] = len(self.elementSet)

    def index_of(self, elem):
        return self.elementMap.get(elem, -1)

    def getDic(self):
        collectionData = {
            (self.name + " collName"): [],
            (self.name + " mapping"): []
        }
        for name, index in self.elementMap.items():
            collectionData[(self.name + " collName")].append(name)
            collectionData[(self.name + " mapping")].append(index)
        return collectionData
    
# Remove special characters and turn string to lowercase 
def remSpecialCharacter(colName):
    newName = ''
    for letter in colName:
        if letter.isalnum():
            newName += letter.lower()
    return newName

# Checks if the input for data is the valid type and not null
def checkvarables(key, append):
    if key == "sample" or key == "monomer1" or key == "monomer2":
        return isinstance(append, str) and append.lower() not in ["-", "none"]
    elif key == "crosslinkermol":
        return isinstance(append, (int, float))
    
# Makes sure that theres input for all information provided
def checkforNulls(hash):
    return all(valueArray[2] for valueArray in hash.values())

def scanWantedCol(dicData, maxRow, df, dataTupple):
    incremenat = 0 
    while (maxRow + incremenat) < df.shape[0]:
        collectedData = []
        validCollection = True
        for name, hashInfo in dataTupple.items():
            info = df.iat[int(hashInfo[0]) + incremenat, int(hashInfo[1])]
            if validCollection and not pd.isna(info) and checkvarables(name, info):
                collectedData.append(info)
            else:
                validCollection = False
        if validCollection:
            dicData["sample"].append(collectedData[0])
            dicData["monomer1"].append(collectedData[1])
            dicData["monomer2"].append(collectedData[2])
            dicData["crosslinkermol"].append(collectedData[3])
            mon1Maping.add(collectedData[1])
            mon2eMaping.add(collectedData[2])
            dicData["mappedmonomer1"].append(mon1Maping.index_of(collectedData[1]))
            dicData["mappedmonomer2"].append(mon2eMaping.index_of(collectedData[2]))
        incremenat += 1

# Finds the Columns of the wanted information
def findWantedCollom(dicData, dicDateinfo, df):
    maxRow = 0
    for rowindex, rowName in df.iterrows():
        for colIndex, colName in enumerate(df.columns):
            if not checkforNulls(dicDateinfo):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str) and remSpecialCharacter(rowName[colName]) in wantedColumns:
                    dicDateinfo[remSpecialCharacter(rowName[colName])][0] = rowindex
                    dicDateinfo[remSpecialCharacter(rowName[colName])][1] = colIndex
                    dicDateinfo[remSpecialCharacter(rowName[colName])][2] = True
                    if maxRow < rowindex:
                        maxRow = rowindex
            else:
                scanWantedCol(dicData, maxRow, df, dicDateinfo)
                return

mon1Maping = HashSetWithIndex("mon1Maping")
mon2eMaping = HashSetWithIndex("mon2eMaping")

# Loops through all the information in the dataset 
for file in os.listdir(labResLocation):
    file_path = os.path.join(labResLocation, file)
    if os.path.isfile(file_path) and file_path.endswith(('.xls', '.xlsx', '.csv')) and not file.startswith('~$'):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, header=0)
            else:
                df = pd.read_excel(file_path, header=0, engine='openpyxl')

            colValueCol = {
                "sample": [],
                "monomer1": [],
                "monomer2": [],
                "crosslinkermol": [],
                "mappedmonomer1": [],
                "mappedmonomer2": []
            }

            dataTupple = {
                "sample": [None, None, False],
                "monomer1": [None, None, False],
                "monomer2": [None, None, False],
                "crosslinkermol": [None, None, False]
            }

            findWantedCollom(colValueCol, dataTupple, df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
    else:
        print(f"Overlooking {file} due to invalid file.")
        continue
    
    # Makes sure that that all the collected information has the same length
    lengths = [len(colValueCol[col]) for col in wantedColumns]
    if len(set(lengths)) != 1:
        print(f"Skipping {file} due to inconsistent data lengths.")
        continue
    
    # Output of the collected information
    new_data_df = pd.DataFrame(colValueCol)
    try:
        if os.path.exists(outputLocation):
            existing_df = pd.read_excel(outputLocation, header=0, engine='openpyxl')
            updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        else:
            updated_df = new_data_df
        updated_df.to_excel(outputLocation, index=False)
    except Exception as e:
        print(f"Error writing to {outputLocation}: {e}")
        
# Output for the mapped data for the legend
collectedData = {**mon1Maping.getDic(), **mon2eMaping.getDic()}
for key, value in collectedData.items():
    print(f"{key}: {value}")

try:
    new_data_df = pd.DataFrame(collectedData)
    if os.path.exists(mappedoutputLocation):
        existing_df = pd.read_excel(mappedoutputLocation, header=0, engine='openpyxl')
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
    else:
        updated_df = new_data_df
    updated_df.to_excel(mappedoutputLocation, index=False)
except Exception as e:
    print(f"Error writing to {mappedoutputLocation}: {e}")

print("Data added successfully.")
