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
    major_versions = [300, 321, 326, 330, 340, 350, 360, 370, 380]  # Known major versions
    minor_version = random.randint(0, 99)
    patch_version = random.randint(100, 999)

    fbav = f"{random.choice(major_versions)}.{minor_version}.0.{patch_version}"
    fbbv = str(random.randint(100000000, 999999999))
    density = random.choice(["1.0", "1.5", "2.0", "2.5", "3.0", "4.0", "5.0", "6.0", "8.0"])

    width = random.choice(["1280", "1366", "1440", "1600", "1920", "2560", "2880", "3200", "3840", "4096", "5120"])
    height = random.choice(["720", "768", "900", "1080", "1440", "1600", "1800", "2160", "2400", "2880", "3200"])

    fblc = random.choice([
        "fr_FR", "en_US", "es_ES", "de_DE", "it_IT", "pt_BR", "zh_CN", "ja_JP", "ko_KR", "ar_AR", "ru_RU", "tr_TR",
        "pl_PL", "nl_NL", "sv_SE", "da_DK", "fi_FI", "no_NO", "cs_CZ", "hu_HU", "el_GR", "ro_RO", "sk_SK", "bg_BG",
        "hr_HR", "sr_RS", "lt_LT", "lv_LV", "et_EE", "ms_MY", "th_TH", "vi_VN", "id_ID", "hi_IN", "bn_BD", "fa_IR", "uk_UA", "he_IL"
    ])
    fbrv = str(random.randint(200000000, 900000000))
    
    fbca = random.choice(["x86", "x86_64", "amd64", "intel64", "arm64", "arm", "armv7", "armv8", "armv7l", "ia64", "ppc", "ppc64", "mips", "mips64", "sparc", "sparc64", "riscv", "riscv64"])
    
    fbpn_values = [
        "com.facebook.katana", 
        "com.facebook.lite", 
        "com.facebook.messenger",
        "com.facebook.web"
    ]
    fbpn = random.choice(fbpn_values)
    
    fbsrv = f"{random.randint(13, 18)}.0"
    fbop = str(random.randint(5, 30))

    hp_laptop_models = [
        "HP Pavilion 15", "HP Envy x360", "HP Spectre x360", 
        "HP EliteBook 840", "HP Omen 15", "HP ProBook 450",
        "HP Chromebook 14", "HP ZBook Studio G7", "HP Stream 14",
        "HP Elite Dragonfly", "HP Envy 13", "HP 15s", "HP EliteBook x360",
        "HP Pro x2", "HP ZBook Fury 15", "HP Envy 17", "HP Spectre Folio",
        "HP Pavilion x360", "HP Chromebook x2", "HP OMEN X 2S", "HP ENVY x2",
        "HP EliteBook 850", "HP ZBook Create G7", "HP Pavilion Gaming 16",
        "HP ENVY 15", "HP Omen X", "HP ZBook 17 G6", "HP Envy x2",
        "HP Omen 17", "HP Pavilion 14", "HP 250 G8", "HP EliteBook 1040",
        "HP Pavilion Gaming 15", "HP Chromebook 11", "HP ProBook 640",
        "HP EliteBook 830", "HP ZBook Power G8", "HP Omen Obelisk",
        "HP Spectre x2", "HP EliteBook 735", "HP Envy x360 15", 
        "HP ProBook 440", "HP Pavilion Aero 13", "HP ZBook Firefly 14",
        "HP Stream 11", "HP EliteBook 845", "HP Chromebook x360 14c",
        "HP ProBook 455", "HP Pavilion 13"
    ]

    dell_laptop_models = [
        "Dell XPS 13", "Dell XPS 15", "Dell Inspiron 15", "Dell Inspiron 13",
        "Dell Latitude 7420", "Dell Latitude 7320", "Dell Vostro 14", "Dell G5 15",
        "Dell Precision 3550", "Dell Alienware M15", "Dell G7 17", "Dell XPS 17",
        "Dell Inspiron 16 Plus", "Dell Latitude 9420", "Dell Precision 5550",
        "Dell Inspiron 14", "Dell Latitude 5520", "Dell Precision 5750", 
        "Dell Alienware X17", "Dell G3 15", "Dell Inspiron 14 5000", 
        "Dell Precision 7750", "Dell Vostro 13", "Dell Alienware Area-51m", 
        "Dell XPS 13 2-in-1", "Dell Latitude 3410", "Dell G15", "Dell Inspiron 7000", 
        "Dell Latitude 5400", "Dell Vostro 15 3000", "Dell Precision 3551",
        "Dell XPS 13 Plus", "Dell Inspiron 13 7000", "Dell Latitude 5430", 
        "Dell Precision 7560", "Dell Alienware m17 R5", "Dell G15 5515", 
        "Dell Inspiron 14 7000", "Dell Latitude 7440", "Dell XPS 15 9520", 
        "Dell G16", "Dell Inspiron 15 5000", "Dell Precision 3570", 
        "Dell Vostro 15 5000", "Dell Alienware x14", "Dell Latitude 7330", 
        "Dell XPS 13 OLED", "Dell Inspiron 16 7000", "Dell Precision 5580", 
        "Dell Alienware x17 R2", "Dell G15 5520", "Dell Inspiron 13 5000", 
        "Dell Latitude 7430", "Dell XPS 17 9720", "Dell Vostro 15 7000"
    ]

    lenovo_laptop_models = [
        "Lenovo ThinkPad X1 Carbon", "Lenovo Yoga Slim 7i", "Lenovo Legion 5",
        "Lenovo IdeaPad 3", "Lenovo Yoga 9i", "Lenovo ThinkBook 14s",
        "Lenovo ThinkPad T14", "Lenovo IdeaPad Flex 5", "Lenovo Yoga C940",
        "Lenovo ThinkPad P15", "Lenovo Legion 7", "Lenovo ThinkPad X13",
        "Lenovo Legion Y740", "Lenovo IdeaPad S540", "Lenovo ThinkPad X1 Extreme",
        "Lenovo ThinkPad L13", "Lenovo Yoga 7i", "Lenovo ThinkPad P1", "Lenovo Legion 5 Pro", 
        "Lenovo IdeaPad Gaming 3", "Lenovo ThinkPad X12 Detachable", "Lenovo Yoga Duet 7i", 
        "Lenovo Legion Slim 7", "Lenovo ThinkPad X280", "Lenovo IdeaPad 5", 
        "Lenovo ThinkBook Plus", "Lenovo ThinkPad L15", "Lenovo Yoga S940", 
        "Lenovo ThinkPad E14", "Lenovo ThinkPad P17", "Lenovo Legion Y530",
        "Lenovo ThinkPad X1 Yoga Gen 6", "Lenovo Yoga 9i 14", "Lenovo Legion 7i", 
        "Lenovo IdeaPad 5 Pro", "Lenovo ThinkBook 15 Gen 3", "Lenovo Yoga 6", 
        "Lenovo ThinkPad X1 Nano", "Lenovo Legion 5i Pro", "Lenovo IdeaPad Flex 5i", 
        "Lenovo ThinkPad L15 Gen 2", "Lenovo Yoga 9i 15", "Lenovo ThinkPad P52", 
        "Lenovo ThinkPad T15", "Lenovo Legion 5 Pro 16", "Lenovo IdeaPad Gaming 3i", 
        "Lenovo ThinkPad X1 Carbon Gen 10", "Lenovo Yoga 7i 14", "Lenovo Legion 5i", 
        "Lenovo IdeaPad 5i Pro", "Lenovo ThinkPad P43s", "Lenovo Yoga C9", 
        "Lenovo ThinkPad X1 Fold", "Lenovo ThinkBook 14 Gen 2", "Lenovo Legion 7i Pro", 
        "Lenovo Yoga 9i 13", "Lenovo IdeaPad Gaming 3 Pro"
    ]

    acer_laptop_models = [
        "Acer Swift 3", "Acer Predator Helios 300", "Acer Aspire 5", "Acer Spin 5",
        "Acer Chromebook 314", "Acer Nitro 5", "Acer TravelMate P6", "Acer ConceptD 7",
        "Acer Enduro N7", "Acer Chromebook Spin 713", "Acer Aspire 7", "Acer Swift 7",
        "Acer TravelMate P2", "Acer Aspire E 15", "Acer Swift X", "Acer Aspire 3", 
        "Acer Spin 3", "Acer Predator Triton 300", "Acer Enduro Urban N3", 
        "Acer ConceptD 3", "Acer Chromebook 514", "Acer Nitro 7", "Acer Aspire S3", 
        "Acer Spin 7", "Acer TravelMate X5", "Acer Enduro T1", "Acer Aspire VX 15", 
        "Acer Swift 5", "Acer TravelMate B3", "Acer Predator Helios 500",
        "Acer Aspire Vero", "Acer Predator Triton 500 SE", "Acer Chromebook 317",
        "Acer Swift Edge", "Acer Aspire 5 A515", "Acer Nitro 16", 
        "Acer Spin 714", "Acer Enduro Urban T3", "Acer TravelMate P4",
        "Acer ConceptD 9", "Acer Chromebook 315", "Acer Aspire 5 Slim",
        "Acer Swift Go", "Acer Predator Helios Neo 16", "Acer Chromebook Vero 514",
        "Acer Aspire 7 Nitro 5", "Acer Predator Helios 700", "Acer Swift 5X", 
        "Acer Aspire 5 Pro", "Acer Nitro 50", "Acer Predator Triton 300 SE",
        "Acer Chromebook 311", "Acer ConceptD 7 Ezel", "Acer Enduro T5", 
        "Acer Swift 3X", "Acer Predator Helios 300 SE", "Acer Aspire 3 A315",
        "Acer Spin 5 Pro", "Acer Nitro 5 AN515", "Acer Chromebook 11 C732",
        "Acer ConceptD 5", "Acer Enduro N3", "Acer Aspire 1", "Acer Swift 3 SF314"
    ]

    asus_laptop_models = [
        "ASUS ZenBook Duo", "ASUS ROG Zephyrus G14", "ASUS VivoBook S15", "ASUS TUF Dash F15",
        "ASUS Chromebook Flip", "ASUS ExpertBook B9", "ASUS ROG Strix G15", "ASUS ZenBook 14",
        "ASUS VivoBook Flip 14", "ASUS ROG Flow X13", "ASUS ProArt StudioBook Pro", "ASUS TUF Gaming A15",
        "ASUS ZenBook Pro Duo", "ASUS VivoBook 15", "ASUS ROG Zephyrus M16", "ASUS ZenBook 13",
        "ASUS Chromebook C425", "ASUS VivoBook S14", "ASUS ZenBook Flip S", "ASUS TUF Gaming F17",
        "ASUS ROG Strix Scar 15", "ASUS VivoBook Ultra K15", "ASUS ZenBook S",
        "ASUS ROG Zephyrus G15", "ASUS VivoBook Pro 14", "ASUS ROG Zephyrus S17", "ASUS ExpertBook P1",
        "ASUS ROG Zephyrus Duo 15", "ASUS VivoBook E14",
        "ASUS ZenBook Flip 13", "ASUS VivoBook K571", "ASUS ExpertBook L1",
        "ASUS ROG Strix Scar 17", "ASUS Chromebook CX9", "ASUS TUF Gaming FX505",
        "ASUS ZenBook UX425", "ASUS ROG Strix G17", "ASUS VivoBook 14",
        "ASUS ProArt StudioBook 16", "ASUS TUF Gaming FX705", "ASUS ZenBook Flip 15",
        "ASUS VivoBook 17", "ASUS ROG Zephyrus G GA502", "ASUS ExpertBook P2",
        "ASUS ROG Strix Hero III", "ASUS ZenBook UX434", "ASUS VivoBook Flip TP470",
        "ASUS ROG Zephyrus Duo SE", "ASUS Chromebook C223", "ASUS VivoBook Ultra 15",
        "ASUS ZenBook 15", "ASUS ROG Flow X16", "ASUS TUF Gaming A17",
        "ASUS VivoBook Flip TP401", "ASUS ROG Zephyrus GX501", "ASUS VivoBook E12",
        "ASUS ZenBook Pro 15", "ASUS ROG Zephyrus S GX701", "ASUS TUF Gaming FX506",
        "ASUS Chromebook Flip C434", "ASUS ZenBook Pro 14", "ASUS VivoBook 13 Slate OLED",
        "ASUS ROG Zephyrus M GU502", "ASUS Chromebook Detachable CM3", "ASUS VivoBook Pro 15",
        "ASUS TUF Dash F17", "ASUS ZenBook Flip UX363", "ASUS ROG Strix Scar III",
        "ASUS VivoBook S14 S433", "ASUS Chromebook Flip C536", "ASUS ROG Zephyrus G15 GA503",
        "ASUS VivoBook Flip TM420", "ASUS ZenBook Pro Duo UX581", "ASUS ExpertBook B1",
        "ASUS VivoBook Flip 12", "ASUS ROG Strix G531", "ASUS ZenBook 14X OLED",
        "ASUS TUF Gaming A15 FA506", "ASUS ZenBook Flip 14 UX463", "ASUS VivoBook 15 X515",
        "ASUS ROG Zephyrus G15 GA502", "ASUS ZenBook S UX393", "ASUS Chromebook Flip C214",
        "ASUS ZenBook Pro Duo 15", "ASUS ExpertBook B3 Flip", "ASUS VivoBook Ultra K14",
        "ASUS ROG Zephyrus Duo 16", "ASUS Chromebook C202", "ASUS TUF Dash FX516",
        "ASUS ZenBook 13 OLED", "ASUS VivoBook S14 M433", "ASUS ZenBook Flip UX461",
        "ASUS ROG Zephyrus GX531", "ASUS VivoBook Ultra A512", "ASUS Chromebook C523",
        "ASUS ZenBook 13 UX325", "ASUS TUF Gaming FX504", "ASUS ZenBook Flip S UX370",
        "ASUS VivoBook Flip TP501", "ASUS ZenBook Flip 14 UM462", "ASUS Chromebook C302",
        "ASUS VivoBook Flip 14 TP412", "ASUS ZenBook Pro Duo UX582", "ASUS VivoBook 15 X512"
    ]
    
    alienware_laptop_models = [
        "Alienware m15 R7", "Alienware x15 R2", "Alienware x17 R2", 
        "Alienware m17 R5", "Alienware Area-51m R2", "Alienware m15 R6", 
        "Alienware m17 R4", "Alienware x17 R1", "Alienware Area-51m", 
        "Alienware 13 R3", "Alienware 17 R5", "Alienware Aurora R11", 
        "Alienware 15 R2", "Alienware 18", "Alienware m15 R5", 
        "Alienware 15 R3", "Alienware Area-51m R1", "Alienware 17 R4",
        "Alienware m15", "Alienware 13 R2", "Alienware x14", "Alienware M11x", 
        "Alienware M14x", "Alienware M17x", "Alienware 17 R3", 
        "Alienware 15 R4", "Alienware 13 R1", "Alienware 18 R1", 
        "Alienware M17", "Alienware Aurora R10", "Alienware Aurora R9"
    ]

    samsung_laptop_models = [
        "Samsung Galaxy Book Pro 360", "Samsung Galaxy Book Flex2 Alpha", 
        "Samsung Galaxy Book Ion", "Samsung Galaxy Book Go", "Samsung Notebook 9 Pro", 
        "Samsung Notebook Odyssey Z", "Samsung Galaxy Book S", "Samsung Notebook 7 Spin", 
        "Samsung Notebook 9 Pen", "Samsung Chromebook Plus V2", 
        "Samsung Galaxy Chromebook 2", "Samsung Notebook 5", "Samsung Galaxy Book Ion2", 
        "Samsung Galaxy Book Flex Alpha", "Samsung ATIV Book 9", "Samsung ATIV Book 4", 
        "Samsung Notebook 9", "Samsung Chromebook 4", "Samsung ATIV Book 8", 
        "Samsung Chromebook Pro", "Samsung Galaxy Chromebook", 
        "Samsung Galaxy Book Flex 15", "Samsung Galaxy Book Pro", "Samsung Chromebook Plus", 
        "Samsung ATIV Book 2", "Samsung Notebook Series 7", "Samsung Notebook Series 9", 
        "Samsung Galaxy Book Flex 13", "Samsung Notebook 7", "Samsung ATIV Smart PC"
    ]

    razer_laptop_models = [
        "Razer Blade 15 Advanced Model", "Razer Blade 14", "Razer Blade Stealth 13", 
        "Razer Blade Pro 17", "Razer Book 13", "Razer Blade 15 Base Model", 
        "Razer Blade 17 Pro", "Razer Blade Stealth 12.5\"", "Razer Blade Studio Edition", 
        "Razer Blade 13 Mercury White", "Razer Blade 13 Quartz Pink", "Razer Blade 15 OLED", 
        "Razer Book 2020 Edition", "Razer Blade 15 Advanced Model 2021", 
        "Razer Blade 15 Base Model 2020", "Razer Blade 17 Pro 2021", 
        "Razer Blade Pro 17 2020", "Razer Blade 15 OLED 2020", 
        "Razer Blade 15 Base Model 2021", "Razer Blade Stealth 2021", 
        "Razer Blade 14 2021", "Razer Blade Pro 2021", "Razer Blade 13 Early 2020", 
        "Razer Blade Stealth 2019", "Razer Blade Stealth 2017", "Razer Blade 2016", 
        "Razer Blade Pro 2017", "Razer Blade 15 Advanced Model 2018", 
        "Razer Blade 15 Base Model 2019", "Razer Blade Stealth 2018"
    ]

    msi_laptop_models = [
        "MSI GE76 Raider", "MSI GS66 Stealth", "MSI Creator Z16", "MSI GP66 Leopard", 
        "MSI Summit E13 Flip Evo", "MSI GS75 Stealth", "MSI GL65 Leopard", 
        "MSI GT76 Titan", "MSI Prestige 14 Evo", "MSI Alpha 15", "MSI Modern 15", 
        "MSI Prestige 15 A10SC", "MSI Bravo 15", "MSI Katana GF66", "MSI Pulse GL66", 
        "MSI GF63 Thin", "MSI WS66", "MSI WE75", "MSI GF65 Thin", "MSI Stealth 15M", 
        "MSI Prestige 15", "MSI WS75", "MSI Modern 14", "MSI GP65 Leopard", 
        "MSI Prestige 14", "MSI GT75 Titan", "MSI GL63", "MSI GV72", 
        "MSI GL72M", "MSI GL62M", "MSI GS63VR"
    ]

    lg_laptop_models = [
        "LG Gram 17", "LG Gram 16 2-in-1", "LG Gram 14", "LG Ultra PC 17", 
        "LG Ultra Gear 17", "LG Gram 15Z90N", "LG Gram 14Z90P", "LG Gram 16Z90P", 
        "LG Gram 13.3\"", "LG Gram Ultra-Light", "LG Gram Ultra Slim", 
        "LG Gram 17Z90P", "LG Gram 14T90N", "LG Ultra-Light 14U70Q", 
        "LG Gram 14T90P", "LG Gram 16T90P", "LG Ultra PC 16", 
        "LG Ultra Gear 15", "LG Gram 15Z90P", "LG Gram 17Z90N", "LG Gram 16T90N", 
        "LG Gram 13Z990", "LG Gram 14Z990", "LG Ultra Gear 16", 
        "LG Gram 15Z980", "LG Gram 17Z980", "LG Gram 15Z990", "LG Ultra-Light 15", 
        "LG Gram 14Z980", "LG Gram 17T90P"
    ]

    brands = {
        "HP": hp_laptop_models,
        "Dell": dell_laptop_models,
        "Lenovo": lenovo_laptop_models,
        "Acer": acer_laptop_models,
        "ASUS": asus_laptop_models,
        "Alienware": alienware_laptop_models,
        "Samsung": samsung_laptop_models,
        "Razer": razer_laptop_models,
        "MSI": msi_laptop_models
    }

    manufacturer = random.choice(list(brands.keys()))
    model = random.choice(brands[manufacturer])

    operating_systems = ["Windows 10", "Windows 11", "Windows 8.1", "Windows 7", "Ubuntu", "Fedora", "Debian", "Linux Mint", "Elementary OS", "Chrome OS", "Pop!_OS", "Red Hat Enterprise Linux", "Linux", "CentOS", "Manjaro Linux", "OpenSUSE", "Solus", "MX Linux"]
    os_choice = random.choice(operating_systems)

    carriers = [
        "Robi", "AT&T", "Verizon", "T-Mobile", "Vodafone", "Orange", "Telekom", "O2", "BT", 
        "Movistar", "Claro", "Telstra", "Sprint", "Airtel", "Reliance Jio", "China Mobile", 
        "China Telecom", "China Unicom", "NTT DoCoMo", "SoftBank", "KDDI", "SK Telecom", 
        "KT Corporation", "LG Uplus", "TIM", "Wind Tre", "Bouygues Telecom", "SFR", "Telkomsel", 
        "Indosat Ooredoo", "XL Axiata", "Smartfren", "TrueMove", "AIS", "DTAC", "MTN", "Vodacom", 
        "Cell C", "Telstra", "Optus", "Singtel", "StarHub", "M1", "Globe Telecom", "Smart Communications", 
        "PLDT", "Digicel", "Claro Brazil", "Oi", "TIM Brasil", "Vivo", "Entel", "Movilnet", "Claro Peru", 
        "Entel Chile", "Tigo", "Personal", "Claro Argentina", "Movistar Argentina", "Movistar Venezuela", 
        "Claro Colombia", "Movistar Colombia", "Movistar Mexico", "Claro Ecuador", "CNT Ecuador", 
        "Movistar Uruguay", "Claro Uruguay", "U Mobile", "Maxis", "Celcom", "Digi Telecommunications", 
        "Free Mobile", "Bouygues Telecom", "SFR", "Wind Hellas", "Cosmote", "MTN Cyprus", 
        "Vodafone Cyprus", "Telecom Italia", "KPN", "Telfort", "Vodafone Netherlands", "Proximus", 
        "Orange Belgium", "BASE", "Swisscom", "Sunrise", "Salt Mobile", "A1 Telekom Austria", 
        "T-Mobile Austria", "Magenta Telekom", "Hutchison Drei Austria", "Telenor", "Telia", "Elisa", 
        "DNA", "Tele2", "Megafon", "MTS", "Beeline", "Tele2 Russia", "Kyivstar", "Vodafone Ukraine", 
        "Lifecell", "Moldcell", "Orange Moldova", "Unitel Mongolia", "G-Mobile", "Mobicom", "Ooredoo Myanmar", 
        "MPT", "Telenor Myanmar", "STC", "Mobily", "Zain", "Du", "Etisalat", "Batelco", "Viva Bahrain", 
        "Ooredoo Qatar", "Vodafone Qatar", "Omantel", "Ooredoo Oman", "Tata DoCoMo", "BSNL", "MTNL"
    ]
    carrier = random.choice(carriers)

    user_agent = (
        f"[FBAN/FBWEB;FBAV/{random.randint(11, 99)}.0.0.{random.randint(1111, 9999)};FBBV/{random.randint(1111111, 9999999)};"
        f"[FBAN/FBWEB;FBAV/{fbav};FBBV/{fbbv};"
        f"FBDM{{density={density},width={width},height={height}}};"
        f"FBLC/{fblc};FBRV/{fbrv};"
        f"FBCR/{carrier};FBMF/{manufacturer};FBBD/{manufacturer};"
        f"FBPN/{fbpn};FBDV/{model};FBSV/{fbsrv};FBOP/{fbop};FBCA/{fbca};]"
    )
    return user_agent

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
