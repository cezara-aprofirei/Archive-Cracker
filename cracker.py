import zipfile
import time
import os

class ZipCracker:
    def __init__(self, zip_path):
        self.zip_path = zip_path  
        self.zip_file = None  
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = None

    def validate_zip(self):
        try:
            if not os.path.exists(self.zip_path):
                print(f"Error: The path '{self.zip_path}' does not exist.")
                return False
            elif not os.path.isfile(self.zip_path):
                print(f"Error: The path '{self.zip_path}' is not a file.")
                return False
            elif not zipfile.is_zipfile(self.zip_path):
                print(f"Error: The file '{self.zip_path}' is not a valid zip file.")
                return False

            self.zip_file = zipfile.ZipFile(self.zip_path)  
            return True
        except FileNotFoundError:
            print("Fișierul ZIP nu a fost găsit.")
            return False
        except zipfile.BadZipFile:
            print("Fișierul specificat nu este o arhivă validă.")
            return False
    
    def attempt_password(self, password):
        try:
            print(f"Trying password: {password}")
            self.zip_file.extractall(pwd=password.encode('utf-8'))
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
                            elapsed_time = self.stop_time - self.start_time
                            return f"Found it! The password is -> {password}\nTime taken: {elapsed_time:.2f} seconds"
            except FileNotFoundError:
                return f"Error: Dictionary file '{dictionary_path}' not found."

            self.stop_time = time.time()  
            elapsed_time = self.stop_time-self.start_time
            return f"Couldn't find the password in the dictionary.\nTime taken: {elapsed_time:.2f} seconds"
        
    
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
    