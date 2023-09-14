'''
Replace relation 
'''
import nltk
nltk.download('punkt')
import os
from tqdm import tqdm

dataset_path = '/Users/benphan/NCKU/IIR-Lab/BioCreative/NewData'
all_distinct_data_path = "/Users/benphan/NCKU/IIR-Lab/BioCreative/all_distinct_pair_entities.csv"
input_path = "/Users/benphan/NCKU/IIR-Lab/IIR_Bio_Creative/Data/evaluate_with_entities_identifier_2_no_none_novel_add_groundtruth.pubtator" 

def create_pair_entities_gt(save_path = all_distinct_data_path, dataset_path = dataset_path, debug = True): 
    list_file = os.listdir(dataset_path)
    preprocess_datas = [] 
    for file_path in list_file:
        file_path = os.path.join(dataset_path, file_path)  
        # Step 1: Open the file
        rawDatas = [] 
        text =  ""
        with open(file_path, 'r') as file:
            preprocess = []
            begin = True
            # Step 2: Read and process the contents
            for line in file:
                fields = line.strip().split('\t')
                if len(fields) == 5:
                    preprocess_datas.append(fields[1:]) 
    unique_data = []
    for sublist in preprocess_datas:
        # If the sublist is not in unique_ben, add it
        if sublist not in unique_data:
            unique_data.append(sublist)
    with open(all_distinct_data_path, 'w') as file:
        for data in unique_data:
            if (len(data) == 4):
                line = '\t'.join(data) + '\n'
                file.write(line)
    if debug:
        print(f"The number of all pair entities is {len(preprocess_datas)}")
        print(f"The number of unique pair entities is {len(unique_data)}")
        print(f'Data all distinct pair entities has been successfully saved to {all_distinct_data_path}') 
    return unique_data

def add_pair_entities(input_path, dataset_path): 
    documents = []
    entities = []
    pair_entities = []
    id_document = 0 
    raw_data = []
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

    unique_data = create_pair_entities_gt(all_distinct_data_path, dataset_path)

    entities = []
    count = 0
    #for i, document in enumerate(documents):
    for i, document in enumerate(tqdm(documents, desc="Processing documents")):
        entity = []
        for fields in document: 
            if len(fields) == 6: 
                entity.append(fields[5])
        entities.append(entity)
    
    
        #check pair entities in ground truth
        pair_entities = [] 
        for j, item in enumerate(entity):
            for distict_data in unique_data: 
                if(item == distict_data[1]) or (item == distict_data[2]):
                    if (distict_data[1] in entity) and (distict_data[2] in entity) : 
                        pair_entities.append(distict_data)
        
        unique_pairs = []
        # Iterate through the original list
        for pair in pair_entities:
            # If the pair is not already in the unique_pairs list, add it
            if pair not in unique_pairs:
                unique_pairs.append(pair)
    
    
        for j, pair in enumerate(unique_pairs): 
            if 1 == 1: 
    
                for fields in document: 
                    if len(fields) == 5:
                        if (fields[2] == pair[1] and fields[3] == pair[2]) or (fields[1] == pair[2] and fields[3] == pair[1]): 
                            unique_pairs.remove(pair)
        unique_pairs = [list(x) for x in {tuple(sublist) for sublist in unique_pairs}] 
        count_free_space = 0 
        for fields in document: 
            if len(fields) == 5: 
                count_free_space += 1
        if len(unique_pairs) == 0 and count_free_space == 0:
            # print("------------this is empty-------------")
            documents[i].append('')
        else: 
            for pair in unique_pairs:
                documents[i].append([document[2][0],pair[0],pair[1],pair[2],pair[3]])  
                count += 1   

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
    
    with open(f"{os.path.dirname(input_path)}/ADD_pair_entities_{os.path.basename(input_path)}", "w") as file: 
      file.writelines(lines_new)

    print(f"The number of pair entities have been add: {count}")
    print(f"The output was save in path: {os.path.dirname(input_path)}/ADD_pair_entities_{os.path.basename(input_path)}")

add_pair_entities(input_path, dataset_path)


