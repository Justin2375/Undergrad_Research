#Script for removing all of the neutral comments
import csv

#Read the comments from the provided file
with open("SentiTool/sentiment-oracle-exclude-comments.csv", "r") as excl, open("SentiTool/Sentiment-comments.csv", "r", encoding="ISO-8859-1") as coms, open("SentiTool/Updated-comments.csv", "w") as out:
    read_one = csv.reader(excl)
    read_two = csv.reader(coms)
    writer = csv.writer(out)
    

    #Create a list of the remove or not flags
    flag = list(zip(*read_one))[16]
    comments_csv = list(read_two)

    index = 0

    #Loop and check for match 
    for row in comments_csv:
        if(index != len(flag)):
            if(flag[index] != "Ex"):
                print(row)
                writer.writerow(row)
            index += 1

    excl.close()
    coms.close()
    out.close()
