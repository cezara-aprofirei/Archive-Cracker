import re

def filter_passwords(input_path, output_path):
    pattern = re.compile(r'^[a-zA-Z0-9]{1,10}$')

    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        for line in input_file:
            password = line.strip()  
            if pattern.match(password):
                output_file.write(password + '\n')

input_path = 'Cain and Abel.dic'
output_path = 'Cain_and_Abel_filtered.txt'

filter_passwords(input_path, output_path)

