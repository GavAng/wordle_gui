import json

words = []

with open("wordleWords.txt","r") as readFile:
    for line in readFile:
        words.append(line.strip())

with open("wordleWords.json","w") as writeFile:
        json.dump(words, writeFile, indent=4)