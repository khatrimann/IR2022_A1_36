# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 21:13:14 2022

@author: Mann
"""

# Importing required libraries
import os
import re
import ftfy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
from copy import deepcopy

# set of stopwirds to be removed
stopwords = set(stopwords.words("english"))

# Empty Dictionary to store word and file indices
indices = {}
file_indices = {}

# Lemma init
lemmatizer = WordNetLemmatizer()

# Path to dataset
path = "C:\\Users\\Mann\\Downloads\\Humor,Hist,Media,Food\\"

# Listing files
files = os.listdir(path)

# calculating total files
total_files = len(files)
all_files_idx = set(list(range(total_files)))

# check if the word is in the indices else return -1 to stop the program
def check_query(query):
    for word in query:
        if word not in indices:
            return -1, word
    return query

# Text cleaner method
# 1. Convert unwanted unicode to ascii - ftfy
# 2. Lower casing
# 3. Cleaning punctuations and white spaces
# 4. Lemmatizing the words using WordNet
# 5. Stop words Removal
def clean_text(text, lower=True, lemma=True, stopwords_removal=True):
    
    text = ftfy.fix_text(text)
    
    if lower:
        text = text.lower()
    
    text = re.sub(r'[\`\~\!\@\#\$\%\^\&\*\(\)\_\-\=\+\{\}\|\\\]\[\:\"\'\;\?\>\<\,\.\/]', ' ', text)
    # text = re.sub(r"\x00", ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.split()
    
    if lemma:
        text = [lemmatizer.lemmatize(word) for word in text]
        
    if stopwords_removal:
        text = [word for word in text if word not in stopwords]
    
    return text

# Checking if the two words are consecutive in the posting lists
def check_consec(posl_a, posl_b):
    
    while posl_a and posl_b:
        # print(posl_a[0], posl_b[0])
        if posl_a[0] >= posl_b[0]:
            del posl_b[0]
        elif posl_a[0] < posl_b[0]:
            if posl_b[0] - posl_a[0] == 1:
                return True
            del posl_a[0]    
    # print()
            
    return False

print("Cleaning text and constructing indices...")
for file_idx, file in tqdm(enumerate(files), total=len(files)):
    file_indices[file] = file_idx
    with open(path + file, 'r', encoding="latin-1") as file:
        file = file.read()
        
    file = clean_text(file)
        
    for word_idx, word in enumerate(file):
        # if word.lower()== "lion":
        #     print(word)
        if word not in indices:
            indices[word] = { "freq": 1,  "position": {file_idx: [word_idx]}}
        else:
            if file_idx not in indices[word]["position"]:
                indices[word]["position"][file_idx] = [word_idx]
                indices[word]["freq"] += 1
            else:
                indices[word]["position"][file_idx].append(word_idx)
            
            
file_indices_inv = {v:k for k, v in file_indices.items()}

print()
print("Soritng...")
indices = {key: indices[key] for key in sorted(indices.keys())}
print("Done")

# Querying
thresh = 5
query = clean_text(input("Enter query [MAX 5 WORDS]: "))
# query = "mushroom salad category"
# query = check_query(clean_text(query))
if query[0] != -1:
    # query = query.split()
    
    assert len(query) <= thresh
    
    docs = set(indices[query[0]]["position"].keys())
    for word in query[1:]:
        docs = set(indices[word]["position"].keys()).intersection(docs)
        
    doc_cntr = 0
    for doc in docs:
        print("Finding", "\""+' '.join(query) + "\"", "in", file_indices_inv[doc])
        cntr = 0
        for i in range(len(query)-1):
            # print("Querying", query[i], query[i+1])
            isconsec = check_consec(deepcopy(indices[query[i]]["position"][doc]), deepcopy(indices[query[i+1]]["position"][doc]))
            # print(isconsec)
            if isconsec:
                cntr += 1
            
        if len(query) - cntr == 1:
            print("\u2713 Found in", file_indices_inv[doc])
            doc_cntr += 1
            
    print()
    print("\u2713 Found in", doc_cntr, "doc(s)")
    
else:
    print("Your query got OOV:", query[1])