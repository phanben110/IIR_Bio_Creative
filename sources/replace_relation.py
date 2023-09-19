'''
Replace relation 
'''
import nltk
nltk.download('punkt')
import os
from tqdm import tqdm

dataset_path = './../Dataset_Relation'
all_distinct_data_path = "./../all_distinct_pair_entities.csv"
input_path = "./../Add_Relation/Entities-Identifiers_Relation-Run1.pubtator"

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

def replace_relation(input_path, dataset_path): 
    unique_data = create_pair_entities_gt(all_distinct_data_path, dataset_path)
    with open(input_path, "r") as file:
        lines = file.readlines()
    # Iterate through the lines and replace the specified line
    count = 0 
    for i, line in enumerate(tqdm(lines, desc="Processing lines")): 
        fields = line.strip().split('\t')
        if len(fields) == 5: 
            for distict_data in unique_data:
                if (fields[1] == distict_data[0] and fields[2] == distict_data[1] and fields[3] == distict_data[2]):
                    count += 1 
                    #print(lines[i]) 
                    lines[i] = f"{fields[0]}\t{fields[1]}\t{fields[2]}\t{fields[3]}\t{distict_data[3]}\n"
                    #print(lines[i])
                    #print("-----------------") 
    
    # Write the new file
    #with open("/Users/benphan/NCKU/IIR-Lab/BioCreative/Data/all_no_none_novel_add_groundtruth.pubtator", "w") as file:
    with open(f"{os.path.dirname(input_path)}/Replace_Relation_{os.path.basename(input_path)}", "w") as file: 
        file.writelines(lines)

    print(f"The number of pair entities have been replace: {count}")
    print(f"The output was save in path: {os.path.dirname(input_path)}/Replace_Relation_{os.path.basename(input_path)}")

replace_relation(input_path, dataset_path)
