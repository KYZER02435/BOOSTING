import requests
from datetime import datetime

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def has_replied(comment_id, access_token, user_id):
    try:
        url = f'https://graph.facebook.com/v18.0/{comment_id}/comments'
        params = {'access_token': access_token}
        response = requests.get(url, params=params)
        response.raise_for_status()
        replies = response.json().get('data', [])
        
        for reply in replies:
            if reply.get('from', {}).get('id') == user_id:
                return True
    except requests.exceptions.RequestException as error:
        print(f"Failed to check replies for comment {comment_id}")
    return False

def reply_to_comment_on_facebook(same_replies, num_replies):
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    comment_id = input('Enter the comment ID to reply to: ')
    
    if same_replies:
        reply_text = input('Enter the reply text (for all replies): ')
    else:
        reply_texts = [input(f'Enter reply text {i + 1}: ') for i in range(num_replies)]

    replies_count = 0
    commented_users = set()  # Track users who have commented

    for i in range(len(user_ids)):
        if replies_count >= num_replies:
            print(f"Successfully made {num_replies} replies.")
            return
        
        user_id = user_ids[i]
        access_token = access_tokens[i]

        if user_id in commented_users:
            continue  # Skip users who have already commented

        try:
            if not has_replied(comment_id, access_token, user_id):
                if same_replies:
                    text_to_use = reply_text
                else:
                    text_to_use = reply_texts[replies_count]  # Use different reply for each comment
                
                url = f'https://graph.facebook.com/v19.0/{comment_id}/comments'
                params = {'access_token': access_token, 'message': text_to_use}
                response = requests.post(url, params=params)

                if response.status_code == 200:
                    commented_users.add(user_id)  # Mark this user as having commented
                    replies_count += 1
                    print(f"Successfully replied to comment {comment_id}")
                else:
                    print(f"Failed to reply to comment {comment_id}")
        except requests.exceptions.RequestException as error:
            print(f"Failed to reply to comment {comment_id}")

    if replies_count < num_replies:
        print(f"Only {replies_count} replies were made.")

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Reply to a comment on Facebook")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Choose reply type:")
            print("1. Same Replies")
            print("2. Different Replies")
            reply_type = input("Enter your choice: ")

            if reply_type == '1':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=True, num_replies=num_replies)
            elif reply_type == '2':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=False, num_replies=num_replies)
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()