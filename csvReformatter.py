# Axioms about input (CSV) data:
#
# 1.) If a value has a ',' '\r' or '\n', the value has quotes around it
# 2.) Values cannot tcontain a '"' in the actual data

import sys
import operator
import re
import datetime

# Global variables
buffer = ""
waitingForEndQuote = False
maxBufferLen = 1000
numColumns = 39 # SET NUMBER OF COLUMNS HERE
bufferIndex = 0
records = None
file = None
outfile = None
diagnosticsfile = None


# Create a new set of records
#
# Records is an array of arrays of strings, e.g.:
#
# [
#    ["this", "is", "an"],
#    ["example", "of", "records"],
# ]
def createNewRecords():
    global records
    records = []
    records.append([])
    return

# This function is called when the buffer length exceeds maxBufferLen.
# This function prints an error and then terminates execution
def bufferLimitExceededExit():
    global maxBufferLen, buffer
    sys.stderr.write('Buffer limit of ' + str(maxBufferLen) + " exceeded\n")
    sys.stderr.write('Buffer contents:\n\n' + buffer + "\n")
    sys.exit()

# Add the byte to the buffer
def addByteToBuffer(byte):
    global buffer
    if (len(buffer) == 999):
        bufferLimitExceededExit()
    buffer += str(byte)
    return

def incrementBufferIndex():
    global bufferIndex, numColumns
    if (bufferIndex == (numColumns - 1)):
        bufferIndex = 0
    else:
        bufferIndex += 1

# Add the contents of the buffer to the records as a value
def addBufferAsValue():
    global records, numColumns
    currInd = len(records) - 1
    lastValueInd = len(records[currInd])
    if (lastValueInd == numColumns):
        records.append([])
        currInd += 1
    records[currInd].append(buffer) # append to records
    clearBuffer() # clear the buffer
    return

# Clear the buffer
def clearBuffer():
    global buffer
    buffer = ""
    return

# Process a byte
def processByte(byte):
    global waitingForEndQuote, records, numColumns
    if (byte == ','):
        if (waitingForEndQuote != True):
            addBufferAsValue()
        else:
            addByteToBuffer(byte)
    elif (byte == '"'):
        if (waitingForEndQuote):
            waitingForEndQuote = False
        else:
            waitingForEndQuote = True
    elif (byte == '\r'):
        return
    elif (byte == '\n'):
        if (waitingForEndQuote):
            addByteToBuffer(byte)
        else:
            if (len(records[len(records)-1]) == (numColumns - 1)): # this ignores newlines at the end of a CSV file
                addBufferAsValue()
    else:
        addByteToBuffer(byte)
    return

def validateRecords():
    global records, numColumns
    errorsFound = False
    
    for i in range(0, len(records)):
        if (len(records[i]) != numColumns):
            print("validateRecords: Error found: len(records[" + str(i) + "]) = " + str(len(records[i])))
            errorsFound = True

    if not errorsFound:
        print("All records have the correct number of columns")
    return

def dumpFormattedRecords():
    global records, outfile, numColumns

    vari = 0
    varj = 0

    try:
        for i in range(1, len(records)):
            vari = i
            outfile.write("Record " + str(i) + ":\n")
            for j in range (0, numColumns):
                varj = j
                outfile.write("\t" + records[0][j] + ': "' + records[i][j] + '"\n')
            outfile.write("\n")
    except IndexError:
        print("Error: i = " + str(vari) + " j = " + str(varj))
        print("len(records[i]) = " + str(len(records[i])))
        print("len(records[i-1]) = " + str(len(records[i-1])))
    return

baseFilename = "./FILENAME" # SET FILENAME HERE
fileExt = ".csv"
filename = baseFilename + fileExt
outfilename = baseFilename + "_formatted.txt"
file = open(filename)
outfile = open(outfilename, "w")

print(datetime.datetime.now())
print("")

print('Parsing "' + filename + '"')
print("Processing...")

# Create a new records
createNewRecords()

# Process the bytes in the file
while True:
    byte = file.read(1)
    if not byte:
        if (len(records[len(records)-1]) == (numColumns - 1)): # this ignores newlines at the end of a CSV file
            addBufferAsValue()
        break
    else:
        processByte(byte)

print(str(len(records)) + " lines found ; " + str(len(records) - 1) + " records found") # (first line is header)

print("Validating records...")
validateRecords()

print('Dumping formatted records to "' + outfilename + '"')
print("Writing...")
dumpFormattedRecords()
print('Done writing records to "' + outfilename + '"')

file.close()
outfile.close()

print("")
print(datetime.datetime.now())

