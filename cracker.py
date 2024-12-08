import zipfile
import time
import string
import random
from concurrent.futures import ThreadPoolExecutor
import threading

class ZipCracker:
    def __init__(self, zip_path):
        self.zip_path = zip_path  
        self.zip_file = None  
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = None
        self.found_event = threading.Event()
        self.password = None
        self.charset = string.ascii_letters + string.digits

    def validate_zip(self):
        try:
            self.zip_file = zipfile.ZipFile(self.zip_path)  
            return True
        except FileNotFoundError:
            print("Couldn't find ZIP file. Check that the path is valid.")
            return False
        except zipfile.BadZipFile:
            print("The file provided is not a valid ZIP file.")
            return False
    
    def attempt_password(self, password):
        if self.found_event.is_set():
            return False  
        
        try:
            print(f"Trying password: {password}")
            self.zip_file.extractall(pwd=password.encode('utf-8'))
            self.password=password
            self.found_event.set()
            return password
        except (RuntimeError, zipfile.BadZipFile):
            return False
    
    def dictionary_attack(self, dictionary_path="Cain_and_Abel_filtered.txt"):
            self.start_time = time.time()  
            try:
                with open(dictionary_path, 'r') as input_file:
                    for line in input_file:
                        password = line.strip()
                        if self.attempt_password(password):
                            self.stop_time = time.time()  
                            self.elapsed_time = self.stop_time - self.start_time
                            self.password=password
                            return f"Found it! The password is -> {self.password}\nTime taken: {self.elapsed_time:.2f} seconds"
            except FileNotFoundError:
                return f"Error: Dictionary file '{dictionary_path}' not found."

            self.stop_time = time.time()  
            self.elapsed_time = self.stop_time-self.start_time
            return f"Couldn't find the password in the dictionary.\nTime taken: {self.elapsed_time:.2f} seconds"

    def random_brute_force(self):
        self.start_time = time.time()

        password_length = int(input("Enter the initial length of the password you want to try: "))
        last_prompt_time = time.time()

        def generate_random_password(length):
            return ''.join(random.choice(self.charset) for _ in range(length))

        print(f"Testing passwords of length {password_length}...")
        while True:  
            current_time = time.time()
            if current_time - last_prompt_time >= 15:
                user_choice = input("\n15 seconds have passed. Do you want to keep trying with the current password length, change the length, or stop? (keep/change/stop): ").strip().lower()
                if user_choice == 'change':
                    new_length = int(input("Enter the new length of the password you want to try: "))
                    password_length = new_length
                    last_prompt_time = time.time()
                    print(f"Changed to passwords of length {password_length}...")
                elif user_choice == 'stop':
                    print("Stopping the brute force attempt...")
                    self.stop_time = time.time()
                    self.elapsed_time = self.stop_time - self.start_time
                    return f"Brute force attempt stopped. Time taken: {self.elapsed_time:.2f} seconds"
                else:
                    last_prompt_time = time.time()
                    print("Continuing with current password length...")

            password = generate_random_password(password_length)
            if self.attempt_password(password):
                self.stop_time = time.time()
                self.elapsed_time = self.stop_time - self.start_time
                return f"Found it! The password is -> {password}\nTime taken: {self.elapsed_time:.2f} seconds"

    def generate_passwords_by_length(self, charset, length):
        def recursive_generate(current_password, remaining_length):
            if remaining_length == 0:
                yield current_password
            else:
                for char in charset:
                    yield from recursive_generate(current_password + char, remaining_length - 1)

        return recursive_generate("", length)
    
    def iterative_brute_force(self):
        max_length = 10  
        self.start_time = time.time()  

        for length in range(1, max_length + 1):
            print(f"Testing passwords of length {length}...")
            for password in self.generate_passwords_by_length(self.charset, length):
                    if self.attempt_password(password):
                        self.stop_time = time.time()  
                        self.elapsed_time = self.stop_time - self.start_time
                        return f"Found it! The password is -> {password}\nTime taken: {self.elapsed_time:.2f} seconds"

        self.stop_time = time.time()  
        self.elapsed_time = self.stop_time-self.start_time
        return f"Couldn't find the password.\nTime taken: {self.elapsed_time:.2f} seconds"
    
    def iterative_brute_force_with_paralelism(self):
        max_length = 10
        self.start_time = time.time()

        try:
            with ThreadPoolExecutor(max_workers=800) as executor:
                for length in range(1, max_length + 1):
                    if self.found_event.is_set():  
                        break

                    print(f"Testing passwords of length {length}...")
                    passwords = list(self.generate_passwords_by_length(self.charset, length))
                    futures = {executor.submit(self.attempt_password, pwd): pwd for pwd in passwords}

                    for future in futures:
                        if self.found_event.is_set():  
                            break
                        try:
                            results = future.result(timeout=0.1)  
                            if results:
                                self.stop_time = time.time()
                                self.elapsed_time = self.stop_time - self.start_time
                        except Exception:
                            pass  
        finally:
            self.stop_time = time.time()
            self.elapsed_time = self.stop_time - self.start_time
            if self.password :
                return f"Found it! The password is -> {self.password}\nTime taken: {self.elapsed_time:.2f} seconds"
            return f"Couldn't find the password.\nTime taken: {self.elapsed_time:.2f} seconds"

    
if __name__ == "__main__":
    path_to_zip = input("Enter the path to the archive you want to crack: ")
    cracker = ZipCracker(path_to_zip)

    while not cracker.validate_zip():
        path_to_zip = input("New path : ")
        cracker = ZipCracker(path_to_zip)

    crack_method = int(input("What method would you like to use? Enter the number :\nBrute force attack-> 1\nDictionary attack -> 2\nMethod : "))
    if crack_method not in {1,2}:
        print("Invalid method number!\n")
        crack_method = int(input("Method: "))

    if crack_method == 2:
        print(cracker.dictionary_attack())
    
    if crack_method == 1:
        variant = int(input("Choose your flavour of brute force :\n Random choice brute force -> 1\n Iterative choice brute force -> 2\n Iterative choice brute force with paralelism -> 3\nYour choice : "))
        if variant not in range(1, 4) :
            print("Ivalid choice number!\n")
            variant = int(input("New choice : "))
        if variant == 1:
            print(cracker.random_brute_force())
        elif variant == 2:
            print(cracker.iterative_brute_force())
        elif variant == 3:
            print(cracker.iterative_brute_force_with_paralelism())