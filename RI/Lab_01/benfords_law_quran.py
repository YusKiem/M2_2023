import collections
import matplotlib.pyplot as plt
import numpy as np

def plot_benfords_law(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()

    # Count the frequency of each word
    word_counts = collections.Counter(words)

    # Get the first digit of each frequency
    first_digits = [int(str(count)[0]) for count in word_counts.values() if count >= 10]

    # Count the frequency of each first digit
    digit_counts = collections.Counter(first_digits)

    # Plot the distribution of the first digits
    digits, frequencies = zip(*sorted(digit_counts.items()))
    plt.bar(digits, frequencies)
    plt.xlabel('First Digit')
    plt.ylabel('Frequency')
    plt.show()

# Plot Benford's law for each collection
plot_benfords_law('quran.txt')