There are 2 files corresponding to each question
1. IR_q1.py
2. IR_q2.py

## IR_q1.py
- Unigram inverted DS is constructed on the given files
- Following operations are permitter
    - OR
    - AND
    - AND NOT
    - OR NOT
- Method:
    - Each file is iterated and stored as integer in the dictionary format
    - Whole content is iterated and words are cleaned and stored in the posting lists
    - These steps give sorted postings by default
    - Keys are sorted after the construction
- If word in query is OOv, program will terminate

## IR_q2.py
- Positional indexing has been done
- query upto 5 words are supported
- Cleaniong steps mentioned are done
- Method:
    - Each file is iterated and stored as integer in the dictionary format
    - Whole content is iterated and words are cleaned and stored in the position lists
    - These steps give sorted positions by default
    - Keys are sorted after the construction
- If word in query is OOv, program will terminate