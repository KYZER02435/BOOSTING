import os
# Define color variables
red = "\033[1;31m"    # Bold red
c = "\033[1;96m"      # Cyan (for overview heading)
r = "\033[0m"         # Reset color
wh = "\033[1;37m"     # Bold white
def clear_screen():
    os.system('clear')

def count_lines(file_path):
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0  # Return 0 if the file does not exist

def overview():
    print(f"\033[1;96m ━━━━━━━━━━━━━━━━━━━━━━━━━[{red}OVERVIEW{c}]━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total_accounts = count_lines("/sdcard/Test/toka.txt")
    total_pages = count_lines("/sdcard/Test/tokp.txt")
    print(f"  {r}                   TOTAL ACCOUNTS: {c}{total_accounts}{r}")
    print(f'{c} ═════════════════════════════════════════════════════════════{wh}')

def clone_and_run(repo_url, script_name):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    
    if not os.path.exists(repo_name):
        os.system(f'git clone {repo_url}')

    os.chdir(repo_name)
    
    os.system(f'python {script_name}')
    
    os.chdir('..')

def main_menu():
    clear_screen()
    overview()  # Call the overview function here

    print("[1] Extract Account")
    print("[2] Auto Facebook Followers")
    print("[3] Auto Comments")
    print("[4] Auto Reply to Comments")
    print("[5] Auto Reacts")
    print("[6] Auto Create Page")
    print("[0] Reset")
    print("[E] Exit")

    choice = input("Enter your choice: ").strip().upper()

    if choice == '1':
        extract_account()
    elif choice == '2':
        auto_facebook_followers()
    elif choice == '3':
        auto_comments()
    elif choice == '4':
        auto_reply_to_comments()
    elif choice == '5':
        auto_reacts()
    elif choice == '6':
        auto_create_page()
    elif choice == '0':
        reset()
    elif choice == 'E':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice, please try again.")
        main_menu()

def extract_account():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'extract-acc.py'
    clone_and_run(repo_url, script_name)

def auto_facebook_followers():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'auto-follow.py'
    clone_and_run(repo_url, script_name)

def auto_comments():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'auto_comment.py'
    clone_and_run(repo_url, script_name)

def auto_reply_to_comments():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'atrc.py'
    clone_and_run(repo_url, script_name)

def auto_reacts():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'auto_reacts.py'
    clone_and_run(repo_url, script_name)

def auto_create_page():
    repo_url = 'https://github.com/KYZER02435/BOOST'
    script_name = 'atc_page.py'
    clone_and_run(repo_url, script_name)

def reset():
    folder_name = "Test"
    file_names = ["toka.txt", "tokaid.txt", "tokp.txt", "tokpid.txt", "cok.txt", "cokid.txt"]
    
    if os.path.exists(folder_name):
        for root, dirs, files in os.walk(folder_name, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                os.remove(file_path)
            for name in dirs:
                dir_path = os.path.join(root, name)
                os.rmdir(dir_path)
        os.rmdir(folder_name)
        print(f"{c}Successfully Reset.{r}")
    else:
        print(f"{red}Failed to reset.")

if __name__ == "__main__":
    main_menu()
