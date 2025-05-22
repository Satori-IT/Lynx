import time
import secrets
import string
import re
from colorama import Fore, Style
import random
import hashlib
import requests
import os
import bcrypt
import base64
from cryptography.fernet import Fernet

version = "v1.4"
HIBP_API_URL = "https://api.pwnedpasswords.com/range/"

def pin_to_key(pin: str) -> bytes:
    pin_hash = hashlib.sha256(pin.encode()).digest()
    key = base64.urlsafe_b64encode(pin_hash)
    return key


print(f"Lynx {version}")
key = input("Enter your master-pass(leave blank if you dont have it): ")
if key == "":
    newkey = input("Enter a master-pass: ")

    key = pin_to_key(newkey)

    time.sleep(3)

    if os.path.exists('passwords.txt') : os.remove("passwords.txt")

else:
    key = pin_to_key(key) 


def generate_random_name(length):
    letters = string.ascii_lowercase
    rname = ''.join(random.choice(letters) for i in range(length))
    return rname


class lynx:

    def check_password():
        password = input(f"{Fore.CYAN}Enter password to check:{Style.RESET_ALL} ").strip()
        
        
        is_breached, count = lynx.check_hibp(password)
        
        
        strength = lynx.password_strength(password)
        strength_color = Fore.GREEN if strength == "strong" else Fore.RED
        
        print("\n" + "="*50)
        if is_breached is None:
            print(f"{Fore.YELLOW}⚠ Can't reach the API(API Error).{Style.RESET_ALL}")
        elif is_breached:
            print(f"{Fore.RED}⚠ Password found in {count} breaches!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ Password not found in breaches.{Style.RESET_ALL}")
        
        # print(f"Strength: {strength_color}{strength}{Style.RESET_ALL}") Non-working
        print("="*50 + "\n")
        input(f"{Fore.CYAN}Press enter to continue{Style.RESET_ALL}")

        menu()

    def check_hibp(password):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        
        try:
            time.sleep(1.5)
            response = requests.get(f"{HIBP_API_URL}{prefix}", timeout=5)
            response.raise_for_status()
            
            for line in response.text.splitlines():
                if line.startswith(suffix):
                    count = int(line.split(":")[1])
                    return True, count
            return False, 0
        except requests.RequestException:
            print(f"{Fore.RED}⚠ Error connecting to HIBP API.{Style.RESET_ALL}")
            return None, 0
        
    def password_strength(password):
        checks = [
            len(password) >= 10,
            re.search(r"\d", password),
            re.search(r"[a-z]", password),
            re.search(r"[A-Z]", password),
            re.search(r"[@#$%^&+=!]", password),
        ]
        return "strong" if all(checks) else "weak"

    def generator():
        print(Fore.MAGENTA + "_______________________________________________\nLynx Generator " + version + "\n_______________________________________________" + Style.RESET_ALL)
        pwd_length = int(input(Fore.MAGENTA + 'How many chars would you like to be in your password?\n' + Style.RESET_ALL))
        time.sleep(2)
    
        alphabet = string.ascii_letters + string.digits + string.punctuation
        pwd = ''.join(secrets.choice(alphabet) for _ in range(pwd_length))

        print(Fore.LIGHTGREEN_EX + "Generated password is : " + pwd + Style.RESET_ALL)
        input("Press enter to proceed...")

        menu()

    def encrypt(password):
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password.decode()

    def decrypt(encrypted_password):
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        return decrypted_password

    def keychain():
        if key != "":
            print(Fore.CYAN + "Welcome to Lynx keychain" + Style.RESET_ALL)
            choice = input(f"""
{Fore.MAGENTA}[1]{Style.RESET_ALL} Add password
{Fore.MAGENTA}[2]{Style.RESET_ALL} View your passwords
{Fore.MAGENTA}[3]{Style.RESET_ALL} Exit
{Fore.CYAN}> {Style.RESET_ALL}""")
    
            if choice == '1':
                userinput = input("Enter a website for the password that you would like to add: ")
                passinput = input("Enter password : ")
                encrypted_pass = lynx.encrypt(passinput)

                with open('passwords.txt', 'a') as f:
                    f.write(f"{userinput}:{encrypted_pass}\n")

        
                lynx.keychain()

            elif choice == '2':

                if not os.path.exists('passwords.txt'):
                    print("No passwords stored yet.")
            
                    lynx.keychain()
            
                with open('passwords.txt', 'r') as f:
                    for line in f:
                        parts = line.strip().split(':')
                        username = parts[0]
                        encrypted_password = parts[1]
                        decrypted_password = lynx.decrypt(encrypted_password)
                        print(f"Website: {username}, Password: {decrypted_password}")
                
                    input("Press any key to proceed")
            
                    lynx.keychain()
            elif choice == '3':
                menu()
            else:
                print("Invalid choice. Please try again.")
        
                lynx.keychain()
        else:
            print("Invalid key.")
            '''
            print(Fore.MAGENTA + "Work in progress..." + Style.RESET_ALL) 
            menu()
            '''
        
def menu():

    print(f"""
{Fore.MAGENTA}
 
 ▄█       ▄██   ▄   ███▄▄▄▄   ▀████    ▐████▀ 
███       ███   ██▄ ███▀▀▀██▄   ███▌   ████▀  
███       ███▄▄▄███ ███   ███    ███  ▐███    
███       ▀▀▀▀▀▀███ ███   ███    ▀███▄███▀    
███       ▄██   ███ ███   ███    ████▀██▄     
███       ███   ███ ███   ███   ▐███  ▀███    
███▌    ▄ ███   ███ ███   ███  ▄███     ███▄  
█████▄▄██  ▀█████▀   ▀█   █▀  ████       ███▄ 
▀                                             

{Style.RESET_ALL}
{Fore.CYAN}Version: {version}{Style.RESET_ALL}
{Fore.CYAN}Running OS : {os.name}{Style.RESET_ALL}""")
    
    gen = input(f"""
{Fore.MAGENTA}[1]{Style.RESET_ALL} Check password for breaches
{Fore.MAGENTA}[2]{Style.RESET_ALL} Generate a secure password
{Fore.MAGENTA}[3]{Style.RESET_ALL} Password manager
{Fore.MAGENTA}[4]{Style.RESET_ALL} Exit
{Fore.CYAN}> {Style.RESET_ALL}"""
    )
    if gen == '1':
        lynx.check_password()
    
    elif gen == '2':
        lynx.generator()
    
    elif gen == '3':
        lynx.keychain()
    
    elif gen == '4':
        exit()
    
    else:
        print('Input is invalid')
        menu()





menu()