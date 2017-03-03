#Script for removing all of the neutral comments
import csv

#Read the comments from the provided file
with open("sentiment-oracle-exclude-comments.csv", "r") as excl:
    reader = csv.reader(excl, delimiter=",")
    second_col = list(zip(*reader))[16]
    excl.close()

#Testing purposes
count=0

#Loop and check for match 
for i in second_col:
    if(i == "Ex"):
        count += 1

print(count)