import os
import requests
import threading
import time
from datetime import timedelta
from queue import Queue
from rich.console import Console
from rich.panel import Panel

console = Console()
print_lock = threading.Lock()  # Lock to synchronize print outputs

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
            return response.get('id')
    except requests.exceptions.RequestException:
        pass
    return None

def load_tokens(file_path):
    """Loads tokens from a file, one token per line."""
    if not os.path.exists(file_path):
        console.print("[bold red]❌ Token file not found.[/bold red]")
        return []

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def worker(tokens, link, total_shares, success_queue, counter):
    """Thread worker function to share posts across multiple tokens."""
    while not total_shares.empty():
        token_index = total_shares.get()
        token = tokens[token_index % len(tokens)]
        post_id = share_post(token, link)

        # Thread-safe counter updates
        with print_lock:
            counter["current"] += 1
            if post_id:
                success_queue.put(f"{token[:8]}_{post_id}")
                counter["success"] += 1
            else:
                counter["failed"] += 1

        # Thread-safe progress display
        display_progress(counter, f"{token[:8]}_{post_id}" if post_id else None)
        total_shares.task_done()

def display_progress(counter, success_detail=None):
    """Displays the current progress inside a panel."""
    with print_lock:  # Ensure only one thread prints at a time
        panel_header = f"[bold magenta]SENT [bold green]{counter['current']} OUT OF {counter['total']}[/bold green] SHARES[/bold magenta]"
        panel_content = ""
        if success_detail:
            panel_content = f"[bold yellow]SUCCESSFULLY SHARED:[/bold yellow] [bold green]{success_detail}[/bold green]"
        panel = Panel(panel_content, title=panel_header, border_style="magenta")
        console.print(panel, justify="center")

def fast_share(tokens, link, share_count):
    """Executes the sharing process using multiple threads."""
    threads = []
    success_queue = Queue()
    total_shares = Queue()
    counter = {"current": 0, "total": share_count, "success": 0, "failed": 0}

    for i in range(share_count):
        total_shares.put(i)

    start_time = time.time()
    for _ in range(min(len(tokens), 80)):
        thread = threading.Thread(target=worker, args=(tokens, link, total_shares, success_queue, counter))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    avg_time = timedelta(seconds=int(elapsed_time))
    days, hours, minutes, seconds = avg_time.days, avg_time.seconds // 3600, (avg_time.seconds // 60) % 60, avg_time.seconds % 60

    # Adjusted header for final panel
    panel_header = f"[bold cyan]{share_count}[/bold cyan] [bold yellow]SHARES SUCCESSFULLY REACHED[/bold yellow]"

    final_panel_text = (
        f"[bold cyan]LINK:[/bold cyan] [bold green]{link}[/bold green]\n"
        f"[bold cyan]AVERAGE TIME:[/bold cyan] [bold blue]{days:02d}|{hours:02d}|{minutes:02d}|{seconds:02d}[/bold blue]"
    )

    # Final panel with updated header
    console.print(Panel(final_panel_text, title=panel_header, border_style="magenta"), justify="center")

def main():
    token_file = "/sdcard/Test/toka.txt"
    tokens = load_tokens(token_file)

    if not tokens:
        console.print("[bold red]❌ No valid tokens found. Exiting...[/bold red]")
        return

    link = input("Enter the post link to share: ").strip()
    try:
        total_shares = int(input("Enter the total number of shares: ").strip())
        if total_shares <= 0:
            console.print("[bold red]❌ Total shares must be greater than 0.[/bold red]")
            return
    except ValueError:
        console.print("[bold red]❌ Invalid input. Please enter a number.[/bold red]")
        return

    fast_share(tokens, link, total_shares)

if __name__ == "__main__":
    main()
