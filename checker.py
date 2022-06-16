import easygui
import json
import requests
import os
from datetime import datetime


files = easygui.fileopenbox(msg="Select tokens", title=None, default='*', filetypes=None, multiple=True)

tokens = []

def get_headers(token, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",      
    }   
    if token:
        headers.update({"Authorization": token})
    return headers

def get_details(token):
    data = requests.get('https://discordapp.com/api/users/@me', headers=get_headers(token))
    return json.loads(data.text)

def get_payment(token):
    data = requests.get("https://discordapp.com/api/users/@me/billing/payment-sources", headers=get_headers(token))
    data2 = len(json.loads(data.text))
    return bool(data2)

def save_tokens(tokens, name):
    date = datetime.now().strftime("%Y-%m-%d %H;%M;%S")
    path = f"tokens/{date}/{name}.txt"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'a') as f:
        f.write('\n'.join(tokens) + '\n')


invalid = 0
valid = []
emailverified = []
mobileverified = []
billing = []
nitroclassic = []
nitro = []

def print_thing():
    os.system('cls')
    print("Invalid: ", invalid)
    print("Valid: ", len(valid))
    print("Mobile verified", len(mobileverified))
    print("Email verified: ", len(emailverified))
    print("Billing: ", len(billing))
    print("Nitro classic: ", len(nitroclassic))
    print("Nitro: ", len(nitro))

for file in files:
    f = open(file, "r")
    for line in f.readlines():
        tokens.append(line.strip('\n'))

def check_token(token):
    global invalid

    if token in valid:
        return

    details = get_details(token)
    try:
        if details['message'] == '401: Unauthorized':
            invalid += 1
            return
    except KeyError:
        pass

    valid.append(token)
    
    if details['verified']:
        emailverified.append(token)

    if details['phone']:
        mobileverified.append(token)
    try:
        if details['premium_type'] == 1:
            nitroclassic.append(token)
        elif details['premium_type'] == 2:
            nitro.append(token)
    except KeyError:
        pass
    
    if get_payment(token):
        billing.append(token)

for token in tokens:
    check_token(token)
    print_thing()
    
if valid:
    save_tokens(valid, "valid")
if emailverified:
    save_tokens(emailverified, "emailverified")
if mobileverified:
    save_tokens(mobileverified, "mobileverified")
if billing:
    save_tokens(billing, "billing")
if nitroclassic:
    save_tokens(nitroclassic, "nitroclassic")
if nitro:
    save_tokens(nitro, "nitro")

input("\nSaved all tokens.")

