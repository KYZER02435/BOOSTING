import os
import requests
import uuid
import random

# Define color codes
green = '\033[1;32m'  # Bold Green
red = '\033[1;31m'    # Bold Red
reset = '\033[0m'      # Reset

folder_name = "/sdcard/Test"
file_names = ["toka.txt", "tokaid.txt", "tokp.txt", "tokpid.txt", "cok.txt", "cokid.txt"]

if not os.path.exists(folder_name):
    try:
        os.makedirs(folder_name)
        print(f"{green}Folder '{folder_name}' created.{reset}")
    except Exception as e:
        print(f"{red}Failed to create folder '{folder_name}': {e}{reset}")
else:
    print(f"{green}Folder '{folder_name}' already exists.{reset}")

for file_name in file_names:
    file_path = os.path.join(folder_name, file_name)
    if not os.path.exists(file_path):  
        try:
            with open(file_path, 'w') as file:
                pass  
            print(f"{green}File '{file_path}' created.{reset}")
        except Exception as e:
            print(f"{red}Failed to create file '{file_path}': {e}{reset}")
    else:
        print(f"{green}File '{file_path}' already exists.{reset}")

def linex():
    print("-" * 50)

def count_lines(filepath):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return sum(1 for _ in file)
        else:
            return 0
    except Exception as e:
        print(f"{red}Error counting lines in {filepath}: {e}{reset}")
        return 0

def overview():
    print(f"\033[1;96m  ━━━━━━━━━━━━━━━━━━━━━━━━[{red}OVERVIEW{reset}]━━━━━━━━━━━━━━━━━━━━━━━━━━")
    total_accounts = count_lines("/sdcard/Test/toka.txt")
    total_pages = count_lines("/sdcard/Test/tokp.txt")
    print(f"  {red}             TOTAL ACCOUNTS: {reset}{total_accounts}{red} | TOTAL PAGES: {reset}{total_pages} {red}")
    print(f'{reset}  ════════════════════════════════════════════════════════════')

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
        print(f"{red}Invalid option.{reset}")
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
            print(f'{red}Error reading the file: {e}{reset}')
    else:
        print(f'{red}File location not found.{reset}')

def Auto():
    directory = '/sdcard'
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    if not txt_files:
        print(f'{red}No .txt files found in {directory}{reset}')
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
                    print(f'{red}Error reading the file: {e}{reset}')
            else:
                print(f'{red}File not found.{reset}')
        else:
            print(f'{red}Invalid option.{reset}')
    except ValueError:
        print(f'{red}Invalid input.{reset}')

def process_users(user_list, user_choice):
    for user_pass in user_list:
        if len(user_pass) == 2:
            user, passw = user_pass
            cuser(user, passw, user_choice)
        else:
            print(f"{red}Invalid format in line: {user_pass}{reset}")

def kyzer():
    model_prefixes = {
        "Samsung": "SM-",
        "Realme": "RMX",
        "Oppo": "CPH",
        "Xiaomi": "M",
        "Poco": "Poco ",
        "Vivo": "V",
        "Nokia": "TA-",
        "Huawei": "CLT-",
        "Infinix": "X",
        "Tecno": "CD-",
        "OnePlus": "NE",
        "LG": "LM-",
        "Sony": "G",
        "Motorola": "XT",
        "Asus": "ASUS_",
        "Lenovo": "LNV-",
        "Google": "Pixel ",
        "ZTE": "ZTE_",
        "HTC": "HTC_",
        "Alcatel": "ALC-",
        "BlackBerry": "BB-",
        "Honor": "HONOR_",
        "Itel": "IT_",
        "Micromax": "MMX_",
        "Panasonic": "PANA_",
        "Meizu": "MZ_",
        "Sharp": "SH-",
        "Coolpad": "CP_",
        "Lava": "LAVA_",
        "iQOO": "I",
        "Acer": "ACER_",
        "Toshiba": "TOSHIBA_",
        "Dell": "DELL_",
        "MSI": "MSI_",
        "Razer": "RAZER_",
        "Alienware": "ALIEN_",
        "Apple": "iPhone ",
        "Nothing": "Nothing Phone ",
        "Fairphone": "FP",
        "Redmi": "Redmi Note ",
        "Vsmart": "Vsmart ",
        "Essential": "PH-",
        "Gionee": "Gionee "
    }

    fbpn_options = [
        'com.facebook.katana',
        'com.facebook.lite',
        'com.facebook.orca',
        'com.facebook.mlite',
        'com.facebook.messenger'
    ]

    fbca_options = [
        "armeabi-v7a:armeabi", "arm64-v8a:armeabi",
        "armeabi-v7a", "armeabi", "arm86-v6a", "arm64-v8a"
    ]

    brand = random.choice(list(model_prefixes.keys()))
    model_prefix = model_prefixes[brand]

    # Generate realistic model numbers
    if brand in ["Samsung", "Sony", "ZTE", "Sharp", "Motorola", "HTC", "Fairphone"]:
        model = f"{model_prefix}{random.randint(100, 9999)}"
    elif brand in ["Realme", "Oppo", "Vivo", "Asus", "Honor", "Lenovo", "iQOO", "Acer", "MSI", "Razer"]:
        model = f"{model_prefix}{random.randint(1000, 99999)}"
    elif brand in ["Xiaomi", "Huawei", "Nokia", "Infinix", "Tecno", "Coolpad", "Meizu", "Micromax", "Itel", "Lava"]:
        model = f"{model_prefix}{random.randint(10, 9999)}"
    elif brand in ["OnePlus", "LG", "BlackBerry", "Panasonic", "Alcatel", "Gionee"]:
        model = f"{model_prefix}{random.randint(100, 99999)}"
    elif brand == "Google":
        model = f"{model_prefix}{random.choice(['4', '4a', '5', '5a', '6', '6a', '7', '7a', '8', '8a', 'Pro'])}"
    elif brand == "Poco":
        model = f"{model_prefix}{random.choice(['X3', 'F1', 'M3', 'F3', 'X4', 'M4', 'F5', 'X5', 'C40'])}"
    elif brand == "Redmi":
        model = f"{model_prefix}{random.choice(['8', '9', '10', '11', '12', '13'])} Pro"
    elif brand in ["Dell", "Toshiba", "Alienware"]:
        model = f"{model_prefix}{random.randint(1000, 99999)}"
    elif brand == "Nothing":
        model = f"{model_prefix}{random.choice(['1', '2'])}"
    elif brand == "Essential":
        model = f"{model_prefix}1"
    elif brand == "Apple":
        model = f"{model_prefix}{random.choice(['6', '6s', '7', '8', 'X', 'XR', 'XS', '11', '12', '13', '14', '15', 'SE', 'Plus', 'Mini', 'Pro'])}"

    fbav = f"{random.randint(100, 999)}.0.0.{random.randint(10, 99)}.{random.randint(100, 999)}"  # App version
    fbbv = random.randint(100000000, 999999999)  # Build version
    fbdm_width = random.choice([720, 1080, 1280, 1440, 1920])
    fbdm_height = int(fbdm_width * (16 / 9))  # Aspect ratio
    fbdm_density = round(random.uniform(2.0, 4.5), 1)  # Screen density
    fbca = random.choice(fbca_options)  # CPU architecture
    fbpn = random.choice(fbpn_options)  # Package name

    ua = (
        f"Dalvik/2.1.0 (Linux; U; Android {random.randint(6, 15)}; "
        f"{brand} {model}) "
        f"[FBAN/FB4A;FBAV/{fbav};FBBV/{fbbv};FBDM/{{density={fbdm_density},width={fbdm_width},height={fbdm_height}}};"
        f"FBLC/en_US;FBPN/{fbpn};FBOP/19;FBCA/{fbca}]"
    )

    return ua

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
        'User-Agent': kyzer(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com'
    }
    
    response = requests.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data, allow_redirects=False).json()
    
    if "session_key" in response:
        print(f"{green}Success: {user} extracted successfully.{reset}")
        
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
        print(f"{red}Failed: {user} isn't extracted.{reset}")

Initialize()
