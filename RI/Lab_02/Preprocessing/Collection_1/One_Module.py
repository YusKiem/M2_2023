import string
import re
import fileinput
from stemming.porter2 import stem


def preprocessing(input_file_path, output_file_path, stopwords_file_path, tokenization, normalization, remove_stopwords, stemming, number_removal):
    
    content = open(input_file_path, 'r').read()

    if tokenization:
        # Remove Punctuations
        content = ''.join([char for char in content if char not in string.punctuation])

    if normalization:
        # NORMALISATION(Case Folding)
        content = content.lower()

    if remove_stopwords:
        content_words = content.split()
        stopwords = open(stopwords_file_path, 'r').read().split()
        content_words = [word for word in content_words if word not in stopwords]
        content = " ".join(content_words)

    if number_removal:
        content = re.sub("\d+", "", content)

    if stemming:
        content_words = content.split()
        stemmed_words = [stem(word) for word in content_words]
        content = "\n".join(stemmed_words)
        open(output_file_path, 'w').write(content)

        unique_stemmed_words = list(dict.fromkeys(stemmed_words))
        unique_content = "\n".join(unique_stemmed_words)
        open(output_file_path.replace(".txt", "_unique.txt"), 'w').write(unique_content)

    print("Preprocessing completed successfully!")


input_file_path = 'Lab_02/collections/sample.txt'
output_file_path = 'Lab_02/preprocessed.txt'
stopwords_file_path = 'Lab_02/stopWords.txt'
preprocessing(input_file_path, output_file_path, stopwords_file_path, True, False, False, False, False)