import requests
import threading
import time

def send_webhook_message(webhook_url, message_content):
    message = {
        "content": message_content
    }
    while True:
        response = requests.post(webhook_url, json=message)
        if response.status_code == 204:
            print("Message sent successfully!")
            break
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            print(f"Failed to send message: {response.status_code}")
            break

webhook_url = input("Enter your Discord webhook URL: ")
message_content = input("Enter the message you want to send: ")
num_requests = int(input("Enter the number of times to send the message: "))


threads = []
for i in range(num_requests):
    thread = threading.Thread(target=send_webhook_message, args=(webhook_url, message_content))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

print("All messages sent.")
