import openai

# Edit API_KEY by adding your personal key here
def getGPT3_Result(filename):
    API_KEY = ""
    openai.api_key = API_KEY
    model = 'text-davinci-003'
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

