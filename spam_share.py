import os
import requests
import threading

def share_post(token, link):
    """Shares a post on the user's feed with 'Only Me' privacy."""
    url = f"https://graph.facebook.com/v13.0/me/feed"
    payload = {
        'link': link,
        'published': '0',  
        'privacy': '{"value":"SELF"}',  
        'access_token': token
    }

    try:
        response = requests.post(url, data=payload).json()
        if 'id' in response:
            print(f"✅ Post shared successfully. Post ID: {response['id']}")
        else:
            print(f"❌ Failed to share post: {response}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error: {e}")

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        print("❌ Token file not found.")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(token, link, share_count):
    """Thread worker function to share posts multiple times for one token."""
    for _ in range(share_count):
        share_post(token, link)

def fast_share(tokens, link, total_shares):
    """Executes the sharing process using multiple threads."""
    share_count_per_token = max(1, total_shares // len(tokens))
    threads = []

    for token in tokens:
        thread = threading.Thread(target=worker, args=(token, link, share_count_per_token))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"\n🚀 Completed {total_shares} shares across all tokens.")

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

    fast_share(tokens, link, total_shares)

if __name__ == "__main__":
    main()
