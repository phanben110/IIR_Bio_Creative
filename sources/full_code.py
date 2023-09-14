import nltk
nltk.download('punkt')
import os

list_file = os.listdir('/Users/benphan/NCKU/IIR-Lab/BioCreative/NewData')
preprocess_datas = [] 
for file_path in list_file:
    output_path = os.path.join('/Users/benphan/NCKU/IIR-Lab/BioCreative/NewData_Add_Sentence', f"{file_path[:-9]}_relation.csv") 
    file_path = os.path.join('/Users/benphan/NCKU/IIR-Lab/BioCreative/NewData', file_path)  


    # Step 1: Open the file
    rawDatas = [] 
    text =  ""
    with open(file_path, 'r') as file:
        preprocess = []
        begin = True
        # Step 2: Read and process the contents
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) == 6:
                preprocess_datas.append(fields[3:]) 
            #  pri
                # preprocess.append(fields) 
unique_data = []

for sublist in preprocess_datas:
    # If the sublist is not in unique_ben, add it
    if sublist not in unique_data:
        unique_data.append(sublist)

print(len(preprocess_datas)) 
print(len(unique_data))
with open("distinct_all_data.csv", 'w') as file:
    for data in unique_data:
        if (len(data) == 4):
            line = '\t'.join(data) + '\n'
            file.write(line)

print(f'Data has been successfully saved to {output_path}')

import os
file_path = "/Users/benphan/NCKU/IIR-Lab/BioCreative/Data/all_full_submit.pubtator"

# Step 1: Open the file
documents = []
entities = []
pair_entities = []
id_document = 0 
raw_data = []
with open(file_path, 'r') as file:
    lines = file.readlines()
    # Step 2: Read and process the contents
for i, line in enumerate(lines):
    fields = line.strip().split('\t')
    if  i == 0 and '|t|' in fields[0]:
        position = fields[0].find('|t|')
        id_document = fields[0][:position]
        raw_data.append(fields)  
        print(id_document) 
    elif i == len(lines) - 1:
        raw_data.append(fields) 
        documents.append(raw_data)
        print(fields)
    elif '|t|' in fields[0]:
        position = fields[0].find('|t|')
        id_document = fields[0][:position]
        documents.append(raw_data)
        raw_data = [] 
        raw_data.append(fields) 
    elif '|a|' in fields[0]:
        position = fields[0].find('|a|')
        if id_document == fields[0][:position] : 
            raw_data.append(fields)  
    elif id_document == fields[0]: 
        raw_data.append(fields)

import re
for i, document in enumerate(documents):
    document_id = ""
    begin = True
    text = ""
    result_list = []
    for fields in document: 
        if '|t|' in fields[0]:
          begin = False
          position = fields[0].index('|t|')
          text += str(fields[0][position + 3:])
          document_id = fields[0][:position]
        elif '|a|' in fields[0]: 
          position = fields[0].index('|a|')
          text = str(text + " " + fields[0][position + 3:])


    for item in unique_data:
        keyword = item[0]
        # Sử dụng biểu thức chính quy để kiểm tra xem keyword có là một từ hoàn chỉnh hay không
        if re.search(r'\b{}\b'.format(re.escape(keyword)), text):
            start_indices = []
            start_index = text.find(keyword)

            while start_index != -1:
                end_index = start_index + len(keyword) 
                if text[end_index] == " " or text[end_index] == "," or text[end_index] == "." or text[end_index] == "!": 
                  result_list.append([document_id, str(start_index), str(end_index), item[0], item[1], item[2]])
                start_index = text.find(keyword, end_index)

    # for item in unique_data:
    #     keyword = item[0]
    #     # Sử dụng biểu thức chính quy để kiểm tra từ hoàn chỉnh
    #     pattern = r'\b' + re.escape(keyword) + r'\b'
    #     start_indices = [match.start() for match in re.finditer(pattern, text)]
    #     for start_index in start_indices:
    #         end_index = start_index + len(keyword)
    #         print(text[end_index:end_index + 1])
    #         print(end_index)
    #         if (text[end_index:end_index + 1]) == " " : 
    #           result_list.append([document_id, str(start_index), str(end_index), item[0], item[1], item[2]])



    sorted_result = sorted(result_list, key=lambda x: (int(x[1]), int(x[2])))
    unique_result = []
    seen_pairs = set()

    sorted_result = sorted(result_list, key=lambda x: (int(x[1]), int(x[2])))

    unique_results = []
    seen_indices = set()

    for item in sorted_result:
        start_index = int(item[1])
        end_index = int(item[2])
        
        # Kiểm tra nếu start_index và end_index chưa xuất hiện trong tập hợp seen_indices
        if (start_index, end_index) not in seen_indices:
            unique_results.append(item)
            seen_indices.add((start_index, end_index))

    # print(unique_results)

    documents[i].extend(unique_results) 

lines_new = []
for document in documents:
    for i, fields in enumerate(document):
       line = ""
       for j, field in enumerate(fields):
          if j == 0: 
             line = line + field    
          else: 
            line = line + "\t" + field
       line = line + "\n" 
       lines_new.append(line) 
    lines_new.append('\n')

with open("/Users/benphan/NCKU/IIR-Lab/BioCreative/test.pubtator", "w") as file: 
  file.writelines(lines_new)


        
