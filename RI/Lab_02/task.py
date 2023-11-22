import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
import pickle

# Preprocessing
pattern = r'TEXT: (.+)'
with open('Lab_02/collections/sample.txt', 'r') as file:
    txt = file.read()
    documents = re.findall(pattern, txt)

tokenization = RegexpTokenizer(r"\w+")
new = []

with open('Lab_02/stopWords.txt', 'r') as file:
    stopWords = file.read().split()

def preprocess(stp, stm, documents):
    for doc in documents:
        # Tokenization
        tokenized = tokenization.tokenize(doc)
        
        # Casefolding
        lower = [word.lower() for word in tokenized]
        
        if stp:
            # Stopwords removal
            lower = [word for word in lower if not word in stopWords]
        
        if stm:
            # Stemming using the stemming library
            lower = [stem(word) for word in lower]
        
        new.append(lower)

preprocess(False, False, documents)


def default_factory():
    return defaultdict(list)

def positional_inverted_index(documents):
    index = {} 
    for doc_id, doc in enumerate(documents):
        for pos, term in enumerate(doc):
            index[term][doc_id].append(pos)
    return index

index = positional_inverted_index(new)

# Boolean Search
def boolean_search(query, index):
    query = query.split()
    result = set(index[query[0]].keys())
    for term in query[1:]:
        result &= set(index[term].keys())
    return result

# Phrase Search
def phrase_search(query, index):
    query = query.split()
    possible_docs = set(index[query[0]].keys())
    for term in query[1:]:
        possible_docs &= set(index[term].keys())
    
    result = []
    for doc_id in possible_docs:
        # Check if terms appear consecutively in document
        positions = [index[term][doc_id] for term in query]
        for pos in positions[0]:
            if all((pos + i) in positions[i] for i in range(1, len(query))):
                result.append(doc_id)
                break
    return result

# Save Index
with open('index.pkl', 'wb') as f:
    pickle.dump(index, f)

# Load Index
with open('index.pkl', 'rb') as f:
    index_loaded = pickle.load(f)
print(index_loaded)
