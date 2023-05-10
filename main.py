# Before you start, make a file called "tokens.txt" and enter your tokens there.
# Remember to put the file in this directory.

# Importing libs
from colorama import Fore, init
import requests
import threading
import time
import ctypes
import re
import sys

init(autoreset=True)

print(Fore.BLUE + """

████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗     █████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ██████╗ ██╗███████╗███████╗██████╗ 
╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██║╚══███╔╝██╔════╝██╔══██╗
   ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    ███████║██║   ██║   ██║   ███████║██║   ██║██████╔╝██║  ███╔╝ █████╗  ██████╔╝
   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ██╔══██║██║   ██║   ██║   ██╔══██║██║   ██║██╔══██╗██║ ███╔╝  ██╔══╝  ██╔══██╗
   ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║    ██║  ██║╚██████╔╝   ██║   ██║  ██║╚██████╔╝██║  ██║██║███████╗███████╗██║  ██║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
              
» Made by Plexus                                                                                                                
""")

auth_url = input(Fore.LIGHTCYAN_EX+"Enter the Discord OAuth2 link: ")
reg = r"^https:\/\/discord\.com\/api\/oauth2\/authorize\?client_id=\d+&redirect_uri=http%3A%2F%2F[a-z0-9.-]+%2F[a-z0-9.-]+&response_type=code&scope=[a-z.%20]+&state=%7B%22guild%22%3A%22\d+%22%2C%22bot%22%3A%22\d+%22%7D$"

if not re.match(reg, auth_url):
    sys.exit("Invalid link")

count = 0
genStartTime = time.time()


def title():
    ctypes.windll.kernel32.SetConsoleTitleW(f'Plexus Token to Auth | Authorized: {count} Speed : {round(count / ((time.time() - genStartTime) / 60))}/m')


# Headers

def get_headers(token):
    headers = {
                "accept": "/",
                # "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "authorization": token,
                "referer": "https://discord.com/channels/@me",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9007 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDA3Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTYxODQyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    return headers


# Authing the tokens

def auth(token):
    global count
    while True:
        try:
            headers = get_headers(token)
            r = requests.post(auth_url, headers=headers, json={"authorize": "true"})

            if r.status_code in (200, 201, 204):
                if 'location' in r.text:
                    location = r.json()['location']
                    requests.get(location)
                    print(count, Fore.GREEN, f"[Success]: Successfully Authorized:", token[:22])
                    count += 1
                    title()
                    break

                else:
                    print(Fore.LIGHTRED_EX + f"[ERROR] Failed", token, r.text)
                    break
            else:
                print(Fore.LIGHTRED_EX + f"[ERROR] Failed", token, r.text)
                break
        except Exception as e:
            print(Fore.YELLOW + f"[ERROR]: Failed to Authorize:", token, e)
            if "connection" in str(e):
                time.sleep(1)
                continue
            else:
                break

file = open("tokens.txt", "r").readlines()

for token in file:
    token = token.strip()
    token = token.split(":")
    time.sleep(0.01)
    threading.Thread(target=auth, args=(token)).start()


