import requests
import re
from concurrent.futures import ThreadPoolExecutor

# Load tokens from the file
def get_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Function to get the profile ID using the token
def get_profile_id(access_token):
    try:
        url = 'https://graph.facebook.com/me'
        params = {'access_token': access_token}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json().get('id')
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Function to join the group using an access token and profile ID
def join_group(group_id, profile_id, access_token):
    try:
        url = f'https://graph.facebook.com/{group_id}/members/{profile_id}'
        params = {'access_token': access_token}
        response = requests.post(url, params=params)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Helper function to extract group ID from the URL or use it directly
def extract_group_id(input_value):
    match = re.search(r'/groups/(\d+)', input_value)
    if match:
        return match.group(1)
    return input_value

# Main function to join bots to the group
def auto_group_join(group_id, num_bots):
    access_tokens = get_tokens_from_file('/sdcard/Test/toka.txt')
    valid_tokens = [token for token in access_tokens if token.startswith("EA") or token.startswith("EAA")]
    
    join_count = 0
    failed_count = 0

    def join_task(access_token):
        nonlocal join_count, failed_count
        profile_id = get_profile_id(access_token)
        if profile_id:
            if join_group(group_id, profile_id, access_token):
                print(f"Success: Group ID {group_id}, User ID {profile_id}")
                join_count += 1
            else:
                print(f"Failed: Group ID {group_id}, User ID {profile_id}")
                failed_count += 1
        else:
            print("Failed: Invalid profile ID for token.")
            failed_count += 1

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(join_task, valid_tokens[:num_bots])

    print(f"\nSuccessfully joined {join_count} accounts to the group.")
    print(f"Failed to join {failed_count} accounts.")

# Input the group link or ID and extract the ID if necessary
group_input = input("Enter the Facebook group link or ID: ")
group_id = extract_group_id(group_input)

num_bots = int(input("Enter the number of Profiles to join: "))

# Call the main function
auto_group_join(group_id, num_bots)
