import requests
import json
import time
import uuid
import base64
import re
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from rich import print

# Color definitions
r = "[bold red]"
g = "[bold green]"

# Thread-safe counter for successful reactions
successful_reactions = 0
counter_lock = threading.Lock()

def fetch_proxies():
    """Fetch proxies from ProxyScrape and return as a list."""
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1&country=all&ssl=all&anonymity=all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip().split('\n')
    except requests.exceptions.RequestException as e:
        print(f"{r}Failed to fetch proxies: {e}")
        return []

def get_random_proxy(proxies):
    """Get a random proxy from the list."""
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

def Reaction(actor_id: str, post_id: str, react: str, token: str, react_count: int) -> bool:
    """Send a reaction request."""
    global successful_reactions
    rui = requests.Session()
    user_agent = generate_user_agent()
    rui.headers.update({"User-Agent": user_agent})

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
        pos = rui.post('https://graph.facebook.com/graphql', data=data).json()
        if react == '0':
            print(f"{g}「Success」» Removed reaction from {actor_id} on {post_id}")
            return True
        elif react in str(pos):
            with counter_lock:
                if successful_reactions < react_count:
                    successful_reactions += 1
                    print(f"{g}「Success」» Reacted with {actor_id} to {post_id} ({successful_reactions}/{react_count})")
            return True
        else:
            print(f"{r}「Failed」» Reacted with {actor_id} to {post_id}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{r}Reaction failed due to an error: {e}")
        return False

def process_reaction(actor_id, token, post_id, react, react_count):
    """Process a reaction and stop when the target is reached."""
    global successful_reactions
    if successful_reactions < react_count:
        Reaction(actor_id, post_id, react, token, react_count)

def AutoReact():
    """Main function to handle auto-reactions."""
    def choose_reaction():
        print("Please choose the reaction you want to use.\n")
        reactions = {
            '1': 'Like',
            '2': 'Love',
            '3': 'Haha',
            '4': 'Wow',
            '5': 'Care',
            '6': 'Sad',
            '7': 'Angry',
            '8': 'Remove Reaction'
        }
        for key, value in reactions.items():
            print(f"     「{key}」 {value}")
        
        rec = input('Choose a reaction: ')
        reaction_ids = {
            '1': '1635855486666999',
            '2': '1678524932434102',
            '3': '115940658764963',
            '4': '478547315650144',
            '5': '613557422527858',
            '6': '908563459236466',
            '7': '444813342392137',
            '8': '0'
        }
        return reaction_ids.get(rec)

    def get_ids_tokens(file_path):
        """Retrieve IDs or tokens from a file."""
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    actor_ids = get_ids_tokens('/sdcard/TEST-BOOSTING/TOKENS.txt')
    tokens = get_ids_tokens('/sdcard/TEST-BOOSTING/IDS.txt')

    post_link = input('Enter the Facebook post link: ')
    post_id = re.search(r'/posts/(\w+)', post_link)
    if not post_id:
        print(f"{r}Invalid post link.")
        return
    post_id = post_id.group(1)

    react = choose_reaction()
    if react:
        react_count = int(input("How many successful reactions do you want to send? "))
        with ThreadPoolExecutor(max_workers=1) as executor:
            for actor_id, token in zip(actor_ids, tokens):
                executor.submit(process_reaction, actor_id, token, post_id, react, react_count)
                if successful_reactions >= react_count:
                    print(f"{g}Target of {react_count} successful reactions reached!")
                    break
    else:
        print(f"{r}Invalid reaction option.")

# Run the AutoReact script
AutoReact()
