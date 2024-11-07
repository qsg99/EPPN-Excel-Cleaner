
import numpy as np
import pandas as pd

import os.path


check_path = #Add the filepath of the original file here


df = pd.read_csv(check_path)

strings = df.screenLabel



def process_text(s):
    word_list = s.split(' ')
    dict = {}
    current_value = ''
    current_key = ''
    for i, word in enumerate(word_list):
        word = word.strip()
        
        if word[-1] == ':':
            if len(current_key) > 0:
                dict[current_key] = current_value
                current_value = ''
                current_key = word[ : len(word)-1]
            else:
                current_key = word[ : len(word)-1]
        elif i < len(word_list) - 1:
            if len(current_value) > 0:
                current_value = current_value + ' ' + word
            else:
                current_value = current_value + word
        else:
            if len(current_value) > 0:
                current_value = current_value + ' ' + word
                dict[current_key] = current_value

            else:
                current_value = current_value + word
                dict[current_key] = current_value
    return dict


dict_list = []
for string in strings:
    result = process_text(string)
    dict_list.append(result)

df = pd.DataFrame.from_dict(dict_list)
df[['FirstName', 'LastName']] = df['Name'].str.split(' ', n = 1, expand = True)

df.drop(['Name', 'HUID', 'NETID', 'HKey'], axis = 1, inplace = True)
df.rename(columns={'EPPN': 'ExternalDataReference'}, inplace=True)
df = df[['FirstName', 'LastName', 'Email', 'ExternalDataReference']]



write_path = #Add the filepath of where you'd like to create the correctly formatted file here

if not os.path.isfile(write_path):
    df.to_excel(write_path)
print('Done!') 
