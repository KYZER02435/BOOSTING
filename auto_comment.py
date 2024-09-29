import requests
from datetime import datetime

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def linktradio(post_link):
    try:
        # Extract the post ID from the link
        post_id = post_link.split('/posts/')[1].split('/')[0]
        return post_id
    except IndexError:
        print("Invalid post link.")
        return None

def get_user_name():
    return "User"

def comment_on_facebook_post():
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    comment_option = input('Choose comment option:\n1. Same comments\n2. Different comments\nEnter option (1 or 2): ')
    num_comments = int(input('Enter the number of comments to make: '))
    post_link = input('Enter the Facebook post link: ')
    post_id = linktradio(post_link)

    if post_id is None:
        print("Could not extract post ID. Exiting.")
        return

    if comment_option == '1':
        comment_text = input('Enter the comment text (or leave blank for auto comment): ')
        if not comment_text:
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%Y-%m-%d")
            user_name = get_user_name()
            comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
        comment_texts = [comment_text] * num_comments
        
    elif comment_option == '2':
        comment_texts = []
        for _ in range(num_comments):
            comment_text = input(f'Enter comment {_ + 1}: ')
            if not comment_text:
                current_time = datetime.now().strftime("%I:%M %p")
                current_date = datetime.now().strftime("%Y-%m-%d")
                user_name = get_user_name()
                comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
            comment_texts.append(comment_text)

    def has_commented(post_id, access_token, user_id):
        try:
            url = f'https://graph.facebook.com/v18.0/{user_id}_{post_id}/comments'
            params = {'access_token': access_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            comments = response.json().get('data', [])
            print("Comments fetched:", comments)  # Debugging line
            
            for comment in comments:
                if comment.get('from', {}).get('id') == user_id:
                    return True
        except requests.exceptions.RequestException as error:
            print(f"Error checking comments: {error}")
        return False

    comments_count = 0
    user_count = len(user_ids)

    for i in range(num_comments):
        for j in range(user_count):
            user_id = user_ids[j]
            access_token = access_tokens[j]
            comment_text = comment_texts[i]
            
            try:
                if not has_commented(post_id, access_token, user_id):
                    url = f'https://graph.facebook.com/v19.0/{user_id}_{post_id}/comments'
                    params = {'access_token': access_token, 'message': comment_text}
                    response = requests.post(url, params=params)
                    
                    if response.status_code == 200:
                        comments_count += 1
                        print(f"Success: commented on {post_id}")
                        if comments_count >= num_comments:
                            print(f"Successfully commented {num_comments} times.")
                            return
                    else:
                        print(f"Error {response.status_code}: {response.json()}")
            except requests.exceptions.RequestException as error:
                print(f"Failed to comment on {post_id}: {error}")

comment_on_facebook_post()
