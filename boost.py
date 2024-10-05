import os
import shutil
import subprocess
import sys
import threading
import time

logo = (f''' \033[1;32m  
          /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$$
         | $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$|__  $$__/
         | $$  \\ $$| $$  \\ $$| $$  \\ $$| $$  \\__/   | $$   
         | $$$$$$$ | $$  | $$| $$  | $$|  $$$$$$    | $$   
         | $$__  $$| $$  | $$| $$  | $$ \\____  $$   | $$   
         | $$  \\ $$| $$  | $$| $$  | $$ /$$  \\ $$   | $$   
         | $$$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/   | $$   
         |_______/  \\______/  \\______/  \\______/    |__/   
                                                  
''')

red = "\033[1;31m"    # Bold red
c = "\033[1;96m"      # Cyan (for overview heading)
g = "\033[1;32m"      # Bold green
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
    print(logo)  # Print the logo
    print(f"\033[1;32m ━━━━━━━━━━━━━━━━━━━━━━━━━━[{g}OVERVIEW{g}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total_accounts = count_lines("/sdcard/Test/toka.txt")
    total_pages = count_lines("/sdcard/Test/tokp.txt")
    print(f"  {g}                   TOTAL ACCOUNTS: {g}{total_accounts}{g}")
    print(f'{g} ════════════════════════════════════════════════════════════════{r}')

def loading_spinner():
    spinner = ['|', '/', '-', '\\']
    while getattr(threading.currentThread(), "do_run", True):
        for symbol in spinner:
            sys.stdout.write(f'\r{symbol} Updating...')
            sys.stdout.flush()
            time.sleep(0.2)

def git_pull_repository():
    repo_path = '.'  # Assuming the script is in the repository you want to update
    spinner_thread = threading.Thread(target=loading_spinner)
    spinner_thread.start()
    
    try:
        subprocess.run(['git', 'pull'], cwd=repo_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{red}Error occurred while updating the repository: {e}{r}")
    finally:
        # Stop the spinner
        spinner_thread.do_run = False
        spinner_thread.join()  # Wait for the spinner thread to finish
        sys.stdout.write('\r')  # Clear the loading line

def clone_and_run(repo_url, script_name):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    
    if not os.path.exists(repo_name):
        os.system(f'git clone {repo_url}')

    os.chdir(repo_name)
    os.system(f'python {script_name}')
    os.chdir('..')

def update_method():
    git_pull_repository()  # Call the update function

def main_menu():
    clear_screen()
    overview()  # Call the overview function here

    print("[0] Update Tool")
    print("[1] Extract Account")
    print("[2] Auto Facebook Followers")
    print("[3] Auto Comments")
    print("[4] Auto Reply to Comments")
    print("[5] Auto Reacts")
    print("[6] Auto Create Page")
    print("[7] Auto React Comment")
    print("[8] Auto Reacts for Videos(NEW METHOD)")
    print('[9] Auto Reacts for Reels ')
    print("[10] Auto Join Groups")
    print("[R] Reset")
    print("[E] Exit")

    choice = input("Enter your choice: ").strip().upper()

    if choice == '0':
        update_method()  # Call the update function
    elif choice == '1':
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
    elif choice == '7':
        auto_react_comment()
    elif choice == '8':
        auto_working_vid()
    elif choice == '9':
        auto_reacts_reels()
    elif choice == '10':
        auto_join_groups()
    elif choice == 'R':
        reset()
    elif choice == 'E':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice, please try again.")
        main_menu()

def extract_account():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'extract-acc.py'
    clone_and_run(repo_url, script_name)

def auto_facebook_followers():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'auto-follow.py'
    clone_and_run(repo_url, script_name)

def auto_comments():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'auto_comment.py'
    clone_and_run(repo_url, script_name)

def auto_reply_to_comments():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'atrc.py'
    clone_and_run(repo_url, script_name)

def auto_reacts():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'auto-reacts.py'
    clone_and_run(repo_url, script_name)

def auto_create_page():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'atc_page.py'
    clone_and_run(repo_url, script_name)
    
def auto_react_comment():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'auto-react-comment.py'
    clone_and_run(repo_url, script_name)
    
def auto_working_vid():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'working-vid.py'
    clone_and_run(repo_url, script_name)
    
def auto_reacts_reels():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'reels_reacts.py'
    clone_and_run(repo_url, script_name)

def auto_join_groups():
    update_method()  # Call the update function
    repo_url = 'https://github.com/KYZER02435/BOOSTING'
    script_name = 'auto_join_group.py'
    clone_and_run(repo_url, script_name)

def reset():
    folder_path = '/sdcard/Test'
    
    # Check if the folder exists
    if os.path.exists(folder_path):
        try:
            # Delete the folder and all its contents
            shutil.rmtree(folder_path)
            print(f"Successfully deleted the folder: {folder_path}")
        except Exception as e:
            print(f"Error while deleting the folder: {e}")
    else:
        print(f"The folder {folder_path} does not exist.")

if __name__ == "__main__":
    main_menu()
