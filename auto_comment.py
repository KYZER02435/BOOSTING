import requests
from datetime import datetime

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def linktradio(post_link):
    # Function to extract post ID from the link
    # Assuming you have the implementation, add it here
    pass

def get_user_name():
    # Function to get the user name, add your own logic here
    return "User"

def comment_on_facebook_post():
    # Load user IDs and access tokens
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    
    # Choose comment option: same or different comments
    comment_option = input('Choose comment option:\n1. Same comments\n2. Different comments\nEnter option (1 or 2): ')
    
    # Enter the number of comments
    num_comments = int(input('Enter the number of comments to make: '))
    
    # Enter the post link
    post_link = input('Enter the Facebook post link: ')
    post_id = linktradio(post_link)
    
    # Handle same or different comments logic
    if comment_option == '1':  # Same comments
        comment_text = input('Enter the comment text (or leave blank for auto comment): ')
        if not comment_text:
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%Y-%m-%d")
            user_name = get_user_name()
            comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
        comment_texts = [comment_text] * num_comments  # Same comment repeated
        
    elif comment_option == '2':  # Different comments
        comment_texts = []
        for _ in range(num_comments):
            comment_text = input(f'Enter comment {_ + 1}: ')
            if not comment_text:
                current_time = datetime.now().strftime("%I:%M %p")
                current_date = datetime.now().strftime("%Y-%m-%d")
                user_name = get_user_name()
                comment_text = f'Time:「{current_time}」「{current_date}」\n-「Auto comment by {user_name}」'
            comment_texts.append(comment_text)  # Add each comment individually

    # Function to check if a user has already commented
    def has_commented(post_id, access_token, user_id):
        try:
            url = f'https://graph.facebook.com/v18.0/{user_id}_{post_id}/comments'
            params = {'access_token': access_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            comments = response.json().get('data', [])
            
            for comment in comments:
                if comment.get('from', {}).get('id') == user_id:
                    return True
        except requests.exceptions.RequestException as error:
            print(f"Failed to comment on {post_id}")
        return False

    # Start commenting process
    comments_count = 0
    user_count = len(user_ids)

    for i in range(num_comments):
        for j in range(user_count):
            user_id = user_ids[j]
            access_token = access_tokens[j]
            comment_text = comment_texts[i]  # Use appropriate comment based on the loop
            
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
                        print(f"Failed to comment on {post_id}")
            except requests.exceptions.RequestException as error:
                print(f"Failed to comment on {post_id}")

# Run the function
comment_on_facebook_post()