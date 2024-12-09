import os
import csv

dataFilePath = 'data.txt'

data = {}

if os.path.exists(dataFilePath):
    with open(dataFilePath, 'r') as dataFile:
        for row in csv.reader(dataFile):
            if len(row) > 1:
                data[row[0]] = row[1]

def updateData(key: str, value: str) -> None:
    data[key] = value

def retrieveData(key: str, defaultValue = None) -> str | None:
    return data.get(key, defaultValue)

def writeAll():
    with open(dataFilePath, mode='w') as dataFile:
        writer = csv.writer(dataFile)
        writer.writerows(data.items())