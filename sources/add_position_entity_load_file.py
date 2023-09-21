import nltk
from tqdm import tqdm
nltk.download('punkt')
import os
import re

all_entity_data_path = "./../Dataset_20_09_23/all_entities.csv"
#input_path = "./../Dataset_20_09_23/Entities-Identifiers-Run1.pubtator"
input_path = "./../Dataset_20_09_23/Entities-Identifiers-Run2.pubtator"
#input_path = "./../demo.pubtator"

def create_pair_entities_gt( all_entity_data_path, debug = True ): 
    unique_data = [] 
    with open(all_entity_data_path, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            if fields[1] == 'Disease':
                fields[1] = 'DiseaseOrPhenotypicFeature'
            elif fields[1] == 'Chemical':
                fields[1] = 'ChemicalEntity'
            elif fields[1] == 'Gene':
                fields[1] = 'GeneOrGeneProduct'
            unique_data.append(fields) 
    print(f"The number of unique pair entities is {len(unique_data)}") 
    print(unique_data[0:100])    
    return unique_data

def add_position_and_entity(all_entity_data_path, input_path = input_path): 
    # Step 1: Open the file

    stop_words = []
    # Read the file and add words to the stop_words list
    with open("stop_words.csv", 'r') as file:
        for line in file:
            word = line.strip()  # Remove leading/trailing whitespace
            if word and not word.startswith("'"):  # Ignore empty lines and words starting with "'"
                stop_words.append(word)

    unique_data = create_pair_entities_gt(all_entity_data_path)
    documents = []
    entities = []
    pair_entities = []
    id_document = 0 
    raw_data = []
    count = 0  
    with open(input_path, 'r') as file:
        lines = file.readlines()
        # Step 2: Read and process the contents
    for i, line in enumerate(lines):
        fields = line.strip().split('\t')
        if  i == 0 and '|t|' in fields[0]:
            position = fields[0].find('|t|')
            id_document = fields[0][:position]
            raw_data.append(fields)  
        elif i == len(lines) - 1:
            raw_data.append(fields) 
            documents.append(raw_data)
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
    
    for i, document in enumerate(tqdm(documents, desc="Processing lines")):
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
            elif len(fields) == 6:
              result_list.append(fields)  
              documents[i] = document[:2]
    
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
    
        sorted_result = sorted(result_list, key=lambda x: (int(x[1]), int(x[2])))
        unique_result = []
        seen_pairs = set()
    
        sorted_result = sorted(result_list, key=lambda x: (int(x[1]), int(x[2])))
    
        unique_results = []
        seen_indices = set()


        # Define a list of stop words
        #stop_words = ["a", "an", "and", "as", "at", "but", "by", "for", "if", "in", "is", "it", "of", "on", "or", "the", "to", "with","has","was","have"] 
        #file_path = "stop_words.csv"

        
        # Initialize unique_results and seen_indices
        unique_results = []
        seen_indices = set()
        
        # Iterate through sorted_result
        for item in sorted_result:
            start_index = int(item[1])
            end_index = int(item[2])
            text = item[3]  # Assuming item[3] contains the text
        
            # Check if text is not a stop word and (start_index, end_index) is not in seen_indices
            if text.lower() not in stop_words and (start_index, end_index) not in seen_indices:
                unique_results.append(item)
                seen_indices.add((start_index, end_index))
                count += 1 
        
        # unique_results now contains items with non-stop words and unique indices



       # for item in sorted_result:
       #     start_index = int(item[1])
       #     end_index = int(item[2])
       #     
       #     # Kiểm tra nếu start_index và end_index chưa xuất hiện trong tập hợp seen_indices
       #     if (start_index, end_index) not in seen_indices:
       #     #if True:
       #         unique_results.append(item)
       #         seen_indices.add((start_index, end_index))
       #         count += 1 
    
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
    
    #with open("/Users/benphan/NCKU/IIR-Lab/BioCreative/test.pubtator", "w") as file: 
    with open(f"{os.path.dirname(input_path)}/Full_entity_{os.path.basename(input_path)}", "w") as file: 
      file.writelines(lines_new)
    
    print(f"The number of entities have been add: {count}")
    print(f"The output was save in path: {os.path.dirname(input_path)}/Full_entity_{os.path.basename(input_path)}")


add_position_and_entity(all_entity_data_path, input_path = input_path)
        
