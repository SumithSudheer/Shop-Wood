import requests

api_url = 'https://api.whatsapp.com/v1/messages'
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

data = {
    'to': 'whatsapp:+91 9562313456',
    'message': 'Hello, this is a test message from my business.'
}

response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 200:
    print('Message sent successfully.')
else:
    print('Error: {}'.format(response.text))




import requests

url = 'https://graph.facebook.com/v15.0/113400621655857/messages'

data = {
    "messaging_product": "whatsapp",
    "to": 919562313456,
    "type": "text",
    "text": { "body": f"your password is "}
}

access_token = 'EAAM5MkoZCiS0BABz6T1lfhU7wr5PwIvznxnQv2v4wvSN0t7DLfHigOPrOnVkkT2JO8n8SNUvfscRbl6cYE0fgtipvtPJe5wfmT7fCLA3WC0hY1iJJHBb1rqGnXUrtTQF2BtlsvpShVAGuHIDtsSi9kNu6JcBCCQsT7biOvV1Ri3c1FtwMyEM4EN8xMibX0P1RylqynQZDZD'
headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)

print(response.json())



#29/01/2023
import requests

# Replace YOUR_ACCESS_TOKEN with your actual access token
access_token = 'EAAM5MkoZCiS0BACgnBVosQJvfwGbeBDgrLaVRLr5vM8z5flxOGR2ZCWQHgVnE2I4yxM7J6aNgSZANxdk6EGd3uYv8JJvbTqvLamfLaKlLhomyrPGYbncRYkjhn252Rx8LpGKpgp9zmLZAz0Rb3IoglZBcgS95i418VgBzQzNSUNs9trp7gk6WfeS7sv3JeB38bmqOb454YwZDZD'

# Replace YOUR_PHONE_NUMBER with the phone number you want to send the message to
phone_number = '+91 62384 10392'

# Replace YOUR_MESSAGE with the message you want to send
message = 'YOUR_MESSAGE hello kareem'

headers = {
    'Authorization': 'Bearer ' + 'EAAM5MkoZCiS0BACgnBVosQJvfwGbeBDgrLaVRLr5vM8z5flxOGR2ZCWQHgVnE2I4yxM7J6aNgSZANxdk6EGd3uYv8JJvbTqvLamfLaKlLhomyrPGYbncRYkjhn252Rx8LpGKpgp9zmLZAz0Rb3IoglZBcgS95i418VgBzQzNSUNs9trp7gk6WfeS7sv3JeB38bmqOb454YwZDZD',
    'Content-Type': 'text'
}

data = {
    'messaging_product': 'whatsapp',
    'to': 919562313456,
    "type": "text",
    "text": {
        "content": "Hello, this is a text message."
    }
}

response = requests.post('https://graph.facebook.com/v15.0/113400621655857/messages', headers=headers, json=data)

print(response.json())
