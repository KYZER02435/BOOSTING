import requests
import json
import time
import uuid
import base64
import re
import random
from rich import print

# Color definitions
r = "[bold red]"
g = "[bold green]"

successful_reactions = 0

def fetch_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=100&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip().split('\n')
    except requests.exceptions.RequestException as e:
        print(f"{r}Failed to fetch proxies: {e}")
        return []

def get_random_proxy(proxies):
    if proxies:
        return random.choice(proxies)
    return None

def generate_user_agent():
    fbav = f"{random.randint(100, 999)}.0.0.{random.randint(11, 99)}.{random.randint(100, 999)}"
    fbbv = random.randint(100000000, 999999999)
    fbca = random.choice(["armeabi-v7a:armeabi", "arm64-v8a:armeabi", "armeabi-v7a", "armeabi", "arm86-v6a", "arm64-v8a"])
    fban = "FB4A"
    fbpv = f"Windows NT {random.randint(10, 12)}.0"
    return f"Dalvik/2.1.0 (Linux; U; {fbpv}; {fban} Build/{fbbv}) [FBAN/{fban};FBAV/{fbav};FBBV/{fbbv};FBCA/{fbca}]"

def Reaction(actor_id: str, post_id: str, react: str, token: str) -> bool:
    rui = requests.Session()
    user_agent = generate_user_agent()
    rui.headers.update({"User-Agent": user_agent})

    proxy = get_random_proxy(fetch_proxies())
    if proxy:
        rui.proxies.update({
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        })

    feedback_id = str(base64.b64encode(f'feedback:{post_id}'.encode('utf-8')).decode('utf-8'))
    var = {
        "input": {
            "feedback_referrer": "native_newsfeed",
            "tracking": [None],
            "feedback_id": feedback_id,
            "client_mutation_id": str(uuid.uuid4()),
            "nectar_module": "newsfeed_ufi",
            "feedback_source": "native_newsfeed",
            "feedback_reaction_id": react,
            "actor_id": actor_id,
            "action_timestamp": str(time.time())[:10]
        }
    }
    data = {
        'access_token': token,
        'pretty': False,
        'format': 'json',
        'server_timestamps': True,
        'locale': 'id_ID',
        'fb_api_req_friendly_name': 'ViewerReactionsMutation',
        'fb_api_caller_class': 'graphservice',
        'client_doc_id': '2857784093518205785115255697',
        'variables': json.dumps(var),
        'fb_api_analytics_tags': ["GraphServices"],
        'client_trace_id': str(uuid.uuid4())
    }

    try:
        pos = rui.post('https://graph.facebook.com/graphql', data=data)
        response_text = pos.text  # Capture raw response for debugging
        pos = pos.json()  # Parse response as JSON

        if react == '0':
            print(f"{g}「Success」» Removed reaction from {actor_id} on {post_id}")
            return True
        elif react in str(pos):
            print(f"{g}「Success」» Reacted with » {actor_id} to {post_id}")
            return True
        else:
            print(f"{r}「Failed」» Reacted with » {actor_id} to {post_id}")
            return False
    except ValueError as json_error:
        print(f"{r}Reaction failed: Could not parse response. Raw response: {response_text}")
        return False
    except requests.exceptions.RequestException as req_error:
        print(f"{r}Reaction failed due to an error: {req_error}")
        return False
