import csv
import re
import gpt3
# import spacy
# from nltk.tokenize import word_tokenize
# nlp = spacy.load("en_core_web_sm")


# def classify_requirements(requirments):
#     frs = []
#     nfrs = []
#     for x in requirments:
#         if x base_classify(x):

def createCSV():
    name = 'results/divided_elements_FR.csv'
    header = ['req_id', 'operation', 'input', 'pre-condition', 'actor', 'actor-type', 'event', 'post-condition', 'output']
    with open(name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    
    name = 'results/divided_elements_NFR.csv'
    # header = ['req_id', 'nfr_type', 'goal', 'metric', 'scope', 'constraints']
    header = ['req_id', 'nfr_type', 'metric', 'operation', 'input', 'pre-condition', 'actor', 'event', 'post-condition', 'output']
    with open(name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()

def create_array_from_txt(file_path):
    frs = []
    frs_index = []
    nfrs_index = []
    nfrs = []
    idx = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('F:'):
                line = line[2:]  # Remove 'F:' prefix
                line = line.strip()  # Remove leading/trailing whitespaces
                frs.append(line)
                frs_index.append(idx)
            elif line.startswith('NF:'):
                line = line[3:]  # Remove 'NF:' prefix
                line = line.strip()  # Remove leading/trailing whitespaces
                nfrs.append(line)
                nfrs_index.append(idx)
            idx+=1
                
            
    return frs,nfrs, frs_index, nfrs_index

def addLine(line):
    name = 'results/divided_elements_FR.csv'
    with open(name, 'a') as f:
       f.write(line)
       f.write("\n")
    f.close()

def addLineNFR(line):
    name = 'results/divided_elements_NFR.csv'
    with open(name, 'a') as f:
       f.write(line)
       f.write("\n")
    f.close()

def divideAndSetNFR(idx, nfr):
    nfr_type = gpt3.get_NFR_type(nfr)
    for x in nfr_type:
        if x != '':
            nfr_type = x
            break

    dividedElements = gpt3.divideElements(nfr)
    operation = ""
    input_data = ""
    output = ""
    actor = ""
    event = ""
    pre_condition = ""
    post_condition = ""
    metric = ""

    for line in dividedElements:
        line = line.replace(",","")
        if line.startswith("Operation:"):
            operation = line.replace("Operation:", "").strip()
            if operation == '':
                operation = 'None'
        elif line.startswith("Input:"):
            input_data = line.replace("Input:", "").strip()
            if input_data == '':
                input_data = 'None'
        elif line.startswith("Any number value with units:"):
            metric = line.replace("Any number value with units:", "").strip()
        elif line.startswith("Output:"):
            output = line.replace("Output:", "").strip()
            if output == '':
                output = 'None'
        elif line.startswith("Actor:"):
            actor = line.replace("Actor:", "").strip()
            if actor == '':
                actor = 'None'
        elif line.startswith("Event:"):
            event = line.replace("Event:", "").strip()
            if event == '':
                event = 'None'
        elif line.startswith("Pre-Condition:"):
            pre_condition = line.replace("Pre-Condition:", "").strip()
            if pre_condition == '':
                pre_condition = 'None'
        elif line.startswith("Post-Condition:"):
            post_condition = line.replace("Post-Condition:", "").strip()
            if post_condition == '':
                post_condition = 'None'
    
    final_line = str(idx)+','+nfr_type+','+metric+','+operation+','+input_data+','+pre_condition+','+actor+','+event+','+post_condition+','+output
    print(metric)
    addLineNFR(final_line)

def divideAndSet(idx,dividedElements):
    operation = ""
    input_data = ""
    output = ""
    actor = ""
    event = ""
    pre_condition = ""
    post_condition = ""

    for line in dividedElements:
        line = line.replace(",","")
        if line.startswith("Operation:"):
            operation = line.replace("Operation:", "").strip()
            if operation == '':
                operation = 'None'
        elif line.startswith("Input:"):
            input_data = line.replace("Input:", "").strip()
            if input_data == '':
                input_data = 'None'
        elif line.startswith("Output:"):
            output = line.replace("Output:", "").strip()
            if not output:
                output = 'None'
        elif line.startswith("Actor:"):
            actor = line.replace("Actor:", "").strip()
            if actor == '':
                actor = 'None'
        elif line.startswith("Event:"):
            event = line.replace("Event:", "").strip()
            if event == '':
                event = 'None'
        elif line.startswith("Pre-Condition:"):
            pre_condition = line.replace("Pre-Condition:", "").strip()
            if pre_condition == '':
                pre_condition = 'None'
        elif line.startswith("Post-Condition:"):
            post_condition = line.replace("Post-Condition:", "").strip()
            if post_condition == '':
                post_condition = 'None'

    final_line = str(idx)+','+operation+','+input_data+','+pre_condition+','+actor+','+event+','+post_condition+','+output
    addLine(final_line)
    
# def getRequirment(idx):
#     file_path = 'results/requirement_report.txt'
#     idx = int(idx)+1
#     index = 0
#     with open(file_path, 'r') as file:
#         for line in file:
#             line = line.strip()  # Remove leading/trailing whitespaces
#             if index == idx:
#                 return line
#             index+=1

def getConflicts():
    file_path = 'conflicts.txt'
    line_array = []
    index = 0
    a1 = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Funtional Conflicts') or line.startswith('Non-Functional Conflicts'):
                continue
            else:
                a1.append(line)
                if index == 2:
                    line_array.append(a1)
                    index = 0
                    a1 = []
                else:
                    index+=1
    return line_array
                





# # def pos_tagging(text):
# #     tokens = word_tokenize(text)
# #     tokens = [token.lower() for token in tokens]

# #     tagged_tokens = []
# #     for token in tokens:
# #         doc = nlp(token)
# #         for word in doc:
# #             tagged_tokens.append((word.text, word.pos_))

# #     return tagged_tokens

# # reqs = ['The website should provide an online platform for collaborative students access.',
# #         'The website should only allow access to priviliged students.']

# # tagged_tokens = pos_tagging(reqs[0])
# print(tagged_tokens)



