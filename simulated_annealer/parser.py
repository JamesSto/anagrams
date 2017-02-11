import os

def parse_data(directory):
    '''Takes in a directory, parses all files in that directory and returns them as a list of strings'''
    data = []
    for path,_,files in os.walk(directory):
        for file_name in files:
            with open(path + "/" + file_name, 'r') as f:
                s = f.read()
                s = s.split()
                s = [word for word in s if word.isalpha()]
                s = " ".join(s)
                s = s.lower()
                data.append(s)
    return data