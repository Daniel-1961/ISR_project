import os
import requests
from tqdm import tqdm

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


# Example Usage:
if __name__ == "__main__":
    # List of Project Gutenberg ebook IDs
    ebook_ids = [
        1342, 84, 2701, 11, 98, 345, 1661, 5200, 4300, 1080,
        1184, 74, 2542, 408, 174, 16328, 215, 1400, 28054, 23
    ]

    downloader = GutenbergDownloader(ebook_ids)
    downloader.download_all_books()
