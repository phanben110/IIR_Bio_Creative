import nltk
nltk.download('punkt')

file_path = '/Users/benphan/NCKU/IIR-Lab/BioCreative/Data/Train.pubTator'

# Step 1: Open the file
rawDatas = [] 
preprocess_datas = []
text =  ""
with open(file_path, 'r') as file:
    preprocess = []
    # Step 2: Read and process the contents
    for line in file:
        fields = line.strip().split('\t')
        if fields[0] == "": 
           rawDatas.append(text)
           preprocess_datas.append(preprocess)
          #  print(preprocess)
           text = ""
           preprocess = []
        elif '|t|' in fields[0]: 
          position = fields[0].index('|t|')
          text += str(fields[0][position + 3:])
        elif '|a|' in fields[0]: 
          position = fields[0].index('|a|')
          text = str(text + " " + fields[0][position + 3:]) 
        else:
          if fields[1].isdigit() and fields[2].isdigit(): 
            preprocess.append(fields) 
            if len(fields) >= 6: 
                print(len(fields[5]))
                print(fields[5])

datas = []
for i, rawData in enumerate(rawDatas):
  sentences = nltk.sent_tokenize(rawData)
  position = []
  for j, sentence in enumerate(sentences):
    index = rawData.index(sentence)
    position.append([j , index, index + len(sentence)])
  data_dict = {
                "raw_data": rawData, 
                "sentences": sentences, 
                "position": position,
                "preprocess": preprocess_datas[i],
                "clean_data": preprocess_datas[i] 
                }  
  datas.append(data_dict) 


for i, data in enumerate(datas): 
  # print("Done")
  for item in datas[i]["preprocess"]:
    for j, position in enumerate(datas[i]["position"]):
      if int(item[1]) >= int(position[1]) and int(item[2]) <= int(position[2]):
        item.append(datas[i]["sentences"][position[0]]) 
        #datas[i]["sentences"][position[0]]

with open('ben_deptrai.pubtator', 'w') as file:
    for data in datas:
        for clean_data in data["clean_data"]:
            line = '\t'.join(clean_data) + '\n'
            file.write(line)
