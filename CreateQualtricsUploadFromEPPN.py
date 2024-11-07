
import numpy as np
import pandas as pd

import os.path

#Create Dataframe from raw data
check_path = #Add the filepath of the original file here
df = pd.read_csv(check_path)

#Grab the raw data from the "screenLabel" column
strings = df.screenLabel

#Converts every screenLabel string into a dictionary with correct attributes
def process_text(s):

    #Split line of text into words based on spaces
    word_list = s.split(' ')
    dict = {}

    #Variables that will find keys and values from the list of words
    current_value = ''
    current_key = ''
    
    for i, word in enumerate(word_list):
        
        word = word.strip()

        #If the word ends in :, this is a new key for the dictionary
        if word[-1] == ':':

            #if we already have a stored key, add the current key-value pair, and then update current_key
            if len(current_key) > 0:
                dict[current_key] = current_value
                current_value = ''
                current_key = word[ : len(word)-1]

            #if this is the first found key, store it in current_key
            else:
                current_key = word[ : len(word)-1]

        #If the word does not end in :, it should be added to the current value for the current key
        elif i < len(word_list) - 1:

            #If the current value is empty, add current word. Else, add a space and the current word
            if len(current_value) > 0:
                current_value = current_value + ' ' + word
            else:
                current_value = current_value + word

        #If we've found the last word in the entire line, add it to current value, and add current key-value pair
        else:
            if len(current_value) > 0:
                current_value = current_value + ' ' + word
                dict[current_key] = current_value

            else:
                current_value = current_value + word
                dict[current_key] = current_value
                
    #return completed dictionary
    return dict

#create a dictionary from every line of text in raw data and add it to dict_list
dict_list = []
for string in strings:
    result = process_text(string)
    dict_list.append(result)

#create new DataFrame from dict_list
df = pd.DataFrame.from_dict(dict_list)

#Extract First and Last name from Name column
df[['FirstName', 'LastName']] = df['Name'].str.split(' ', n = 1, expand = True)

#Remove unnecessary columns
df.drop(['Name', 'HUID', 'NETID', 'HKey'], axis = 1, inplace = True)

#Rename EPPN Column
df.rename(columns={'EPPN': 'ExternalDataReference'}, inplace=True)

#Put columns in proper order
df = df[['FirstName', 'LastName', 'Email', 'ExternalDataReference']]



write_path = #Add the filepath of where you'd like to create the correctly formatted file here

#Create new file - check that we are not overwriting another file
if not os.path.isfile(write_path):
    df.to_excel(write_path)
else:
    print('That file already exists')
print('Done!') 
