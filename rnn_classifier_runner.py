import torch
import random
import spacy
import torchtext
import torchtext.legacy.data as data

from sklearn.metrics import precision_recall_fscore_support
RANDOM_SEED = 123
torch.manual_seed(RANDOM_SEED)
nlp = spacy.load('en_core_web_sm')
vocab_size = 558
LEARNING_RATE = 0.005
BATCH_SIZE = 128
NUM_EPOCHS = 250
DEVICE = torch.device('cpu')

EMBEDDING_DIM = 128
HIDDEN_DIM = 256
NUM_CLASSES = 2


def reconvertData():
    TEXT = torchtext.legacy.data.Field(
        tokenize='spacy',
        tokenizer_language='en_core_web_sm'
    )

    LABEL = torchtext.legacy.data.LabelField(dtype=torch.long)
    fields = [('Text', TEXT), ('Category', LABEL)] 

    trainset = torchtext.legacy.data.TabularDataset(
        path='models/df1.csv',format='csv',
        skip_header=True,fields=fields
    )

    test_data = torchtext.legacy.data.TabularDataset(
        path='models/df2.csv',format='csv',
        skip_header=True,fields=fields
    )

    train_data, valid_data = trainset.split(
        split_ratio=[0.85,0.15],
        random_state=random.seed(RANDOM_SEED)

    )

    TEXT.build_vocab(train_data,max_size=vocab_size)
    LABEL.build_vocab(train_data)

    train_loader, valid_loader, test_loader = \
        torchtext.legacy.data.BucketIterator.splits(
            (train_data,valid_data,test_data),
            batch_size = BATCH_SIZE,
            sort_within_batch = False,
            sort_key=lambda x: len(x.Text),
            device = DEVICE
        )
    
    return train_loader, valid_loader, test_loader, TEXT, LABEL


train_loader, valid_loader, test_loader, TEXT, LABEL = reconvertData()

# Define the RNN model class
class RNN(torch.nn.Module):
    def __init__(self, input_dim, embedding_dim, hidden_dim, output_dim):
        super().__init__()

        self.embedding = torch.nn.Embedding(input_dim,embedding_dim)
        self.rnn = torch.nn.LSTM(embedding_dim, hidden_dim)
        self.fc = torch.nn.Linear(hidden_dim, output_dim)
    
    def forward(self, text):
        embedded = self.embedding(text)
        output, (hidden, cell) = self.rnn(embedded)
        hidden.squeeze_(0)
        output = self.fc(hidden)
        return output

# Create a new instance of the RNN class
loaded_model = RNN(input_dim=len(TEXT.vocab),
                   embedding_dim=EMBEDDING_DIM,
                   hidden_dim=HIDDEN_DIM,
                   output_dim=NUM_CLASSES)

# Load the saved state dictionary
loaded_model.load_state_dict(torch.load('saved_models/classifierRNN.pt'))

# Put the model in evaluation mode
loaded_model.eval()

textArray = []
with open('results/requirement_report.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    textArray.append(line.strip())

with open('results/final_report.txt', 'a') as f3:
    # Write new lines to the file

    # # Preprocess the text using the TEXT field
    for x in textArray:
        preprocessed_text = [tok.text for tok in nlp.tokenizer(x)]
        preprocessed_text = [TEXT.vocab.stoi[word] for word in preprocessed_text]
        tensor_text = torch.LongTensor(preprocessed_text).to(DEVICE)

        # Pass the preprocessed text through the loaded model
        with torch.no_grad():
            output = loaded_model(tensor_text.unsqueeze(1))
            _, predicted = torch.max(output, 1)
        
        # Print the predicted label
        out_line = ''
        if predicted.item() == 0:
            out_line = 'NF: '+x 
        else:
            out_line = 'F: '+x 
        f3.write(out_line)
        f3.write('\n')





