import os
import re
import string
import requests
from tqdm import tqdm
import nltk
#nltk.download('punkt')
from nltk.tokenize import RegexpTokenizer
from collections import Counter
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class GutenbergDownloader:
    def __init__(self, ebook_ids, save_dir="gutenberg_books"):
        self.ebook_ids = ebook_ids
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def get_book_url(self, ebook_id):
        """Return the standard plain-text URL for a Project Gutenberg book."""
        return f"https://www.gutenberg.org/files/{ebook_id}/{ebook_id}-0.txt"

    def download_book(self, ebook_id):
        """Download a single book and save it as a .txt file."""
        url = self.get_book_url(ebook_id)
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(self.save_dir, f"book_{ebook_id}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            return True
        else:
            print(f"⚠️ Failed to download book ID {ebook_id}")
            return False

    def download_all_books(self):
        """Download all books in the list."""
        print(f"📥 Starting download of {len(self.ebook_ids)} books...")
        for ebook_id in tqdm(self.ebook_ids, desc="Downloading books"):
            self.download_book(ebook_id)
    
    def clean_text(self, text):
    # Convert to lowercase
      text = text.lower()

    # Remove Project Gutenberg header/footer
      text = re.sub(r"\*\*\* start of(.*?)\*\*\*", "", text, flags=re.DOTALL | re.IGNORECASE)
      text = re.sub(r"\*\*\* end of(.*?)\*\*\*", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove punctuation and digits
      text = re.sub(rf"[{re.escape(string.punctuation)}]", " ", text)  # punctuation
      text = re.sub(r"\d+", " ", text)  # numbers

    # Remove special characters and multiple spaces
      text = re.sub(r"[^a-z\s]", " ", text)
      text = re.sub(r"\s+", " ", text).strip()

      return text
    
    def clean_all_books(self, cleaned_dir="cleaned_books"):
      os.makedirs(cleaned_dir, exist_ok=True)
      print("🧹 Cleaning all downloaded books...")

      for ebook_id in tqdm(self.ebook_ids, desc="Cleaning books"):
        original_path = os.path.join(self.save_dir, f"book_{ebook_id}.txt")
        cleaned_path = os.path.join(cleaned_dir, f"cleaned_{ebook_id}.txt")

        if os.path.exists(original_path):
            with open(original_path, "r", encoding="utf-8") as infile:
                raw_text = infile.read()
                cleaned_text = self.clean_text(raw_text)

            with open(cleaned_path, "w", encoding="utf-8") as outfile:
                outfile.write(cleaned_text)
        else:
            print(f"⚠️ Original file not found: {original_path}")

    def tokenize_text(self, text):
     """Split cleaned text into tokens (words)."""
     tokenizer = RegexpTokenizer(r'\w+')
     tokens = tokenizer.tokenize(text)
     return tokens
    
    def tokenize_all_books(self, cleaned_dir="cleaned_books", tokenized_dir="tokenized_books"):
      os.makedirs(tokenized_dir, exist_ok=True)
      print("🪄 Tokenizing all cleaned books...")

      for ebook_id in tqdm(self.ebook_ids, desc="Tokenizing books"):
        cleaned_path = os.path.join(cleaned_dir, f"cleaned_{ebook_id}.txt")
        tokenized_path = os.path.join(tokenized_dir, f"tokenized_{ebook_id}.txt")

        if os.path.exists(cleaned_path):
            with open(cleaned_path, "r", encoding="utf-8") as infile:
                cleaned_text = infile.read()
                tokens = self.tokenize_text(cleaned_text)

            with open(tokenized_path, "w", encoding="utf-8") as outfile:
                outfile.write(" ".join(tokens))
        else:
            print(f"⚠️ Cleaned file not found: {cleaned_path}")

    def calculate_word_frequencies(self, tokenized_dir="tokenized_books", freq_dir="frequencies"):
      os.makedirs(freq_dir, exist_ok=True)
      print("📊 Calculating word frequencies for all tokenized books...")

      for ebook_id in tqdm(self.ebook_ids, desc="Calculating frequencies"):
        tokenized_path = os.path.join(tokenized_dir, f"tokenized_{ebook_id}.txt")
        freq_path = os.path.join(freq_dir, f"freq_{ebook_id}.txt")

        if os.path.exists(tokenized_path):
            with open(tokenized_path, "r", encoding="utf-8") as infile:
                tokens = infile.read().split()

            # Count word frequencies
            word_freq = Counter(tokens)

            # Save frequencies
            with open(freq_path, "w", encoding="utf-8") as outfile:
                for word, freq in word_freq.most_common():
                    outfile.write(f"{word}\t{freq}\n")
        else:
            print(f"⚠️ Tokenized file not found: {tokenized_path}") 

    def calculate_word_frequencies_csv_file(self, tokenized_dir="tokenized_books", output_csv="word_frequencies.csv"):
        print("🧮 Calculating word frequencies across all tokenized books...")
        all_tokens = []

        # Read all tokenized files
        for ebook_id in tqdm(self.ebook_ids, desc="Reading tokenized books"):
            tokenized_path = os.path.join(tokenized_dir, f"tokenized_{ebook_id}.txt")

            if os.path.exists(tokenized_path):
                with open(tokenized_path, "r", encoding="utf-8") as infile:
                    tokens = infile.read().split()
                    all_tokens.extend(tokens)
            else:
                print(f"⚠️ Tokenized file not found: {tokenized_path}")

        # Count frequencies
        counter = Counter(all_tokens)

        # Sort by frequency (high to low)
        most_common = counter.most_common()

        # Add RANK
        ranked_words = [(rank + 1, word, freq) for rank, (word, freq) in enumerate(most_common)]

        # Save to CSV
        output_path = os.path.join(tokenized_dir, output_csv)
        os.makedirs(tokenized_dir, exist_ok=True)

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Rank", "Word", "Frequency"])
            writer.writerows(ranked_words)

        print(f"✅ Word frequencies saved successfully to {output_path}")
    


    def plot_zipfs_law(self):
    # Load your word frequencies
      df=pd.read_csv("word_frequencies.csv")

    # Extract rank and frequency
      ranks = df['Rank']
      frequencies = df['Frequency']

    # Plot
      plt.figure(figsize=(8, 4))
      plt.plot(ranks, frequencies, linestyle='-', color='blue')

      plt.xlabel('Rank')
      plt.ylabel('Frequency')
      plt.title('Word Frequency vs Rank (Zipf\'s Law)')
      plt.grid(True)
      plt.show()
      #Detail graph
      df_10=df[df['Rank']<100]
      df_20=df[df['Rank']<200]
      df_100=df[df['Rank']<500]
      fig, axes=plt.subplots(3,1, figsize=(8,10))
      fig.suptitle("Rank Vs Frequency Analysis", fontsize=16, fontweight='bold')
      fig.patch.set_edgecolor('black')  # Border color
      fig.patch.set_linewidth(3)
      axes[0].plot(df_10['Rank'],df_10['Frequency'], color='b',ls='-')
      axes[0].set_title("Zip's Law for Top 100 Words", fontweight='bold')
      axes[1].plot(df_20['Rank'],df_20['Frequency'], color='b',ls='-')
      axes[1].set_title("Zip's Law for Top 200 words",fontweight='bold')
      axes[2].plot(df_100['Rank'], df_100['Frequency'], color='b',ls='-')
      axes[2].set_title("Zip's Law for Top 500 words", fontweight='bold')
      for ax in axes:
          ax.set_xlabel("Rank")
          ax.set_ylabel("Frequency")
          ax.legend()
          ax.grid(True)
    
      
      plt.tight_layout()
      plt.show()

# Example Usage:
if __name__ == "__main__":
    # List of Project Gutenberg ebook IDs
    ebook_ids = [
        1342, 84, 2701, 11, 98, 345, 1661, 5200, 4300, 1080,
        1184, 74, 2542, 408, 174, 16328, 215, 1400, 28054, 23
    ]

    downloader = GutenbergDownloader(ebook_ids)
    #downloader.download_all_books()
    #downloader.clean_all_books()
    downloader.tokenize_all_books()
