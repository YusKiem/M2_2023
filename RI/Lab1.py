import string
import re
import fileinput
# print(string.punctuation)
def tokenizing_func(input_file, output_file, lower_cased):
    # Read the content of the file to be preprocessed 
    with open(input_file, 'r') as file1:
        content1 = file1.read()

    for char in content1:
        if char in string.punctuation:
            content1 = content1.replace(char, '')

    with open(output_file, 'w') as file2:
        file2.write(content1)    

    with open(output_file, 'r') as file:
        to_lower= file.read()

    with open(lower_cased, 'w') as file:
        file.write(to_lower.lower())

# Specify input and output file paths
input_file_path = 'quran_original_copy.txt'  # Change to your input file path
output_file_path = "tokenized_text.txt"  # Change to your output file path
lower_cased_filepath="lower_cased_text.txt"

# Remove punctuation from the input file and save to the output file
tokenizing_func(input_file_path, output_file_path,lower_cased_filepath)
print("Punctuation removed from the file and saved to:", output_file_path)

def remove_stop_words(file1_path, file2_path, no_stopwords):
    # Read the content of the first file
    with open(file1_path, 'r') as file1:
        content1 = file1.read()
    # Read the content of the second file
    with open(file2_path, 'r') as file2:
        content2 = file2.read()
    
    # Split the content into lists of words
    words1 = content1.split()
    words2 = content2.split()

    # Find words in words1 that are not in words2 while maintaining the order
    unique_words = [word for word in words1 if word not in words2]

    # Write the unique words(not in stopwords list) to the output file
    with open(no_stopwords, 'w') as file:
        file.write("\n".join(unique_words))

stopwords_file_path = 'stopWords.txt'  # Replace with the actual path of the second file
removed_stopwords="text_without_stopwords.txt"
# Compare the content of the specified files
remove_stop_words(lower_cased_filepath, stopwords_file_path,removed_stopwords)


# for line in fileinput.input(removed_stopwords, inplace=True):
#     print(re.sub("\d+", "", line))

# Specify the file path to stem
file_path_stem = 'stem_text_without_stopwords.txt'

# Specify the output file path to unique stem words
file_path_stem_unique = 'unique_stemmed_words.txt'

with open(removed_stopwords, 'r') as file:
        content = file.read()

with open(file_path_stem, 'w') as file:
        file.write(content)

from stemming.porter2 import stem
def stem_words(without_stpwrds, file_path_stem, file_path_stem_unique ):
    # Read the content of the file
    with open(without_stpwrds, 'r') as file:
        content = file.read()

    words = content.split()

    # Stem each word
    stemmed_words = [stem(word) for word in words]

    # Join the stemmed words back into a string
    stemmed_content = '\n'.join(stemmed_words)

    # Write the stemmed content back to the file
    with open(file_path_stem, 'w') as file:
        file.write(stemmed_content)

     # Remove duplicates by converting the list to a set, then convert it back to a list
    unique_stemmed_words = list(dict.fromkeys(stemmed_words))

     # Join the stemmed words back into a string
    unique_stemmed_content = '\n'.join(unique_stemmed_words)

    # Write the unique stemmed content back to the file
    with open(file_path_stem_unique, 'w') as file:
        file.write(unique_stemmed_content)

# Stem the words in the specified file
stem_words(removed_stopwords,file_path_stem, file_path_stem_unique)