# Other imports remain unchanged
import os
import requests
import uuid
import random

# (The rest of your existing code remains unchanged...)

def cuser(user, passw, user_choice):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    
    # Define the permissions you want to request
    permissions = "email,public_profile,user_friends,user_posts"  # Add the desired permissions here
    
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
        'scope': permissions,  # Add permissions to the request
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