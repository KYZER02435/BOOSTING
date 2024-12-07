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
    return f"Dalvik/2.1.0 (Linux; U; {fbpv}; {fban} Build/{fbbv}) [FBAN/{fban};FBAV/{fbav};FBBV/{fbbv};FBCA/{fbca}]"

def get_ids_tokens(file_path):
    """
    Reads actor IDs or tokens from a file.
    Each line in the file should contain one ID or token.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{r}Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"{r}Error reading file: {e}")
        return []

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
        if successful_reactions >= react_count:
            return  # Stop processing if successful reactions reach the limit
        if Reaction(actor_id=actor_id, post_id=post_id, react=react, token=token):
            with counter_lock:
                if successful_reactions < react_count:
                    successful_reactions += 1

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

    def linktradio(post_link: str) -> str:
        patterns = [
            r'/posts/(\w+)',
            r'/videos/(\w+)',
            r'/groups/(\d+)/permalink/(\d+)',
            r'/reels/(\w+)',
            r'/live/(\w+)',
            r'/photos/(\w+)',
            r'/permalink/(\w+)',
            r'story_fbid=(\w+)',
            r'fbid=(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, post_link)
            if match:
                if pattern == r'/groups/(\d+)/permalink/(\d+)':
                    return match.group(2)
                return match.group(1)
        
        print("Invalid post link or format")
        return None

    actor_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    post_link = input('Enter the Facebook post link: ')
    post_id = linktradio(post_link)
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
                future.result()

        print(f"{g}{successful_reactions} successful reactions sent! You're awesome![/bold green]")
    else:
        print(f"{r}Invalid reaction option.[/bold red]")

# Run the AutoReact script
AutoReact()
