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
    prompt = 'Divide the elements (Operation, Input, Output, Actor, Actor-Type, Event, Pre-Condition, Post-Condition, Any number value with units(example: seconds, pages, km, etc.) ) from this requirement text: ' + requiement + '. Assume only if element cannot be directly gathered from text.'

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

def determineNoneValue(req, element):
    op = req['operation']
    data_in = req['input']
    data_out = req['output']
    actor = req['actor']
    if op is None:
        op = 'N/A'
    elif data_in is None:
        data_in = 'N/A'
    elif data_out is None:
        data_out = 'N/A'
    elif actor is None:
        actor = 'N/A'
    if element == 2:
        prompt = "Given an operation "+ op + " , the input data " + data_in + " and the output data "+ data_out + ". Determine the actor that will be using that operation. If none found return the word None as default."
    elif element == 3:
        prompt = "Given an operation "+ op + " , the input data " + data_in + " and the actor "+ actor + ". Determine the event that initiates the operation. If none found return the word None as default."
    elif element == 4:
        prompt = "Given an operation "+ op + " , the actor " + actor + " and the output data "+ data_out + ". Determine possible input for the operation. If none found return the word Data as default."
    elif element == 5:
        prompt = "Given an operation "+ op + " , the actor " + actor + " and the input data "+ data_in + ". Determine possible output for the operation. If none found return the word Data as default."
    elif element == 6:
        prompt = "Given an operation "+ op + " , the input data " + data_in + " and the actor "+ actor + ". Determine the pre-condition for the operation. If none found return the word None as default."
    elif element == 7:
        prompt = "Given an operation "+ op + " , the output data " + data_out + " and the actor "+ actor + ". Determine the post-condition for the operation. If none found return the word None as default."

    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=15,
        temperature = 0.3,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    return gptOutput[2]


def get_NFR_type(req):
    prompt = "You are working on a software development project, and you need to identify the type of Non-Functional Requirement (NFR) mentioned in the requirment text "+req+ " from the list of types that includes: (Performance, Reliability, Usability, Security, Maintainability, Portability, Scalability, Availability, Efficiency, Data Integrity, Legal, Capacity)"
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

def getReasonNumber(reason):
    if reason.startswith('Reason:'):
        reason = reason[7:]
        reason = reason.strip() 
    if reason ==  'The operations are same but the events are different.':
        return 1
    elif reason == 'Same actor and operation generates different output':
        return 2
    elif reason == 'The operations are same but the actors are different.':
        return 3
    elif reason == 'The operations are different but the post-conditions are same.':
        return 4
    elif reason == 'The operations are different but generates the same output.':
        return 5
    elif reason == 'The operations are different but both pre-condtions and inputs are same.':
        return 6
    elif reason == 'The operations are different but both actors and inputs are same.':
        return 7
    elif reason == 'The operations are different but both pre-condtions and events are same.':
        return 8
    elif reason == 'The operations are different but both actors and events are same.':
        return 9
    
    return 0
    
def get_user_story():
    file_path = 'dataset/user_story.txt'
    with open(file_path, 'r') as file:
        for l in file:
            return l

def get_system_type():
    user_story = get_user_story()
    prompt = "Determine the system type from the given statement: "+ user_story + " from the list (automated system , educational system, ecommerce, social, transaction, streaming, file storage and web based system)" 
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=20,
        temperature = 0.1,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text
    gptOutput = textVal.split('\n')
    gptOutput = gptOutput[2]
    return gptOutput


def resolveConflicts(conflicts, loop):
    req1 = conflicts[0]
    req2 = conflicts[1]
    reason = conflicts[2]
    prompt = 'Given the two conflicting requirements '+ req1 + ' and ' + req2+'.' 
    system_type = get_system_type()
    reason_no = getReasonNumber(reason)
    temp = 0.5
    token = 100

    if loop == 0:
        if reason_no == 1:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the event in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 2:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the output in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 3:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the actor in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 4:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the post-condition in a single sentence. Make sure the context of the initial requirement text does not change."
            # prompt += "Merge and return a single requirement statement that serves both operation."
        elif reason_no == 5:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the output in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 6:
            prompt += "Rewrite the first requirement, "+req1+ "specifically mentioning the pre-condition and input in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 7:
            prompt+= "Rewrite the first requirement, "+req1+ "specifically mentioning the actor and input in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 8:
            prompt+= "Rewrite the first requirement, "+req1+ "specifically mentioning the event and pre-condition in a single sentence. Make sure the context of the initial requirement text does not change."
        elif reason_no == 9:
            prompt+= "Rewrite the first requirement, "+req1+ "specifically mentioning the event and actor in a single sentence. Make sure the context of the initial requirement text does not change."
        else:
            prompt += "Return one requirement from them which best fits a "+ system_type 
            temp = 0.1
    else:
        token = 200
        if reason_no == 1:

            prompt+= "Merge the two requirements into a single requirement that can be initiated by a single event."
            
        elif reason_no == 4 or reason_no == 5:
            prompt+= "Merge the two requirements into a single requirement containing different operations and generating the same output and/or post-condition."
        elif reason_no == 3:
            token = 100
            prompt+= "Rewrite the first requirement, "+req1+ "specifically making sure the operation is suitable for the actor performing the operation."
        elif reason_no == 6:
            prompt+= "Merge the two requirements into a single requirement containing different operations that can be initiated with the same input and pre-conditions."
        elif reason_no == 7:
            prompt+= "Merge the two requirements into a single requirement containing different operations that can be initiated with the same input and actor."
        elif reason_no == 8:
            prompt+= "Merge the two requirements into a single requirement containing different operations that can be initiated by the same event and pre-conditions."
        elif reason_no == 9:
            prompt+= "Merge the two requirements into a single requirement containing different operations that can be initiated by the same event and actor."
        else:
            prompt += "Return one requirement from them which best fits a "+ system_type 
            temp = 0.1
        if reason_no != 3:
            reason_no = 0
    
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=token,
        temperature = temp,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    gptOutput = gptOutput[2]
    # print(req1)
    # print(req2)
    # print(gptOutput)
    if 'NF:' in conflicts[0]:
        gptOutput = 'NF:' + gptOutput.split('NF:', 1)[-1]
    elif 'F:' in conflicts[0]:
        gptOutput = 'F:' + gptOutput.split('F:', 1)[-1]
    else:
        print('Wrong Output')
    return gptOutput, reason_no



