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
    header = ['req_id', 'nfr_type', 'goal', 'metric', 'scope', 'constraints']
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

    print(nfr_type)
    dividedElements = gpt3.get_NFR_task(nfr)
    goal = ""
    scope = ""
    metric = ""
    constraints = ""
    for line in dividedElements:
        line = line.replace(",","")
        if line.startswith("Goal:"):
            goal = line.replace("Goal:", "").strip()
        elif line.startswith("Metrics:"):
            metric = line.replace("Metrics:", "").strip()
        elif line.startswith("Scope:"):
            scope = line.replace("Scope:", "").strip()
        elif line.startswith("Constraints:"):
            constraints = line.replace("Constraints:", "").strip()

    
    final_line = str(idx)+','+nfr_type+','+goal+','+scope+','+metric+','+constraints
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
        elif line.startswith("Input:"):
            input_data = line.replace("Input:", "").strip()
        elif line.startswith("Output:"):
            output = line.replace("Output:", "").strip()
        elif line.startswith("Actor:"):
            actor = line.replace("Actor:", "").strip()
        elif line.startswith("Actor-Type:"):
            actor_type = line.replace("Actor-Type:", "").strip()
        elif line.startswith("Event:"):
            event = line.replace("Event:", "").strip()
        elif line.startswith("Pre-Condition:"):
            pre_condition = line.replace("Pre-Condition:", "").strip()
        elif line.startswith("Post-Condition:"):
            post_condition = line.replace("Post-Condition:", "").strip()
    
    final_line = str(idx)+','+operation+','+input_data+','+pre_condition+','+actor+','+actor_type+','+event+','+post_condition+','+output
    addLine(final_line)
    
def getRequirment(idx):
    file_path = 'results/requirement_report.txt'
    idx = int(idx)+1
    index = 0
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if index == idx:
                return line
            index+=1


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



