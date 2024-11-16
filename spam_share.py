import os
import requests
import threading
from queue import Queue

class ShareManager:
    def __init__(self, tokens, link, total_shares):
        self.tokens = tokens
        self.link = link
        self.total_shares = total_shares
        self.success_count = 0
        self.lock = threading.Lock()
        self.queue = Queue()

    def share_post(self, token):
        """Shares a post on the user's feed with 'Only Me' privacy."""
        url = f"https://graph.facebook.com/v13.0/me/feed"
        payload = {
            'link': self.link,
            'published': '0',
            'privacy': '{"value":"SELF"}',
            'access_token': token
        }

        try:
            response = requests.post(url, data=payload).json()
            if 'id' in response:
                with self.lock:
                    self.success_count += 1
                    print(f"✅ Post shared successfully. Total: {self.success_count}/{self.total_shares}")
            else:
                print(f"❌ Failed to share post: {response}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Network error: {e}")

    def worker(self):
        """Thread worker function to process tokens from the queue."""
        while not self.queue.empty():
            token = self.queue.get()
            if self.success_count >= self.total_shares:
                break
            self.share_post(token)
            self.queue.task_done()

    def start_sharing(self):
        """Starts the sharing process with threads."""
        for token in self.tokens:
            self.queue.put(token)

        threads = []
        for _ in range(min(10, len(self.tokens))):  # Limit to 10 concurrent threads
            thread = threading.Thread(target=self.worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print(f"\n🚀 Completed {self.success_count}/{self.total_shares} successful shares.")

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        print("❌ No valid tokens found. Exiting...")
        return

    link = input("Enter the post link to share: ").strip()
    try:
        total_shares = int(input("Enter the total number of shares: ").strip())
        if total_shares <= 0:
            print("❌ Share count must be greater than 0.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    manager = ShareManager(tokens, link, total_shares)
    manager.start_sharing()

if __name__ == "__main__":
    main()
