import openai
API_KEY = ""
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
    prompt = 'Identify the main Operation, Input, Output, Actor, Event, Pre-Condition, Post-Condition from this requirement text: ' + requiement 
    # prompt = 'Identify the key actions and behaviors from this text: '+ requiement

    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=100,
        temperature = 0.9,
        n=1,
        stop=['---']
    )

    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')

    return gptOutput

def checkSimilarity(req1, req2):
    if 'None' in req1 or 'None' in req2:
        return False
    if 'N/A' in req1 or 'N/A' in req2:
        return False
    if 'n/a' in req1 or 'n/a' in req2:
        return False
    if req1 == '' or req2 == '':
        return False
    
    prompt = 'Determine if' + req1 + 'means the same thing as' + req2 +'and only provide True or False as your output'
    
    response = openai.Completion.create(
        prompt=prompt,
        model=model,
        max_tokens=5,
        temperature = 0.9,
        n=1,
        stop=['---']
    )
    textVal = ''
    for result in response.choices:
        textVal = result.text

    gptOutput = textVal.split('\n')
    print(gptOutput)
    if 'True' in gptOutput or 'Yes' in gptOutput:
        return True
    return False

# requiement = "The system should allow users to create new accounts."
# print(divideElements(requiement))



