# Zipf's Law Text Analysis Project

This project explores and validates **Zipf's Law** using a collection of text files sourced from **Project Gutenberg**. Zipf's Law predicts an inverse relationship between a word's frequency and its rank in a corpus.

## Project Summary

- Texts from Project Gutenberg were **downloaded, cleaned, preprocessed, and tokenized**.
- Word frequencies were computed and **ranked**.
- A **plot of Frequency vs. Rank** was created to visually validate Zipf’s Law.
- The resulting graph demonstrates the expected power-law distribution.

##  Visualization

- The plot confirming Zipf’s Law is located in the **`notebook_visualization.ipynb`** folder.
- Check the notebook for step-by-step insights and the final graph.

##  Project Files

- `Text_processing.txt`: Contains the **entire codebase** — from text preprocessing to frequency analysis and ranking.
- `notebooks`: Includes the **Zipf’s Law visualization notebook**.
- `cleaned_books/`, `tokenized_books/`: Processed text files.
- `word_frequencies.csv`: Ranked word frequency data used for visualization.

##  Methodology Steps

1. Download texts from Project Gutenberg.
2. Clean and preprocess text (punctuation, casing, noise removal).
3. Tokenize text into words.
4. Count word frequencies using `collections.Counter`.
5. Rank tokens by frequency.
6. Plot Frequency vs. Rank using `matplotlib` and `numpy`.

##  Results

The frequency-rank graph aligns with **Zipf's Law**, validating the hypothesis on real-world text data.

---

