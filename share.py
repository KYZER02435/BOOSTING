import os
import re
import requests
import json
from datetime import datetime

def logo_menu():
    logo = """
    WELCOME TO FACEBOOK AUTO SHARE TOOLS
    """
    print(logo)

def login():
    os.system("clear")
    print("LOGIN COOKIES FIRST BRO")
    print("TAKE COOKIES FROM KIWI BROWSER")
    
    cookie = input("Enter your Facebook cookies: ")
    
    try:
        response = requests.get(
            "https://business.facebook.com/business_locations",
            headers={
                "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
                "referer": "https://www.facebook.com/",
                "host": "business.facebook.com",
                "origin": "https://business.facebook.com",
                "upgrade-insecure-requests": "1",
                "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "content-type": "text/html; charset=utf-8"
            },
            cookies={"cookie": cookie}
        )
        
        print(f"Response status code: {response.status_code}")
        
        find_token = re.search("(EAAG\w+)", response.text)
        if find_token:
            token = find_token.group(1)
            with open(".token.xx.txt", "w") as token_file:
                token_file.write(token)
            with open(".cookie.xx.txt", "w") as cookie_file:
                cookie_file.write(cookie)
            print("SUCCESSFUL LOGIN")
            bot_share(token, cookie)
        else:
            raise ValueError("Token not found in response")
    
    except Exception as e:
        print(f"Error during login: {e}")
        if os.path.exists(".token.xx.txt"):
            os.remove(".token.xx.txt")
        if os.path.exists(".cookie.xx.txt"):
            os.remove(".cookie.xx.txt")
        print("COOKIE INVALID")
        login()

def bot_share(token, cookie):
    os.system('clear')
    
    try:
        cookie_dict = {"cookie": cookie}
        ip = requests.get("https://api.ipify.org").text
        
        user_info = requests.get(f"https://graph.facebook.com/me?fields=name,id&access_token={token}", cookies=cookie_dict).json()
        name = user_info.get("name", "Unknown")
        id = user_info.get("id", "Unknown")
    
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return
    
    os.system('clear')
    print(f"USER ACTIVE     : {name}")
    print(f"YOUR ID         : {id}")
    print(f"YOUR IP         : {ip}")
    print(f"CURRENT DATE    : {datetime.now().strftime('%A, %d %B %Y')}")
    
    link = input("\nEnter the post link: ")
    jumlah = int(input("Initial amount of shares: "))
    
    print("\nAUTO SHARE IS RUNNING")
    start_time = datetime.now()
    
    try:
        n = 0
        header = {
            "authority": "graph.facebook.com",
            "cache-control": "max-age=0",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1"
        }
        
        while jumlah > 0:
            n += 1
            post = requests.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&privacy={{'value':'SELF'}}&access_token={token}", 
                headers=header, 
                cookies=cookie_dict
            ).json()
            
            print(f"API Response: {post}")  # Debug: Print the response
            
            if "COOKIE LIMIT" in json.dumps(post):
                print("\nCOOKIE LIMIT REACHED. PLEASE GET ANOTHER ONE.")
                return
            
            if "id" in post:
                elapsed_time = datetime.now() - start_time
                print(f"\rSuccessful sharing {n} post(s). Time elapsed: {elapsed_time}", end='')
                jumlah -= 1  # Decrement the number of shares left to do
            else:
                print("\nFailed to share the post. Possible issue with the token, cookie, or link.")
                return
    
    except requests.exceptions.ConnectionError:
        print("\nYou are not connected to the internet!")
        return

logo_menu()
login()