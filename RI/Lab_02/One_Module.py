import string
import re
import fileinput
from stemming.porter2 import stem


input_file_path = 'collections/sample.txt'
content = open(input_file_path, 'r').read()
print(content)
output_file_path = 'preprocessed.txt'
stopwords_file_path = 'stopWords.txt'
new = []

def preprocessing(content, output_file_path, stopwords_file_path, tokenization, normalization, remove_stopwords, stemming, number_removal):
    
    # content = open(input_file_path, 'r').read()

    if tokenization:
        # Remove Punctuations
        content = ''.join([char for char in content if char not in string.punctuation])
        print('tokenized')

    if normalization:
        # NORMALISATION(Case Folding)
        content = content.lower()
        print("lowered")

    if remove_stopwords:
        content_words = content.split()
        stopwords = open(stopwords_file_path, 'r').read().split()
        content_words = [word for word in content_words if word not in stopwords]
        content = " ".join(content_words)
        print("stoped")

    if number_removal:
        content = re.sub("\d+", "", content)
        print("numbers removed")

    if stemming:
        content_words = content.split()
        stemmed_words = [stem(word) for word in content_words]
        content = "\n".join(stemmed_words)
        # open(output_file_path, 'w').write(content)
        print("Stemmed")

        unique_stemmed_words = list(dict.fromkeys(stemmed_words))
        unique_content = "\n".join(unique_stemmed_words)
        open(output_file_path.replace(".txt", "_unique.txt"), 'a').write(unique_content)
        print("Unique stem")
    
    open(output_file_path, 'a').write(content)
    
    print("Preprocessing completed successfully!")

pattern = r'TEXT: (.+)'
with open('collections/sample.txt', 'r') as file:
    txt = file.read()
    documents = re.findall(pattern, txt)
    print(documents)





# def preprocess_documents(documents, output_file_path, stopwords_file_path):
#     with open(output_file_path, 'w') as output_file:  # Open the output file in write mode
#         for doc in documents:
#             preprocessed_doc = preprocessing(doc, output_file_path,stopwords_file_path, True, False, False, False, False)
#             output_file.write(preprocessed_doc + '\n')  # Write the preprocessed document to the output file

# preprocess_documents(documents, output_file_path, stopwords_file_path)
for doc in documents:    
    preprocessing(doc + '\n' , output_file_path, stopwords_file_path, False, True, True, True, False)

