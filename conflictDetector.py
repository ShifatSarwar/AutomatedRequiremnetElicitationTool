import csv
from gpt3 import checkSimilarity

def read_csv_file():
    file_path = 'results/divided_elements.csv'
    requirements = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            requirements.append(row)

    return requirements


def check_conflict(req1, req2):
    if checkSimilarity(req1['operation'],req2['operation']):
        if not checkSimilarity(req1['actor'],req2['actor']): 
            reason = 'The operations are same but the actors are different.'
            return True, reason
        elif not checkSimilarity(req1['event'],req2['event']):
            reason = 'The operations are same but the events are different.'
            return True, reason
    else:
        if checkSimilarity(req1['post-condition'],req2['post-condition']):
            reason = 'The operations are different but the post-conditions are same.'
            return True, reason
        elif checkSimilarity(req1['output'],req2['output']):
            reason = 'The operations are different but generates the same output.'
            return True, reason
        elif checkSimilarity(req1['input'],req2['input']):
            if checkSimilarity(req1['pre-condition'],req2['pre-condition']):
                reason = 'The operations are different but both pre-condtions and inputs are same.'
                return True, reason
            elif checkSimilarity(req1['actor'],req2['actor']):
                reason = 'The operations are different but both actors and inputs are same.'
                return True, reason
        elif checkSimilarity(req1['event'],req2['event']):
            reason = 'The operations are different but the events are same.'
            return True, reason
    return False,''

def find_conflicts(requirements):
    conflict_list = []
    for i in range(len(requirements)):
        for j in range(i+1, len(requirements)):
            conflict, reason = check_conflict(requirements[i], requirements[j])
            if conflict:
                conflict_list.append([requirements[i]['req_id'], requirements[j]['req_id'], reason])
    return conflict_list



# # if req1['operation'] == req2['operation'] and req1['actor'] != req2['actor']:
    #     reason = 'The operations are same but the actors are different.'
        
    #     return True, reason
    # elif checkSimilarity(req1['operation'],req2['operation']) and not checkSimilarity(req1['actor'],req2['actor']):
    
    # # elif req1['operation'] == req2['operation'] and req1['event'] != req2['event']:
    #     reason = 'The operations are same but the events are different.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['post-condition'] == req2['post-condition']:
    #     reason = 'The operations are different but the post-conditions are same.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['output'] == req2['output']:
    #     reason = 'The operations are different but generates the same output.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['pre-condition'] == req2['pre-condition'] and req1['input'] == req2['input']:
    #     reason = 'The operations are different but both pre-condtions and inputs are same.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['actor'] == req2['actor'] and req1['input'] == req2['input']:
    #     reason = 'The operations are different but both actors and inputs are same.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['event'] == req2['event']:
    #     reason = 'The operations are different but the events are same.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['event'] == req2['event'] and req1['pre-condition'] == req2['pre-condition']:
    #     reason = 'The operations are different but both events and pre-conditions are same.'
    #     return True, reason
    # # elif req1['operation'] != req2['operation'] and req1['event'] == req2['event'] and req1['actor'] == req2['actor']:
    #     reason = 'The operations are different but both events and actors are same.'
    #     return True, reason
