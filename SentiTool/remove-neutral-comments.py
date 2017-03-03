#Script for removing all of the neutral comments
import csv

#Read the comments from the provided file
with open("sentiment-oracle-exclude-comments.csv", "r") as excl, open("Sentiment-comments.csv", "r", encoding="ISO-8859-1") as coms:
    read_one = csv.reader(excl, delimiter=",")
    read_two = csv.reader(coms, delimiter=",")
    flag = list(zip(*read_one))[16]
    comment = list(zip(*read_two))[1]

    excl.close()
    coms.close()
    #excl.close()

index = 0
count = 0

#Loop and check for match 
for i in flag:
    if(i == "Ex"):
        print(comment[index])
        count += 1
    index += 1

print(count)