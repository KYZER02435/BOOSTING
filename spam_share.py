import os
import requests
import time
from datetime import timedelta
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

# Color definitions
r = "[bold red]"
g = "[bold green]"
b = "[bold blue]"
y = "[bold yellow]"

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
        elif 'error' in response:
            error_msg = response['error'].get('message', 'Unknown error')
            if "Invalid OAuth access token" in error_msg or "Session expired" in error_msg:
                return None  # Skip banned/invalid tokens
    except requests.exceptions.RequestException:
        pass  # Ignore network errors

    return None  # Return None if failed

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print(f"{r}❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(token, link, success_queue):
    """Worker function for sharing posts."""
    post_id = share_post(token, link)
    if post_id:
        success_queue.put(f"{token[:8]}_{post_id}")

def fast_share(tokens, link, share_count):
    """Executes the sharing process using multiple threads."""
    success_queue = Queue()
    start_time = time.time()

    print(f"{y}🚀 Starting sharing process...")  

    with ThreadPoolExecutor(max_workers=min(len(tokens), 70)) as executor:
        futures = []
        for i in range(share_count):
            token = tokens[i % len(tokens)]
            futures.append(executor.submit(worker, token, link, success_queue))

        # Ensure all tasks complete
        for future in futures:
            future.result()

    elapsed_time = time.time() - start_time
    avg_time_per_share = elapsed_time / share_count if share_count > 0 else 0

    total_time = timedelta(seconds=int(elapsed_time))
    avg_time = timedelta(seconds=int(avg_time_per_share))

    success_count = success_queue.qsize()

    print(f"\n{b}📋 Success Details:")
    if success_count == 0:
        print(f"{r}❌ No posts were successfully shared.")
    while not success_queue.empty():
        print(f"{g}✅ {success_queue.get()}")

    print(f"\n🚀 Target: {link}")
    print(f"{g}✅ Successfully Shared: {success_count}/{share_count}")
    
    if success_count < share_count:
        print(f"{r}⚠️ Warning: Not all shares were completed. Some tokens may be invalid.")
    
    print(f"⏳ Total Time: {total_time}")
    print(f"⏱️ Average Time per Share: {avg_time}")

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        print(f"{r}❌ No valid tokens found. Exiting...")
        return

    link = input("Enter the post link to share: ").strip()
    print(f"\n{g}✅ Link Confirmed: {link}")

    try:
        total_shares = int(input("Enter the total number of shares: ").strip())
        if total_shares <= 0:
            print(f"{r}❌ Total shares must be greater than 0.")
            return
    except ValueError:
        print(f"{r}❌ Invalid input. Please enter a number.")
        return

    fast_share(tokens, link, total_shares)

if __name__ == "__main__":
    main()
