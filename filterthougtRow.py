import os
import pandas as pd

# Set the file locations
labResLocation = "./data_from_Synthesis_Lab_Spring_2024"
outputLocation = "./rowFilter.csv"
mappedoutputLocation = "./legendRowMapping.csv"
wantedColumns = {"sample", "monomer1", "monomer2", "crosslinkermol"}

# A class that allows for the collection of info that then gets mapped to a number
class HashSetWithIndex:
    def __init__(self, name: str):
        """Initialize the HashSetWithIndex with a name, an element map, and a set for unique elements."""
        self.name = name
        self.elementMap = {}
        self.elementSet = set()

    def add(self, elem):
        """Add a unique element to the set and map it to an index."""
        if elem not in self.elementSet:
            self.elementSet.add(elem)
            self.elementMap[elem] = len(self.elementSet) - 1  # Use len(set) - 1 to start from 0

    def index_of(self, elem):
        """Return the index of the element if it exists, otherwise return -1."""
        return self.elementMap.get(elem, -1)

    def get_dictionary(self):
        """Return a dictionary with the element names and their corresponding indices."""
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
    return ''.join(letter.lower() for letter in colName if letter.isalnum())

# Checks if the input for data is the valid type and not null
def checkvarables(key, append):
    if key in {"sample", "monomer1", "monomer2"}:
        return isinstance(append, str) and append.lower() not in ["-", "none"] and append is not None
    elif key == "crosslinkermol":
        return isinstance(append, (int, float)) and append is not None

# Makes sure that there's input for all information provided
def checkforNulls(hash):
    return all(valueArray[2] for valueArray in hash.values())

def scanWantedCol(dicData, maxRow, df, dataTupple):
    incremenat = 0  # The variable that causes to look at the next row
    while (maxRow + incremenat) < df.shape[0]:
        collectedData = []  # The data that is collected which will later be graphed
        validCollection = True  # This is the bool that is used to check if all the needed information is found
        
        for name, hashInfo in dataTupple.items():
            info = df.iat[int(hashInfo[0]) + incremenat, int(hashInfo[1])]
            if validCollection and checkvarables(name, info):
                collectedData.append(info)
            else:
                validCollection = False
        
        if validCollection:
            dicData["sample"].append(collectedData[0])
            dicData["monomer1"].append(collectedData[1])
            dicData["monomer2"].append(collectedData[2])
            dicData["crosslinkermol"].append(collectedData[3])
            monMaping.add(collectedData[1])
            monMaping.add(collectedData[2])
            dicData["mappedmonomer1"].append(monMaping.index_of(collectedData[1]))
            dicData["mappedmonomer2"].append(monMaping.index_of(collectedData[2]))
        incremenat += 1

def findWantedCollom(dicData, dicDateinfo, df):
    maxRow = 0
    for rowindex, rowName in df.iterrows():
        for colIndex, colName in enumerate(df.columns):
            if not checkforNulls(dicDateinfo):
                if not pd.isna(df.iat[rowindex, colIndex]) and isinstance(rowName[colName], str) and remSpecialCharacter(rowName[colName]) in wantedColumns:
                    dicDateinfo[remSpecialCharacter(rowName[colName])][:2] = [rowindex, colIndex]
                    dicDateinfo[remSpecialCharacter(rowName[colName])][2] = True
                    maxRow = max(maxRow, rowindex)
            else:
                scanWantedCol(dicData, maxRow, df, dicDateinfo)
                return

# The main function

monMaping = HashSetWithIndex("monMaping")

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
    
    lengths = [len(colValueCol[col]) for col in wantedColumns]
    if len(set(lengths)) != 1:
        print(f"Skipping {file} due to inconsistent data lengths.")
        continue
    
    new_data_df = pd.DataFrame(colValueCol)
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

collectedData = monMaping.get_dictionary()


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



print("collectedData")
print(collectedData)
print("Data added successfully.")
