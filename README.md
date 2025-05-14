# Zipf's Law Text Analysis Project

This project explores and validates **Zipf's Law** using a collection of text files sourced from **Project Gutenberg**. Zipf's Law predicts an inverse relationship between a word's frequency and its rank in a corpus.

## Project Summary

- Texts from Project Gutenberg were **downloaded, cleaned, preprocessed, tokenized and stop words are removed**.
- Word frequencies were computed and **ranked**.
- A **plot of Frequency vs. Rank** was created to visually validate Zipf’s Law.
- The resulting graph demonstrates the expected distribution.

##  Visualization

- The plot confirming Zipf’s Law is located in the **`notebook_visualization.ipynb`** folder.
- Check the notebook for step-by-step insights and the final graph.

##  Project Files

- `Text_processing.py`: Contains the **entire codebase** — from text preprocessing to frequency analysis and ranking.
- `notebook_visualiazation`: Includes the **Zipf’s Law visualization notebook**.
- `cleaned_books/`, `tokenized_books/`,`gutenberg_books/`,`frequencies/`: Processed text files.
- `word_frequencies.csv`: Ranked word frequency data from the entire collection used for visualization.

##  Methodology Steps

1. Download texts from Project Gutenberg.   Data in *gutenberg_books/*
2. Clean and preprocess text (punctuation, casing, noise removal). Data in *cleaned_books/*
3. Tokenize text into words. Data in *tokenized_books/*
4. Count word frequencies using `collections.Counter`.  Data in *frequencies/*
5. Rank tokens by frequency. Generated .csv file for words from entire collection
6. Plot Frequency vs. Rank using `matplotlib` and `numpy`.

##  Results

The frequency-rank graph aligns with **Zipf's Law**, validating the hypothesis on real-world text data.

---

