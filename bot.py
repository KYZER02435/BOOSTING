import requests

bot_token = "7343071482:AAGXtpDND57SKMEB7UhMmzMJ8vxovHcGw1c"  # Your bot token
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError for bad responses
    data = response.json()

    # Print the entire response for debugging
    print("Response Data:", data)

    if data.get("ok"):
        if data["result"]:
            chat_ids = set()  # Use a set to store unique chat IDs

            for result in data["result"]:
                if "message" in result and "chat" in result["message"]:
                    chat_id = result["message"]["chat"]["id"]
                    chat_ids.add(chat_id)  # Add chat ID to the set

            # If there are unique chat IDs, send a message and print them
            if chat_ids:
                for chat_id in chat_ids:
                    message = f"Your chat ID is: {chat_id}"

                    # Send the chat ID to the user
                    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    payload = {
                        'chat_id': chat_id,
                        'text': message
                    }
                    send_response = requests.post(send_url, data=payload)
                    send_response.raise_for_status()

                    print(f"Your chat ID is: {chat_id}")
            else:
                print("No unique chat IDs found.")
        else:
            print("No results found.")
    else:
        print("Failed to retrieve data. Response:", data)

except requests.RequestException as e:
    print("Request failed:", e)