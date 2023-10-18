import csv;
import math;

def gatherInfo(csv_file):
	objectList = [];

	with open(csv_file, mode='r') as file:
		reader = csv.reader(file);
		for row in reader:
			temp = {};
			temp["bin"] = None;
			temp["count"] = 1;
			temp["value"] = float(row[0]);
			objectList.append(temp);

	return objectList;

def createNewDataObjectsList(dataObjects):
	tempDataObjectsList = [];
	smallestNumberIndex = -1;
	smallestNumber = float("inf");

	for i in range(0,len(dataObjects)-1):
		number = dataObjects[i+1]["value"] - dataObjects[i]["value"];
		if number < smallestNumber:
			smallestNumber = number;
			smallestNumberIndex = i;

	if smallestNumberIndex == 0:
		temp = {};
		temp["bin"] = None;
		temp["count"] = dataObjects[smallestNumberIndex]["count"] + dataObjects[smallestNumberIndex+1]["count"];
		temp["value"] = ((dataObjects[smallestNumberIndex]["count"]*dataObjects[smallestNumberIndex]["value"]) + (dataObjects[smallestNumberIndex+1]["count"]*dataObjects[smallestNumberIndex+1]["value"]))/temp["count"];
		tempDataObjectsList.append(temp);
		tempDataObjectsList.extend(dataObjects[smallestNumberIndex+2:len(dataObjects)]);
	elif smallestNumberIndex == len(dataObjects)-1:
		tempDataObjectsList.extend(dataObjects[0:smallestNumberIndex-1]);
		temp = {};
		temp["bin"] = None;
		temp["count"] = dataObjects[smallestNumberIndex]["count"] + dataObjects[smallestNumberIndex+1]["count"];
		temp["value"] = ((dataObjects[smallestNumberIndex]["count"]*dataObjects[smallestNumberIndex]["value"]) + (dataObjects[smallestNumberIndex+1]["count"]*dataObjects[smallestNumberIndex+1]["value"]))/temp["count"];
		tempDataObjectsList.append(temp);
	else:
		tempDataObjectsList.extend(dataObjects[0:smallestNumberIndex]);
		temp = {};
		temp["bin"] = None;
		temp["count"] = dataObjects[smallestNumberIndex]["count"] + dataObjects[smallestNumberIndex+1]["count"];
		temp["value"] = ((dataObjects[smallestNumberIndex]["count"]*dataObjects[smallestNumberIndex]["value"]) + (dataObjects[smallestNumberIndex+1]["count"]*dataObjects[smallestNumberIndex+1]["value"]))/temp["count"];
		tempDataObjectsList.append(temp);
		tempDataObjectsList.extend(dataObjects[smallestNumberIndex+2:len(dataObjects)]);

	return tempDataObjectsList;

def findNewEntropy(dataObjects,totalLength):
	entropy = 0;

	for data in dataObjects:
		entropy += (data["count"]/totalLength)*math.log2(totalLength/data["count"]);

	return entropy;

def findNewDelta(x1,x2):
	if x1 == None:
		return None;
	return x1 - x2;

def findDeltaChange(x1,x2):
	if x1 == None:
		return None;
	return x2 - x1;

def getBins(dataObjects,iterations,entropy,delta,totalLength):

	print(f"Iteration {iterations}:\n");
	newDataObjects = createNewDataObjectsList(dataObjects);
	printObjectList(newDataObjects);
	print("\n");
	newEntropy = findNewEntropy(newDataObjects,totalLength);
	print("Old Entropy: ", entropy, " : New Entropy: ",newEntropy);
	newDelta = findNewDelta(entropy,newEntropy);
	print("Old Delta: ", delta, " : New Delta: ",newDelta);
	deltaChange = findDeltaChange(delta,newDelta);
	print("Delta Change: ",deltaChange);
	print("\n--------------------------------------------\n");
	
	if(iterations == 0):
		bins = [];
		for data in newDataObjects:
			bins.append(data["value"]);

		return bins;

	return getBins(newDataObjects,iterations-1,newEntropy,newDelta,totalLength);

def printObjectList(dataObjects):
	for o in dataObjects:
		print("[",o["value"]," : ",o["bin"]," : ",o["count"],"]");

def setBins(dataObjects):
	for data in objectList:
		for i in range(0,len(bins)):
			if data["value"] <= bins[i]:
				data["bin"] = i;
				break;

		if data["bin"] == None:
			data["bin"] = len(bins);


csv_file = 'input2.csv'
objectList = gatherInfo(csv_file);
objectList = sorted(objectList, key=lambda x: x['value']);

bins = getBins(objectList,5,findNewEntropy(objectList,len(objectList)),None,len(objectList));

for data in objectList:
	for i in range(0,len(bins)):
		if data["value"] <= bins[i]:
			data["bin"] = i;
			break;

	if data["bin"] == None:
		data["bin"] = len(bins);


print(bins);
setBins(objectList);
print("\n--------------------------------------------\n");
printObjectList(objectList);