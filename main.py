# from models.knn_svm_classifier import getAccuracy
# from models.dataLoader import tokenizeData
from gpt3 import getGPT3_Result
from nn_runner import run_nn_model
import pandas as pd
import re
import sys


if __name__ == "__main__":
    fileLoc = sys.argv[1]
    # load CSV file as a dataframe
    pd.set_option('display.max_colwidth', 1000)
    df = pd.read_csv('dataset/requirement_guide.csv')

    # getAccuracy('KNN')
    # getAccuracy('SVM')
    
    gptOutput = getGPT3_Result(fileLoc)

    for outs in gptOutput:
        if outs != '':
            reqList = []
            outs = re.sub(r"^\d+\.", "", outs)

            with open('results/requirement_report.txt', 'r') as f:
                for line in f:
                    reqList.append(line.strip())
                
            with open('results/requirement_report.txt', 'a') as f:
                # Write some text to the file
                if outs not in reqList:
                    f.write(outs)
                    f.write('\n')

            response_list = run_nn_model(outs)

            if response_list != ['']:
                for x in response_list:
                    reqs = df['data'][df['name'] == x]
                    # reqs = reqs.to_string(index=False)
                    # Open the file in write mode
                    with open('results/requirement_report.txt', 'a') as f:
                        # Write some text to the file
                        for y in reqs:
                            if y not in reqList:
                                f.write(y)
                                f.write('\n')
    

            


    print('End')
import rnn_classifier_runner