import os
import requests
import uuid
import random

folder_name = "/sdcard/Test"
file_names = ["toka.txt", "tokaid.txt", "tokp.txt", "tokpid.txt", "cok.txt", "cokid.txt"]

# Check if the folder exists, if not, create it
if not os.path.exists(folder_name):
    try:
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
    except Exception as e:
        print(f"Failed to create folder '{folder_name}': {e}")
else:
    print(f"Folder '{folder_name}' already exists.")

# Check each file in the list
for file_name in file_names:
    file_path = os.path.join(folder_name, file_name)
    if not os.path.exists(file_path):  # Check if file exists
        try:
            with open(file_path, 'w') as file:
                pass  # Create an empty file if it doesn't exist
            print(f"File '{file_path}' created.")
        except Exception as e:
            print(f"Failed to create file '{file_path}': {e}")
    else:
        print(f"File '{file_path}' already exists.")
# Define colors
red = '\033[91m'
c = '\033[0m'
r = '\033[1;31m'
wh = '\033[0;37m'

def linex():
    print("-" * 50)

# Function to count lines in a file
def count_lines(filepath):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return sum(1 for _ in file)
        else:
            return 0
    except Exception as e:
        print(f"Error counting lines in {filepath}: {e}")
        return 0

def overview():
    print(f"\033[1;96m  ━━━━━━━━━━━━━━━━━━━━━━━━[{red}OVERVIEW{c}]━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total_accounts = count_lines("/sdcard/Test/toka.txt")
    total_pages = count_lines("/sdcard/Test/tokp.txt")
    print(f"  {r}             TOTAL ACCOUNTS: {c}{total_accounts}{r} | TOTAL PAGES: {c}{total_pages} {r}")
    print(f'{c}  ════════════════════════════════════════════════════════════{wh}')

def Initialize():
    print(f"  Please choose how you want to Extract.\n")
    print(f"     1. Manual through input")
    print(f"     2. Manual through File")
    print(f"     3. Automatic through File")
    print(f"     4. Overview")
    
    choice = input('   Choose: ')
    if choice == '1':
        Manual()
    elif choice == '2':
        ManFile()
    elif choice == '3':
        Auto()
    elif choice == '4':
        overview()
    else:
        print('Invalid option.')
        Initialize()

def Manual():
    user_choice = input(" Input y or leave blank if it's an account. If it's a page then input n (y/N/d): ")
    user = input("USER ID/EMAIL: ")
    passw = input("PASSWORD: ")
    linex()
    cuser(user, passw, user_choice)

def ManFile():
    file_path = input('Put file path: ')
    if os.path.isfile(file_path):
        try:
            user_choice = input(" Input y or leave blank if it's an account. If it's a page, input n (y/N/d): ")
            with open(file_path, 'r') as file:
                for line in file:
                    user_pass = line.strip().split('|')
                    process_users([user_pass], user_choice)
        except Exception as e:
            print(f'Error reading the file: {e}')
    else:
        print('File location not found.')

def Auto():
    directory = '/sdcard'
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    if not txt_files:
        print(f'No .txt files found in {directory}')
        return
    
    for i, filename in enumerate(txt_files, start=1):
        print(f"    {i}. {filename}")
    
    try:
        linex()
        choice = int(input('Choose: '))
        if 1 <= choice <= len(txt_files):
            selected_file = os.path.join(directory, txt_files[choice - 1])
            if os.path.isfile(selected_file):
                try:
                    user_choice = input(" Input y or leave blank if it's an account. If it's a page, input n (y/N/d): ")
                    with open(selected_file, 'r') as file:
                        for line in file:
                            user_pass = line.strip().split('|')
                            process_users([user_pass], user_choice)
                except Exception as e:
                    print(f'Error reading the file: {e}')
            else:
                print('File not found.')
        else:
            print('Invalid option.')
    except ValueError:
        print('Invalid input.')

def process_users(user_list, user_choice):
    for user_pass in user_list:
        if len(user_pass) == 2:
            user, passw = user_pass
            cuser(user, passw, user_choice)
        else:
            print(f"Invalid format in line: {user_pass}")

def cuser(user, passw, user_choice):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': f'{uuid.uuid4()}',
        'format': 'json',
        'device_id': f'{uuid.uuid4()}',
        'cpl': 'true',
        'family_device_id': f'{uuid.uuid4()}',
        'credentials_type': 'device_based_login_password',
        'email': user,
        'password': passw,
        'access_token': accessToken,
        'generate_session_cookies': '1',
        'locale': 'en_US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32',
    }
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 8.0.0; SM-A720F Build/R16NW) [FBAN/Orca-Android;FBAV/196.0.0.29.99;FBPN/com.facebook.orca;FBLC/en_US;FBBV/135374479;FBCR/SMART;FBMF/samsung;FBBD/samsung;FBDV/SM-A720F;FBSV/8.0.0;FBCA/armeabi-v7a:armeabi;FBDM/{density=3.0,width=1080,height=1920};FB_FW/1;]",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com'
    }
    
    response = requests.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data, allow_redirects=False).json()
    
    if "session_key" in response:
        print(f"Success: {user} extracted successfully.")
        
        cookie = ';'.join(f"{i['name']}={i['value']}" for i in response['session_cookies'])
        c_user_value = [i['value'] for i in response['session_cookies'] if i['name'] == 'c_user'][0]
        
        if user_choice.lower() in ['n', 'no']:
            with open('/sdcard/Test/tokpid.txt', 'a') as f:
                f.write(f'{c_user_value}\n')
            with open('/sdcard/Test/tokp.txt', 'a') as f:
                f.write(f'{response["access_token"]}\n')
        else:
            with open('/sdcard/Test/toka.txt', 'a') as f:
                f.write(f'{response["access_token"]}\n')
            with open('/sdcard/Test/tokaid.txt', 'a') as f:
                f.write(f'{c_user_value}\n')
        
        with open('/sdcard/Test/cok.txt', 'a') as f:
            f.write(f'{cookie}\n')
        with open('/sdcard/Test/cokid.txt', 'a') as f:
            f.write(f'{c_user_value}\n')
    else:
        print(f"Failed: {user} isn't extracted.")

# Start the tool
Initialize()