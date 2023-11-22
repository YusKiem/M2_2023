import collections
import matplotlib.pyplot as plt
import numpy as np

def plot_zipfs_law(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()

    # Count the frequency of each word
    word_counts = collections.Counter(words)

    # Print the unique terms with their frequency
    for word, count in word_counts.items():
        print(f"{word}: {count}")

    # Sort the words by their frequency
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Plot the frequencies in a log-log graph
    frequencies = [count for word, count in sorted_word_counts]
    ranks = range(1, len(frequencies) + 1)
    plt.loglog(ranks, frequencies)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.show()

# Plot Zipf's law for each collection
plot_zipfs_law('quran.txt')