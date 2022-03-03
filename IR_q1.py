# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 16:56:04 2022

@author: Mann
"""

# Importing required libraries
import os
import re
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import ftfy
from nltk.corpus import stopwords
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
            return -1
    return query

# Text cleaner method
# 1. Convert unwanted unicode to ascii - ftfy
# 2. Lower casing and word tokenized
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
    
    # return ' '.join(text)
    return text


# Operation execution. Works using Mere or set based algo to carry out operations
# Return comparisions made with required postings
def carry_op(posl_a, posl_b, op, method="merge", invert=None):
    
    comparisions = 0
    # print(len(posl_a), len(posl_b))
    if invert == [1]:
        posl_a = list(all_files_idx.difference(posl_a))
    elif invert == [2]:
        posl_b = list(all_files_idx.difference(posl_b))
    elif invert == [1,2]:
        posl_a = list(all_files_idx.difference(posl_a))
        posl_b = list(all_files_idx.difference(posl_b))
    
    if method == "merge":
        if op == "OR":
            tmp_posl = []
            
            while posl_a and posl_b:
                if posl_a[0] == posl_b[0]:
                    tmp_posl.append(posl_a[0])
                    del posl_a[0], posl_b[0]
                elif posl_a[0] > posl_b[0]:
                    tmp_posl.append(posl_b[0])
                    del posl_b[0]
                else:
                    tmp_posl.append(posl_a[0])
                    del posl_a[0]
                comparisions += 1
            if posl_a:
                tmp_posl += posl_a
            else:
                tmp_posl += posl_b
                
            # print("comparisions OR", comparisions)
                
            return tmp_posl, comparisions
        
        if op == "AND":
            tmp_posl = []
            
            while posl_a and posl_b:
                if posl_a[0] == posl_b[0]:
                    tmp_posl.append(posl_a[0])
                    del posl_a[0], posl_b[0]
                elif posl_a[0] > posl_b[0]:
                    del posl_b[0]
                else:
                    del posl_a[0]
                comparisions += 1
                # print("comparisions AND", comparisions)
            return tmp_posl, comparisions
    if method == "set":
        if op == "OR":
            return list(set(posl_a).union(posl_b))
        if op == "AND":
            return list(set(posl_a).intersection(posl_b))

print("Cleaning text and constructing indices...")
for file_idx, file in tqdm(enumerate(files), total=len(files)):
    file_indices[file] = file_idx
    with open(path + file, 'r', encoding="latin-1") as file:
        file = file.read()
        
    file = clean_text(file)
        
    for word in file:
        # if word.lower()== "lion":
        #     print(word)
        if word not in indices:
            indices[word] = [file_idx]
        elif indices[word] and indices[word][-1] != file_idx:
            indices[word].append(file_idx)
            

    # test = 100
    # if file_idx == test:
    #     all_files_idx = set(list(range(test)))
    #     break

file_indices_inv = {v:k for k, v in file_indices.items()}

print()
print("Soritng...")
indices = {key: indices[key] for key in sorted(indices.keys())}

print("Done")

ops_dict = {
    1: "OR",
    2: "AND",
    3: "OR NOT",
    4: "AND NOT"
    }

query = check_query(clean_text(input("Enter you query: ")))
if isinstance(query, list):
    # query = query.split()
    
    print("Enter ops. [OR]: 1, [AND]: 2, [OR NOT]: 3, [AND NOT]: 4 => ")
    ops = []
    for i in range(len(query)-1):
        ops.append(input(f"Enter op {i+1}/{len(query)-1}: "))
    ops = [ops_dict[int(op)] for op in ops]
    
    # assert len(query) - len(ops) == 1
    
    comp = 0
    # tmp_comp = 0
    if ops[0] == "AND NOT": 
        res, comp = carry_op(deepcopy(indices[query[0]]), deepcopy(indices[query[1]]), "AND", [2])
    elif ops[0] == "OR NOT": 
        res, comp = carry_op(deepcopy(indices[query[0]]), deepcopy(indices[query[1]]), "OR", [2])
    else:
        res, comp = carry_op(deepcopy(indices[query[0]]), deepcopy(indices[query[1]]), ops[0])
    # print("comp", comp)
    # print("len(res)", len(res))
    for i in range(2, len(query)):
        if ops[i-1] == "AND NOT":
            res, tmp_comp = carry_op(deepcopy(res), deepcopy(indices[query[i]]), op="AND", invert=[2])
            # print("len(res)", len(res)) 
            # print('tmp_comp if3', tmp_comp)
            comp += tmp_comp
        if ops[i-1] == "OR NOT":
            res, tmp_comp = carry_op(deepcopy(res), deepcopy(indices[query[i]]), op="OR", invert=[2])
            # print("len(res)", len(res)) 
            # print('tmp_comp if2', tmp_comp)
            comp += tmp_comp
        else:
            print()
            # print("Dummy", carry_op(deepcopy(res), deepcopy(indices[query[i]]), ops[i-1]))
            res, tmp_comp = carry_op(deepcopy(res), deepcopy(indices[query[i]]), ops[i-1])
            # print("len(res) else", len(res)) 
            # print('tmp_comp else', tmp_comp)
            comp += tmp_comp
            
        # print("len(res)", len(res))        
        # print('tmp_comp', tmp_comp)
        # comp += tmp_comp
        # print(query[i], ops[i-1])
    print("Comparisions", comp)
    print("Files", len(res))
    res_files = [file_indices_inv[idx] for idx in res]
    print("Files retrieved:", ", ".join(res_files[:5] + ["..."]))
else:
    print("Query is invalid: OOV")

