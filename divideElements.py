import csv
import re
import gpt3

def createCSV():
    name = 'results/divided_elements.csv'
    header = ['req_id', 'operation', 'input', 'pre-condition', 'actor', 'event', 'post-condition', 'output']
    with open(name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()

def create_array_from_txt(file_path):
    result_array = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('F:'):
                line = line[2:]  # Remove 'F:' prefix
            elif line.startswith('NF:'):
                line = line[3:]  # Remove 'NF:' prefix
            line = line.strip()  # Remove leading/trailing whitespaces
            result_array.append(line)

    return result_array

def addLine(line):
    name = 'results/divided_elements.csv'
    with open(name, 'a') as f:
       f.write(line)
       f.write("\n")
    f.close()

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
        elif line.startswith("Event:"):
            event = line.replace("Event:", "").strip()
        elif line.startswith("Pre-Condition:"):
            pre_condition = line.replace("Pre-Condition:", "").strip()
        elif line.startswith("Post-Condition:"):
            post_condition = line.replace("Post-Condition:", "").strip()
    
    final_line = str(idx)+','+operation+','+input_data+','+pre_condition+','+actor+','+event+','+post_condition+','+output
    addLine(final_line)
    




