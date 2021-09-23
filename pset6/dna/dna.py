import csv
import sys


def main():

    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Error: There must be exactly 2 command-line arguments.")

    database = []
    sequence = ''
    # Open the CSV file and read it into memory (a 2D list)
    # Open the text file and read it into memory (a string)
    with open(sys.argv[1], 'r') as csv_file, open(sys.argv[2], 'r') as sequence_file:
        data = csv.reader(csv_file)
        for row in data:
            for i in range(1, len(row)):
                if row[i].isnumeric():
                    row[i] = int(row[i])
            database.append(row)
        sequence = sequence_file.read()

    result = []
    # Check the count of each STR in sequence and put them into a list
    for i in range(1, len(database[0])):
        _output = check(database[0][i], sequence)
        result.append(_output)

    match = ''
    # Iterate over the database to check for match with the result
    for i in range(1, len(database)):
        if compare(result, database[i]):
            match = database[i][0]

    # Output the person to whom the DNA most like belongs
    if match == '':
        print("No match")
    else:
        print(match)


# Function to check longest repeated STR sequence in the string
# Return the number of STRs in that sequence
def check(strseq, data):
    longest_count = 0       # Keep track of the longest count
    current_count = 0       # Keep track of the current count
    seq_size = len(strseq)
    i = 0                   # Use a variable and string slicing to traverse through the data sequence

    # Traverse through the data sequence and check for STR
    while i < len(data):
        # If a match is found, calculate the count of that sequence
        if data[i:(i + seq_size)] == strseq:
            current_count += 1
            if (i + seq_size) <= len(data):
                i += seq_size
            continue    # Continue will skip the rest of the code in current iteration and jump to the next iteration of the loop

        # Check if the current count is the longest, if not, move on to search in the data sequence
        else:
            if current_count > longest_count:
                longest_count = current_count
                current_count = 0
            else:
                current_count = 0
        i += 1

    return longest_count


# Function to compare the result and a row of database minus 1st element (lists)
# Return True if matches, otherwise return False
def compare(result, data):
    for i in range(len(result)):
        if result[i] != data[i+1]:
            return False
    return True


if __name__ == "__main__":
    main()