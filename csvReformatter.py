# Axioms about input (CSV) data:
#
# 1.) If a value has a ',' '\r' or '\n', the value has quotes around it
# 2.) Values cannot tcontain a '"' in the actual data

import sys
import operator
import re
import datetime

# Global var_iables
buffer = ""
waiting_for_end_quote = False
MAX_BUFFER_LEN = 1000
num_columns = 3 # SET NUMBER OF COLUMNS HERE
buffer_index = 0
records = None
file = None
outfile = None
diagnostics_file = None


# Create a new set of records
#
# Records is an array of arrays of strings, e.g.:
#
# [
#    ["this", "is", "an"],
#    ["example", "of", "records"],
# ]
def create_new_records():
    global records
    records = []
    records.append([])
    return

# This function is called when the buffer length exceeds MAX_BUFFER_LEN.
# This function prints an error and then terminates execution
def buffer_limit_exceeded_exit():
    global MAX_BUFFER_LEN, buffer
    sys.stderr.write('Buffer limit of ' + str(MAX_BUFFER_LEN) + " exceeded\n")
    sys.stderr.write('Buffer contents:\n\n' + buffer + "\n")
    sys.exit()

# Add the byte to the buffer
def add_byte_to_buffer(byte):
    global buffer
    if (len(buffer) == 999):
        buffer_limit_exceeded_exit()
    buffer += str(byte)
    return

def increment_buffer_index():
    global buffer_index, num_columns
    if (buffer_index == (num_columns - 1)):
        buffer_index = 0
    else:
        buffer_index += 1

# Add the contents of the buffer to the records as a value
def add_buffer_as_value():
    global records, num_columns
    curr_ind = len(records) - 1
    last_value_ind = len(records[curr_ind])
    if (last_value_ind == num_columns):
        records.append([])
        curr_ind += 1
    records[curr_ind].append(buffer) # append to records
    clear_buffer() # clear the buffer
    return

# Clear the buffer
def clear_buffer():
    global buffer
    buffer = ""
    return

# Process a byte
def process_byte(byte):
    global waiting_for_end_quote, records, num_columns
    if (byte == ','):
        if (waiting_for_end_quote != True):
            add_buffer_as_value()
        else:
            add_byte_to_buffer(byte)
    elif (byte == '"'):
        if (waiting_for_end_quote):
            waiting_for_end_quote = False
        else:
            waiting_for_end_quote = True
    elif (byte == '\r'):
        return
    elif (byte == '\n'):
        if (waiting_for_end_quote):
            add_byte_to_buffer(byte)
        else:
            if (len(records[len(records)-1]) == (num_columns - 1)): # this ignores newlines at the end of a CSV file
                add_buffer_as_value()
    else:
        add_byte_to_buffer(byte)
    return

def validate_records():
    global records, num_columns
    errors_found = False
    
    for i in range(0, len(records)):
        if (len(records[i]) != num_columns):
            print("validate_records: Error found: len(records[" + str(i) + "]) = " + str(len(records[i])))
            errors_found = True

    if not errors_found:
        print("All records have the correct number of columns")
    return

def dump_formatted_records():
    global records, outfile, num_columns

    var_i = 0
    var_j = 0

    try:
        for i in range(1, len(records)):
            var_i = i
            outfile.write("Record " + str(i) + ":\n")
            for j in range (0, num_columns):
                var_j = j
                outfile.write("\t" + records[0][j] + ': "' + records[i][j] + '"\n')
            outfile.write("\n")
    except IndexError:
        print("Error: i = " + str(var_i) + " j = " + str(var_j))
        print("len(records[i]) = " + str(len(records[i])))
        print("len(records[i-1]) = " + str(len(records[i-1])))
    return

base_filename = "./examples/test" # SET FILENAME HERE (without .csv file extension)
file_ext = ".csv"
filename = base_filename + file_ext
out_filename = base_filename + "_formatted.txt"
file = open(filename)
outfile = open(out_filename, "w")

print(datetime.datetime.now())
print("")

print('Parsing "' + filename + '"')
print("Processing...")

# Create a new records
create_new_records()

# Process the bytes in the file
while True:
    byte = file.read(1)
    if not byte:
        if (len(records[len(records)-1]) == (num_columns - 1)): # this ignores newlines at the end of a CSV file
            add_buffer_as_value()
        break
    else:
        process_byte(byte)

print(str(len(records)) + " lines found ; " + str(len(records) - 1) + " records found") # (first line is header)

print("Validating records...")
validate_records()

print('Dumping formatted records to "' + out_filename + '"')
print("Writing...")
dump_formatted_records()
print('Done writing records to "' + out_filename + '"')

file.close()
outfile.close()

print("")
print(datetime.datetime.now())

