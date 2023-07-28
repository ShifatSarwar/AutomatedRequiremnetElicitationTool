import csv
import re
import numpy as np
# from gensim.models import KeyedVectors
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity


def extract_number_and_unit(text):
    none_array = ['None', 'N/A', 'none', 'n/a', '']
    for x in none_array:
        if x == text:
            return -1,''
    # Regular expression pattern to extract numbers with optional decimal point
    number_pattern = r'\d+(\.\d+)?'
    
    # Regular expression pattern to extract the unit (assuming it is a single word)
    unit_pattern = r'\b\w+\b'
    
    # Find all occurrences of numbers in the text
    numbers = re.findall(number_pattern, text)
    
    # Find all occurrences of units in the text
    units = re.findall(unit_pattern, text)

    if not numbers:
        return -1, None
    
    return numbers, units


def read_csv_file_fr():
    file_path = 'results/divided_elements_FR.csv'
    requirements = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            requirements.append(row)

    return requirements

def read_csv_file_nfr():
    file_path = 'results/divided_elements_NFR.csv'
    requirements = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            requirements.append(row)

    return requirements

def checkSimilarity(req1, req2, element):
    print(req1, req2)
    none_array = ['None', 'N/A', 'none', 'n/a', '']
    for x in none_array:
        if (x == req1) or (x == req2):
            return 3
    
    # Load pre-trained BERT model and tokenizer
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    # Step 2: Access word vectors for the elements
    req1 = req1.lower()
    req2 = req2.lower()
    # Use regular expression to remove anything but alphabets (A-Z and a-z)
    req1 = re.sub(r'[^a-z]', ' ', req1)
    req2 = re.sub(r'[^a-z]', ' ', req2)
    # Remove multiple spaces and replace them with a single space
    req1 = re.sub(r'\s+', ' ', req1).strip()
    req2 = re.sub(r'\s+', ' ', req2).strip()

    outputs_1 = tokenizer(req1, return_tensors="pt", padding=True, truncation=True)
    outputs_2 = tokenizer(req2, return_tensors="pt", padding=True, truncation=True)
    outputs_1 = model(**outputs_1)
    outputs_2 = model(**outputs_2)
    embedding_1 = torch.mean(outputs_1.last_hidden_state, dim=1)  # Mean pooling
    embedding_2 = torch.mean(outputs_2.last_hidden_state, dim=1)  # Mean pooling
    
    # Convert embeddings to numpy arrays and calculate cosine similarity
    embedding_1 = embedding_1.detach().numpy()
    embedding_2 = embedding_2.detach().numpy()
    similarity_score = cosine_similarity(embedding_1, embedding_2)[0][0]
    if similarity_score > 0.65:
        return 1
    return 2

def check_functional_conflict(req1, req2):
    trueValues = [1,3]
    falseValues = [2,3]
    if checkSimilarity(req1['operation'],req2['operation'], 1) in trueValues:
        if checkSimilarity(req1['actor'],req2['actor'], 2) in trueValues: 
            if checkSimilarity(req1['output'], req2['output'],5) in falseValues:
                reason = 'Same actor and operation generates different output'
                return True, reason
        
        if checkSimilarity(req1['actor'],req2['actor'], 2) in falseValues:
            reason = 'The operations are same but the actors are different.'
            return True, reason 
        elif checkSimilarity(req1['event'],req2['event'], 3) in falseValues:
            reason = 'The operations are same but the events are different.'
            return True, reason

    else:
        if checkSimilarity(req1['post-condition'],req2['post-condition'],4) in trueValues:
            reason = 'The operations are different but the post-conditions are same.'
            return True, reason
        elif checkSimilarity(req1['output'],req2['output'],5)in trueValues:
            reason = 'The operations are different but generates the same output.'
            return True, reason
        elif checkSimilarity(req1['input'],req2['input'],6) in trueValues:
            if checkSimilarity(req1['pre-condition'],req2['pre-condition'],4) in trueValues:
                reason = 'The operations are different but both pre-condtions and inputs are same.'
                return True, reason
            elif checkSimilarity(req1['actor'],req2['actor'],2) in trueValues:
                reason = 'The operations are different but both actors and inputs are same.'
                return True, reason
        elif checkSimilarity(req1['event'],req2['event'],3) in trueValues:
            reason = 'The operations are different but the events are same.'
            return True, reason
    return False,''

def check_nonfunctional_conflict(req1, req2):
    trueValues = [1,3]
    falseValues = [2,3]
    if req1['nfr_type'] == req2['nfr_type']: 
        if checkSimilarity(req1['metric'], req2['metric'],3) in trueValues:
            if checkSimilarity(req1['scope'], req2['scope'],5) in falseValues:
                return True, 'Scope Issues'
            elif checkSimilarity(req1['constraints'], req2['constraints'],4) in falseValues:
                return True, 'Constraint Issues'

    else:
        if checkSimilarity(req1['scope'], req2['scope'],3) in trueValues:
            if checkSimilarity(req1['goal'], req2['goal'],5) in trueValues:
                return True, 'Contradictions'
            elif checkSimilarity(req1['constraints'], req2['constraints'],4) in trueValues:
                return True, 'Constraint issues'
    return False,''

    
def find_functional_conflicts(requirements):
    conflict_list = []
    for i in range(len(requirements)):
        for j in range(i+1, len(requirements)):
            conflict, reason = check_functional_conflict(requirements[i], requirements[j])
            if conflict:
                conflict_list.append([requirements[i]['req_id'], requirements[j]['req_id'], reason])
    return conflict_list

def find_nonfunctional_conflicts(requirements):
    conflict_list = []
    for i in range(len(requirements)):
        for j in range(i+1, len(requirements)):
            conflict, reason = check_nonfunctional_conflict(requirements[i], requirements[j])
            if conflict:
                conflict_list.append([requirements[i]['req_id'], requirements[j]['req_id'], reason])
    return conflict_list

def update_final_report(req1, req2, updated_req):
    input_file = 'results/final_report.txt'
    # Open input and output files
    updated_files = ''
    with open(input_file, 'r') as file_in:
        for line in file_in:
            if req1 in line or req2 in line:
                continue
            else:
                updated_files+=line


    with open(input_file, 'w') as file_out:
        if updated_files != '':
            file_out.write(updated_files)
        file_out.write(updated_req+'\n')


def read_line_from_file(line_number):
    file_path = 'results/final_report.txt'
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, 1):
            if line_num == int(line_number)+1:
                return line.strip()  # Remove newline character from the end of the line
    return line_number  # Line number not found in the file

def create_conflict_list(conflicts, fr):
    # File path and name
    file_path = "conflicts.txt"
    lines = []
    if fr:
        lines.append('Funtional Conflicts')
    else:
        lines.append('Non-Functional Conflicts')

    for x in conflicts:
        lines.append(read_line_from_file(x[0]))
        lines.append(read_line_from_file(x[1]))
        lines.append('Reason: '+ x[2])

    # Open the file in write mode ('w') and write lines to it
    with open(file_path, "a") as file:
        for line in lines:
            file.write(line + "\n")
