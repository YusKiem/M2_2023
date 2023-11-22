# %%
import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from stemming.porter2 import stem 
from collections import defaultdict
import pickle

# %%
# Preprocessing
pattern = r'TEXT: (.+)'
with open('collections/sample.txt', 'r') as file:
    x = file.read()
    documents = re.findall(pattern, x)


# print(documents)

tokenization = RegexpTokenizer(r"\w+")
new = []

with open('stopWords.txt', 'r') as file:
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


# %%
# Concatenate tokens
# final=[]
# for i in new:
#     final.append(' '.join(i))
# print(final)
final = [' '.join(i) for i in new] 
final

# %%
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

# %%
pos_index = positional_inverted_index(final)
with open('sampleindex.txt', 'w') as file:
    for term, info in pos_index.items():
        file.write(term + ":\n")
        for doc_id, positions in info['documents'].items():
            file.write(f"\t{doc_id}:\t{', '.join(map(str, positions))}\n")

print("Term\tDocument ID\tPositions")
for term, info in pos_index.items():
    print(term + ":")
    for doc_id, positions in info['documents'].items():
        print(f"\t{doc_id+1}: {', '.join(map(str, positions))}")

# %%
pos_index

# %%
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
inv_index

# %%
def and_postings(posting1, posting2):
    return sorted(set(posting1).intersection(posting2))


# %%
def or_postings(posting1, posting2):
    return sorted(set(posting1).union(posting2))

# %%
def NOT(posting, total_docs):
    return sorted(set(range(total_docs)) - set(posting))

# %%
# Boolean Search
def boolean_search(query, index):
    query = query.split()
    result = set(index[query[0]].keys())
    for term in query[1:]:
        result &= set(index[term].keys())
    return result

query = "he AND NOT ice"
result = boolean_search(query, inv_index)
print(result)

# %%
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

# Example usage:
total_docs = len(final)
query = input('Enter your query - ')
result = process_query(query, inv_index, total_docs)
print(result)


# %%
# Save Index
with open('index.pkl', 'wb') as f:
    pickle.dump(pos_index, f)



# %%
# Load Index
with open('index.pkl', 'rb') as f:
    index_loaded = pickle.load(f)
# print(index_loaded)

# %%
def process_query(query):
    query_terms = query.split()
    i = 0
    total_docs = len(documents)
    
    while i < len(query_terms):
        term = query_terms[i]

        if term == 'AND':
            result = and_postings(inv_index[query_terms[i-1]], inv_index[query_terms[i+1]], total_docs)
        elif term == 'OR':
            result = or_postings(inv_index[query_terms[i-1]], inv_index[query_terms[i+1]], total_docs)
        elif term == 'NOT':
            result = NOT(inv_index[query_terms[i+1]], total_docs)
        elif i == 0:
            try:
                result = inv_index[term]
            except KeyError:
                result = set()
        i += 2  # Move to the next query term

    return result

query = input('Enter your query - ')
print(process_query(query))


# %%


# %%


# %%
def phrase_search(query, pos_index):
    query_terms = query.split()
    postings = pos_index[query_terms[0]]['documents']
    for term in query_terms[1:]:
        term_postings = pos_index[term]['documents']
        for doc in postings.keys():
            if doc in term_postings:
                postings[doc] = [pos for pos in postings[doc] if pos + 1 in term_postings[doc]]
            else:
                postings.pop(doc)
    return postings

# %%


# %%
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

# %%
pos_index

# %%
   query = "he ink and"
   result = phrase_search(query, pos_index)
   print(result)

# %%


# %%
def proximity_search(query, k, pos_index):
    query_terms = query.split()
    postings = pos_index[query_terms[0]]['documents']
    for term in query_terms[1:]:
        term_postings = pos_index[term]['documents']
        for doc in postings.keys():
            if doc in term_postings:
                postings[doc] = [pos for pos in postings[doc] if any(abs(pos - other_pos) <= k for other_pos in term_postings[doc])]
            else:
                postings.pop(doc)
    return postings

# %%


# %%
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

# %%
   query = "he ink and"
   k = 5  # Set the proximity threshold
   result = proximity_search(query, k, pos_index)
   print(result)

# %% [markdown]
# 5. Large index: If the index is very large, it would be best to save the index in a database or use an indexing service like Elasticsearch. To load the index into memory, you can load it in chunks or use a memory-mapped file.

# %% [markdown]
# 6. Large number of documents: If the number of documents is very large, you can use delta encoding to save document numbers. Delta encoding saves the difference between two consecutive numbers instead of the numbers themselves, which can save a lot of space when the numbers are close together.


