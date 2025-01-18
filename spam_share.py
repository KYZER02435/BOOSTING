import os
import requests
import time
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor

def share_post(token, link):
    """Shares a post on the user's feed with 'Only Me' privacy."""
    url = "https://graph.facebook.com/v13.0/me/feed"
    payload = {
        'link': link,
        'published': '0',  
        'privacy': '{"value":"SELF"}',  
        'access_token': token
    }

    try:
        response = requests.post(url, data=payload).json()
        if 'id' in response:
            return response['id']
        return None  # Return None if the request failed
    except requests.exceptions.RequestException:
        return None  # Ignore network errors

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(tokens, link, token_index, share_number):
    """Worker function for sharing posts."""
    while True:
        token = tokens[token_index % len(tokens)]  # Cycle through tokens
        post_id = share_post(token, link)
        if post_id:
            print(f"✅ Successfully Shared: {token[:8]}_{post_id} : {share_number}")  # Fixed share count
            return  # Stop only if the post was successfully shared
        token_index += 1  # Move to the next token if the current one fails

def fast_share(tokens, link, share_count):
    """Executes the sharing process using multiple threads."""
    start_time = time.time()
    print("🚀 Starting sharing process...")  

    with ThreadPoolExecutor(max_workers=min(len(tokens), 70)) as executor:
        futures = []
        share_number = 1  # Start share count from 1

        while share_number <= share_count:
            future = executor.submit(worker, tokens, link, share_number - 1, share_number)
            futures.append(future)
            share_number += 1  # Increment count only when a share task is created

        # Ensure all tasks complete
        for future in futures:
            future.result()

    elapsed_time = time.time() - start_time
    avg_time_per_share = elapsed_time / share_count if share_count > 0 else 0

    total_time = timedelta(seconds=int(elapsed_time))
    avg_time = timedelta(seconds=int(avg_time_per_share))

    print(f"\n🚀 Target: {link}")
    print(f"⏳ Total Time: {total_time}")
    print(f"⏱️ Average Time per Share: {avg_time}")

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        print("❌ No valid tokens found. Exiting...")
        return

    link = input("Enter the post link to share: ").strip()
    print(f"\n✅ Link Confirmed: {link}")

    try:
        total_shares = int(input("Enter the total number of shares: ").strip())
        if total_shares <= 0:
            print("❌ Total shares must be greater than 0.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    fast_share(tokens, link, total_shares)

if __name__ == "__main__":
    main()
