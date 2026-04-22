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
    password = "wrongpassword"
    
    print(f"[*] Testing {username}:{password}")
    response = attempt_login(username, password)

    print(f"[*] Status code: {response.status_code}")
    print(f"[*] Response body: {response.text}")

if __name__ == "__main__":
    main()