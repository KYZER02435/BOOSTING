import requests, json, time, uuid, base64, re, random
from rich import print

r = "[bold red]"
g = "[bold green]"

# Thread-safe counter for successful reactions
successful_reactions = 0

def generate_user_agent():
    fbav = f"{random.randint(100, 999)}.0.0.{random.randint(11, 99)}.{random.randint(100, 999)}"
    fbbv = random.randint(100000000, 999999999)
    fbca = random.choice(["armeabi-v7a:armeabi", "arm64-v8a:armeabi", "armeabi-v7a", "armeabi", "arm86-v6a", "arm64-v8a"])
    fban = "FB4A"
    fbpv = f"Windows NT {random.randint(10, 12)}.0"
    return f"Dalvik/2.1.0 (Linux; U; {fbpv}; {fban} Build/{fbbv}) [FBAN/{fban};FBAV/{fbav};FBBV/{fbbv};FBCA/{fbca}]"

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

        try:
            pos = rui.post('https://graph.facebook.com/graphql', data=data).json()
            if react == '0':
                print(f"{g}「Success」» Removed reaction from {actor_id} on {post_id}")
                return True
            elif react in str(pos):
                print(f"{g}「Success」» Reacted with » {actor_id} to {post_id}")
                return True
            else:
                print(f"{r}「Failed」» Reacted with » {actor_id} to {post_id}")
                return False
        except json.JSONDecodeError as e:
            print(f"{r}JSONDecodeError: {e}")
        except requests.exceptions.RequestException as e:
            print(f"{r}RequestException: {e}")
        except Exception as e:
            print(f"{r}An unexpected error occurred: {e}")
        return False

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

    def get_ids_tokens(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    def choose_type():
        print("Do you want to react to:")
        print("1. A regular post")
        print("2. A group post")
        print("3. A video post")
        print("4. A photo post")
        choice = input('Choose an option: ')
        return choice

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
        react_count = int(input("How many reactions do you want to send? "))
        successful_reactions = 0  # Reset the counter
        
        for actor_id, token in zip(actor_ids, tokens):
            if successful_reactions >= react_count:
                break
            if Reaction(actor_id=actor_id, post_id=post_id, react=react, token=token):
                successful_reactions += 1
                # Adding a human-like delay between reactions
                time.sleep(random.uniform(1, 3))  # Simulating a random delay between 1 and 3 seconds

        print(f"[bold green]{successful_reactions} successful reactions sent! You're awesome![/bold green]")
    else:
        print('[bold red]Invalid reaction option.[/bold red]')

# Run the AutoReact script
AutoReact()
