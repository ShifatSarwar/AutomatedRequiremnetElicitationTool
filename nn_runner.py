#!/usr/bin/env python
import torch
import json
from models.training.model import NeuralNet
from models.training.nltkutilities import tokenize, bag_of_words
#checking import
import nltk
nltk.download('punkt')


def run_nn_model(user_story):
    #Allows use of cuda or cpu for computing prediction
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = torch.device('cpu')
    
    #read from json data for getting responses based on asked questions
    with open('dataset/intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    #File contains model trained
    FILE = "saved_models/data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    #Gets model up and running
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    # with open('dataset/user_story.txt', 'r') as f:
    #     user_story = f.readline()

    # user_story = input("Enter your story: ")

    #convert command into a tokenized array
    command = tokenize(user_story)

    #get arrays to compare and predict
    X = bag_of_words(command, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted  = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    #runs if probability high
    if prob.item() > 0.65 :
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(tag)
                response_list = intent["responses"]
                return response_list
    else:
        tag = "unknown"
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(tag)
                response_list = intent["responses"]
                return response_list


    return ['']    
                    






