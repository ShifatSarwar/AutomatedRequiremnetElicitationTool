import openai
API_KEY = "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"
openai.api_key = API_KEY
model = 'text-davinci-003'

# Edit API_KEY by adding your personal key here
def getGPT3_Result(filename):
    with open(filename, 'r') as file:
        text = file.read()

    prompt = text+'Get the requirements from this text.'

    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=200,
        temperature = 0.9,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')

    return gptOutput

def divideElements(requiement):
    prompt = 'Divide the elements (Operation, Input, Output, Actor, Actor-Type, Event, Pre-Condition, Post-Condition) from this requirement text: ' + requiement + '. Assume only if element cannot be directly gathered from text.'

    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=len(requiement),
        temperature = 0.1,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')

    return gptOutput

# def checkSimilarity(req1, req2, element):
#     if 'None' in req1 or 'None' in req2:
#         return False
#     if 'N/A' in req1 or 'N/A' in req2:
#         return False
#     if 'n/a' in req1 or 'n/a' in req2:
#         return False
#     if req1 == '' or req2 == '':
#         return False
    
#     prompt_addition = ' and only provide True or False as your output'
#     if element == 1:
#         prompt = 'Determine if '+req1+' and '+req2+' are the same operation'
#     elif element == 2:
#         prompt = 'Determine if '+req1+' and '+req2+' represents the same actor with same privilages'
#     elif element == 3:
#         prompt = 'Determine if '+req1+' and '+req2+' represents the same event'
#     elif element == 4:
#         prompt = 'Determine if '+req1+' and '+req2+' represents the same condition'
#     elif element == 5:
#         prompt = 'Determine if '+req1+' and '+req2+' can be considered as the same output'
#     elif element == 6:
#         prompt = 'Determine if '+req1+' and '+req2+' can be considered as the same input'

#     prompt = prompt+prompt_addition
#     index = 0
#     while index < 3:
#         response = openai.Completion.create(
#             prompt=prompt,
#             model=model,
#             max_tokens=5,
#             temperature = 0.9,
#             n=1,
#             stop=['---']
#         )
#         textVal = ''
#         for result in response.choices:
#             textVal = result.text

#         gptOutput = textVal.split('\n')
#         print(gptOutput)
#         if 'True' in gptOutput:
#             return True
#         index+=1
#     return False


def get_NFR_type(req):
    prompt = "You are working on a software development project, and you need to identify the type of Non-Functional Requirement (NFR) mentioned in the requirment text "+req+ " from the list of types that includes: (Performance, Reliability, Usability, Security, Maintainability, Portability, Scalability, Availability, Interperability, Compliance, Efficiency, Data Integrity, Safety, Legal, Capacity)"
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=15,
        temperature = 0.1,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    return gptOutput

def get_NFR_task(req):
    prompt = 'Divide the elements (Goal, Metrics, Scope, Constraints) from this requirement text: ' + req + '. Assume only if element cannot be directly gathered from text.'
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=80,
        temperature = 0.1,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    return gptOutput


def resolveConflicts(req1, req2):
    with open('dataset/user_story.txt', 'r') as file:
        user_story = file.read()

    prompt = "Resolve the conflicts in the requirements ‘"+req1+"’ and ‘"+req2+"’ in a way that serves the user_story which states ‘"+user_story+"’ by creating a single requirement statement as output." 

    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=50,
        temperature = 0.2,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    return gptOutput
    




