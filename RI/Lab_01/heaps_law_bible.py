import collections
import matplotlib.pyplot as plt
import numpy as np


def plot_heaps_law(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()

    # Initialize the vocabulary and the lists to store the number of terms and the vocabulary size
    vocabulary = set()
    num_terms = []
    vocab_sizes = []

    # Go through the words one by one
    for i, word in enumerate(words):
        vocabulary.add(word)
        num_terms.append(i + 1)
        vocab_sizes.append(len(vocabulary))

    # Plot the growth of vocabulary
    plt.plot(num_terms, vocab_sizes)
    plt.xlabel('Number of Terms')
    plt.ylabel('Vocabulary Size')
    plt.show()

    # Fit Heap's law to the data and print the best fitting k and b
    log_num_terms = np.log(num_terms)
    log_vocab_sizes = np.log(vocab_sizes)
    b, log_k = np.polyfit(log_num_terms, log_vocab_sizes, 1)
    k = np.exp(log_k)
    print(f"Best fitting k: {k}, b: {b}")

# Plot Heap's law for each collection
plot_heaps_law('quran.txt')
plot_heaps_law('bible.txt')
plot_heaps_law('wikitext.txt')