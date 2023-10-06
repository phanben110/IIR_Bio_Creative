file = open("AIONER.pubtator", 'r')
Lines = file.readlines()

cheatedIDlist = []
for line in Lines:
    splitted = line.split('|')
    if(len(splitted) == 3 and str(splitted[2]).strip() == '- No Title -'):
        cheatedID = splitted[0]
        cheatedIDlist.append(cheatedID)
print(f'Cheated list len: {len(cheatedIDlist)}')
print(cheatedIDlist)
file.close()

file2 = open("Subtask2_Run3.pubtator", 'r')
Lines = file2.readlines()
NewLines = []
for line in Lines:
    newline = line
    splitted1 = line.split('|')
    if(len(splitted1) == 3 and str(splitted1[1]).strip() == 't'):
        cheatedID = splitted1[0]
        if (cheatedID in cheatedIDlist):
            newline = cheatedID+ '|t|- No Title -\n'
            # NewLines.append(newline)
    if(len(splitted1) == 3 and str(splitted1[1]).strip() == 'a'):
        cheatedID = splitted1[0]
        if (cheatedID in cheatedIDlist):
            newline = cheatedID+ '|a|\n'
            # NewLines.append(newline)
    splitted2 = line.split('\t')
    if(len(splitted2) > 3 and splitted2[0] in cheatedIDlist):
       continue
    NewLines.append(newline)
result = ''.join(NewLines)
with open("Update_Subtask2_Run3.pubtator", 'w') as output_file:
    output_file.write(result)