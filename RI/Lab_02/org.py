import re
from nltk.tokenize import RegexpTokenizer
from stemming.porter2 import stem
import pickle

# Preprocessing
pattern = r'TEXT: (.+)'
with open('collections/sample.txt', 'r') as file:
    x = file.read()
    documents = re.findall(pattern, x)

tokenization = RegexpTokenizer(r"\w+")
new = []

with open('stopWords.txt', 'r') as file:
    stopWords = file.read().split()

def preprocess(stp, stm, documents):
    for doc in documents:
        tokenized = tokenization.tokenize(doc)
        lower = [word.lower() for word in tokenized]

        if stp:
            lower = [word for word in lower if not word in stopWords]
        
        if stm:
            lower = [stem(word) for word in lower]
        
        new.append(lower)

preprocess(False, False, documents)

def and_postings(posting1, posting2):
    return sorted(set(posting1).intersection(posting2))

def or_postings(posting1, posting2):
    return sorted(set(posting1).union(posting2))

def NOT(posting, total_docs):
    return sorted(set(range(total_docs)) - set(posting))

def boolean_search(query, index):
    query = query.split()
    result = set(index[query[0]].keys())
    for term in query[1:]:
        result &= set(index[term].keys())
    return result

def process_query(query, inv_index, total_docs):
    query_terms = query.split()
    result = None

    for i, term in enumerate(query_terms):
        if term == "AND" or term == "OR":
            if query_terms[i+1] == "NOT":
                operand = NOT(inv_index[query_terms[i+2]], total_docs)
            else:
                operand = inv_index[query_terms[i+1]]

            if term == "AND":
                result = and_postings(result, operand)
            elif term == "OR":
                result = or_postings(result, operand)

        elif term == "NOT" and i == 0:
            result = NOT(inv_index[query_terms[i+1]], total_docs)
        elif i == 0:
            try:
                result = inv_index[term]
            except KeyError:
                result = set()

    return result

def positional_inverted_index(documents):
    index = {}
    for doc_id, doc in enumerate(documents):
        for pos, word in enumerate(doc.split()):
            if word not in index:
                index[word] = {
                    'document_frequency': 0,
                    'documents': {},
                }
            if doc_id not in index[word]['documents']:
                index[word]['documents'][doc_id] = []
                index[word]['document_frequency'] += 1
            index[word]['documents'][doc_id].append(pos)
    return index

pos_index = positional_inverted_index(new)

def save_index(index, filename):
    with open(filename, 'wb') as f:
        pickle.dump(index, f)

def load_index(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

final = [' '.join(i) for i in new] 
final

# Example usage:
total_docs = len(final)
query = input('Enter your query - ')
result = process_query(query, pos_index, total_docs)
print(result)


def phrase_search(query, pos_index):
    query_terms = query.split()
    result = pos_index[query_terms[0]]['documents'].copy()  # Create a copy of the initial postings
    for term in query_terms[1:]:
        term_postings = pos_index[term]['documents']
        updated_postings = {}
        for doc in result.keys():
            if doc in term_postings:
                updated_postings[doc] = [pos for pos in result[doc] if pos + 1 in term_postings[doc]]
        result = updated_postings  # Update the result with the new postings
    return result

pos_index

query = "he ink and"
result = phrase_search(query, pos_index)
print(result)

def proximity_search(query, k, pos_index):
    query_terms = query.split()
    result = pos_index[query_terms[0]]['documents'].copy()  # Create a copy of the initial postings
    for term in query_terms[1:]:
        term_postings = pos_index[term]['documents']
        updated_postings = {}
        for doc in result.keys():
            if doc in term_postings:
                updated_postings[doc] = [pos for pos in result[doc] if any(abs(pos - other_pos) <= k for other_pos in term_postings[doc])]
        result = updated_postings  # Update the result with the new postings
    return result

query = "he ink and"
k = 5  # Set the proximity threshold
result = proximity_search(query, k, pos_index)
print(result)