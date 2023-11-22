import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from collections import Counter
from matplotlib import pyplot as plt


pattern = r'TEXT: (.+)'
with open('Lab_02/collections/sample.txt', 'r') as file:
    txt = file.read()
    documents = re.findall(pattern, txt)

print(documents)

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from stemming.porter2 import stem 

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
# print(new)
for list in new:
    print(list)

# Concatenate tokens
final=[]
for i in new:
    final.append(' '.join(i))
print(final)  

def positional_inverted_index(documents):
    index = {}
    for doc_id, doc in enumerate(documents):
        for pos, word in enumerate(doc.split()):
            if word not in index:
                index[word] = {}
            if doc_id not in index[word]:
                index[word][doc_id] = []
            index[word][doc_id].append(pos)
    return index

pos_index = positional_inverted_index(final)
print(pos_index)

def inverted_index(documents):
    index = {}
    for doc_id, doc in enumerate(documents):
        for word in doc.split():
            if word not in index:
                index[word] = []
            if doc_id not in index[word]:
                index[word].append(doc_id)
    return index

inv_index = inverted_index(final)
print(inv_index)


# ... (import statements and preprocessing code)

def inverted_index(documents):
    index = {}
    for doc_id, doc in enumerate(documents):
        for word in doc.split():
            if word not in index:
                index[word] = []
            if doc_id not in index[word]:
                index[word].append(doc_id)
    return index

def positional_index(documents):
    index = {}
    for doc_id, doc in enumerate(documents):
        for pos, word in enumerate(doc.split()):
            if word not in index:
                index[word] = []
            index[word].append((doc_id, pos))
    return index

inv_index = inverted_index(final)
pos_index = positional_index(final)


import pickle

# Save index to a file
def save_index(index, filename):
    with open(filename, 'wb') as f:
        pickle.dump(index, f)

# Load index from a file
def load_index(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Boolean search
def boolean_search(query, index):
    query = query.split()
    if query[0] not in index:
        return set()
    result = set(index[query[0]])
    for term in query[1:]:
        if term not in index:
            continue
        if term == 'AND':
            result &= set(index[query[query.index(term) + 1]])
        elif term == 'OR':
            result |= set(index[query[query.index(term) + 1]])
        elif term == 'NOT':
            result -= set(index[query[query.index(term) + 1]])
    return result

# Phrase search
def phrase_search(query, index):
    query = query.split()
    if query[0] not in index:
        return set()
    result = set(index[query[0]])
    for term in query[1:]:
        if term not in index:
            continue
        result &= set(index[term])
    return result

# Proximity search
def proximity_search(query, index, k):
    query = query.split()
    if query[0] not in index:
        return set()
    result = set(index[query[0]])
    for term in query[1:]:
        if term not in index:
            continue
        result &= set([doc for doc in index[term] if abs(index[query[0]].index(doc) - index[term].index(doc)) <= k])
    return result


# Save the index
save_index(inv_index, 'inverted_index.pkl')
save_index(pos_index, 'positional_index.pkl')

# Load the index
inv_index = load_index('inverted_index.pkl')
pos_index = load_index('positional_index.pkl')

# Run searches
print(boolean_search('drink AND ink', inv_index))
print(phrase_search('thinks he', inv_index))
print(proximity_search('water ink', pos_index, 5))