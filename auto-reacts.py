import requests, json, time, uuid, base64, re, threading, random
from rich import print
from concurrent.futures import ThreadPoolExecutor, as_completed

r = "[bold red]"
g = "[bold green]"

# Thread-safe counter for successful reactions
successful_reactions = 0
counter_lock = threading.Lock()

def generate_user_agent():
    fbav = f"{random.randint(100, 999)}.0.0.{random.randint(11, 99)}.{random.randint(100, 999)}"
    fbbv = random.randint(100000000, 999999999)
    fbca = random.choice(["armeabi-v7a:armeabi", "arm64-v8a:armeabi", "armeabi-v7a", "armeabi", "arm86-v6a", "arm64-v8a"])
    fban = "FB4A"
    fbpv = f"Windows NT {random.randint(10, 12)}.0"
    fbsv = f"{random.randint(10, 15)}.{random.randint(0, 5)}"
    return f"Dalvik/2.1.0 (Linux; U; {fbpv}; {fban} Build/{fbbv}) [FBAN/{fban};FBAV/{fbav};FBBV/{fbbv};FBCA/{fbca};FBSV/{fbsv}]"

def AutoReact():
    def Reaction(actor_id: str, post_id: str, react: str, token: str) -> bool:
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
            'method': 'post',
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

        pos = rui.post('https://graph.facebook.com/graphql', data=data).json()
        time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior
        try:
            if react == '0':
                print(f"{g}「Success」» Removed reaction from {actor_id} on {post_id}")
                return True
            elif react in str(pos):
                print(f"{g}「Success」» Reacted with » {actor_id} to {post_id}")
                return True
            else:
                print(f"{r}「Failed」» Reacted with » {actor_id} to {post_id}")
                return False
        except Exception:
            print(f"{r}Reaction failed due to an error.")
            return False

    def process_reaction(actor_id, token, post_id, react):
        global successful_reactions
        with counter_lock:
            if successful_reactions >= react_count:  # Stop further reactions if limit is reached
                return
        time.sleep(random.uniform(1, 3))  # Random delay before each reaction
        if Reaction(actor_id=actor_id, post_id=post_id, react=react, token=token):
            with counter_lock:
                if successful_reactions < react_count:
                    successful_reactions += 1

    # Rest of your unchanged code...

    actor_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    choice = choose_type()
    
    if choice == '1':
        post_link = input('Enter the Facebook post link: ')
        post_id = linktradio(post_link)
    elif choice == '2':
        post_link = input('Enter the Facebook group post link: ')
        post_id = linktradio(post_link)
    elif choice == '3':
        post_link = input('Enter the Facebook video post link: ')
        post_id = linktradio(post_link)
    elif choice == '4':
        post_link = input('Enter the Facebook photo post link: ')
        post_id = linktradio(post_link)
    else:
        print('Invalid choice.')
        return

    if not post_id:
        return
    
    react = choose_reaction()
    if react:
        global react_count  # Declare react_count as global to track its usage
        react_count = int(input("How many reactions do you want to send? "))
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(process_reaction, actor_id, token, post_id, react)
                for actor_id, token in zip(actor_ids, tokens)
            ]

            for future in as_completed(futures):
                if successful_reactions >= react_count:  # Exit early if limit is reached
                    break
                future.result()

        print(f"[bold green]{successful_reactions} successful reactions sent! You're awesome![/bold green]")
    else:
        print('[bold red]Invalid reaction option.[/bold red]')

# Run the AutoReact script
AutoReact()
