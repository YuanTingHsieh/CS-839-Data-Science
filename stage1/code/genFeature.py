import os
from os.path import join

import numpy as np
import pandas as pd
from collections import Counter
import math
import re

text_mode = 'last' # brace or new or special or super or goodbye
doc_idx = 1
label_idx = 4

# read in examples
input_file = open('./' + text_mode + '_example.txt', 'rb')
examples = input_file.read().splitlines()
y = np.zeros(len(examples))
input_file.close()

# count word total frequency and document frequency
movie_path = './' + text_mode + '_pos_movie/'
word_count = Counter() # total frequency
df_dict = {} # document frequency
doc_count = 0
for root, dirs, files in os.walk(movie_path):
    for name in files:
        f = open(movie_path + name).read()
        words = f.lower().split()
        word_count.update(words)
        for w in set(words):
            df_dict[w] = df_dict.get(w, 0) + 1
        doc_count += 1

# word index in each documents
word_in_doc = [ dict() for x in range(doc_count) ]

# read in prefix dict
input_file = open('prefix_dict.txt', 'rb')
lines = input_file.read().lower().splitlines()
prefix_dict = set(lines)
input_file.close()


# random shuffle of doc numbers
np.random.seed(68)
indexes = np.arange(1, doc_count+1)
np.random.shuffle(indexes)
train_index = indexes[0:doc_count*2/3]
test_index = indexes[doc_count*2/3:]


# these are for DEBUG
doc_index = np.zeros(len(examples))
candidate_str = []
prev_str, next_str = [], []


# check for prefix dict
has_prefix = np.zeros(len(examples))
has_prefix_in_candidate = np.zeros(len(examples))

# tf, df, tf-idf, len of total chars, num of words
average_tf, average_df, average_tfidf = np.zeros(len(examples)), np.zeros(len(examples)), np.zeros(len(examples))
word_length, num_of_words = np.zeros(len(examples)), np.zeros(len(examples))
start_pos, end_pos = np.zeros(len(examples)), np.zeros(len(examples))

# tf, df, tf-idf of prev word
prev_tf, prev_df, prev_tfidf = np.zeros(len(examples)), np.zeros(len(examples)), np.zeros(len(examples))
next_tf, next_df, next_tfidf = np.zeros(len(examples)), np.zeros(len(examples)), np.zeros(len(examples))

# check if word in braces and if next is brace
is_in_braces = np.zeros(len(examples))
next_is_braces = np.zeros(len(examples))

# if all upper case and upper case count
is_all_upper = np.zeros(len(examples))
upper_counts = np.zeros(len(examples))

# check if words after looks like verb
next_like_verbs = np.zeros(len(examples))

# check if words after has first char Capital
next_word_capital = np.zeros(len(examples))

# start extracting features
for i, row in enumerate(examples):
    segs = row.split(',')

    doc_index[i] = segs[doc_idx]
    start_pos[i] = segs[2]
    end_pos[i] = segs[3]

    y[i] = segs[label_idx]

    candidate_str.append(segs[0])

    f = open(movie_path + text_mode  +"_" + segs[doc_idx] + ".txt").read().strip()
    words = f.lower().split()
    wc = Counter(words)


    # tf-idf of that segs
    # ex. Kevin Li => would count kevin and li's tf-idf
    # and average them
    tf_total = 0
    tfidf_total = 0
    df_total = 0
    upper_cases = 0
    word_list = segs[0].lower().split()
    for w in word_list:
        tf = float(wc[w]) / len(words)
        df = float(df_dict[w]) / doc_count
        tf_total += tf
        df_total += df
        tfidf_total += math.log(tf / (1 + df))
        if w in prefix_dict:
            has_prefix_in_candidate[i] = 1
 
    print "Dealing with ", word_list, " in doc ", segs[doc_idx]

    is_all_upper[i] = int(segs[0].isupper())
    for c in segs[0]:
        if c.isupper():
            upper_cases += 1
    upper_counts[i] = upper_cases

    average_tf[i] = float(tf_total) / len(word_list)
    average_df[i] = float(df_total) / len(word_list)
    average_tfidf[i] = float(tfidf_total) / len(word_list)

    word_length[i] = len(segs[0])
    num_of_words[i] = len(word_list)

    # tf-idf of prev word
    # start_pos is 1-based (starts at 1)
    curr_pos = int(start_pos[i] - 3)
    prev_word = ''
    while curr_pos >= 0:
        if f.lower()[curr_pos] == ' ':
            break
        prev_word = f.lower()[curr_pos] + prev_word
        curr_pos -= 1
    print "Get prev word ", prev_word

    if start_pos[i] == 1:
        prev_tf[i] = 0
        prev_df[i] = 0
        prev_tfidf[i] = 0
        has_prefix[i] = 0
        prev_str.append("")
    else:
        prev_tf[i] = float(wc[prev_word]) / len(words)
        prev_df[i] = float(df_dict[prev_word]) / doc_count
        prev_tfidf[i] = math.log(prev_tf[i] / (1 + prev_df[i]))
        if prev_word in prefix_dict:
            has_prefix[i] = 1
        prev_str.append(prev_word)


    # tf-idf of next word
    next_word = ''
    curr_pos = int(end_pos[i] + 1)
    while curr_pos < len(f.lower()):
        if f.lower()[curr_pos] == ' ' or f.lower()[curr_pos] == '\n':
            break
        next_word += f.lower()[curr_pos]
        curr_pos += 1
    print 'Get next word ', next_word

    if next_word == '' or next_word == ' ':
        next_tf[i] = 0
        next_df[i] = 0
        next_tfidf[i] = 0
        next_str.append("")
    else:
        next_tf[i] = float(wc[next_word]) / len(words)
        next_df[i] = float(df_dict[next_word]) / doc_count
        next_tfidf[i] = math.log(next_tf[i] / (1 + next_df[i]))
        next_str.append(next_word)

    # check braces
    if prev_word and next_word:
        if prev_word == '(' and next_word == ')':
            is_in_braces[i] = 1

    # check next word like verb or is brace or it has Capital first letter
    if next_word:
        if 'ed' in next_word or 'ing' in next_word:
            next_like_verbs[i] = 1
        if next_word == '(' or next_word == ')':
            next_is_braces[i] = 1
        if next_word[0].isupper():
            next_word_capital[i] = 1

d = {'doc_index': doc_index,
     'average_tf': average_tf,
     'average_df': average_df,
     'average_tfidf': average_tfidf,
     'word_length': word_length,
     'num_of_words': num_of_words,
     'prev_tf': prev_tf,
     'prev_df': prev_df,
     'prev_tfidf': prev_tfidf,
     'next_tf': next_tf,
     'next_df': next_df,
     'next_tfidf': next_tfidf,
     'label': y,
     'has_prefix': has_prefix,
     'has_prefix_in_candidate': has_prefix_in_candidate,
     'candidate_str': candidate_str,
     'is_all_upper': is_all_upper,
     'upper_counts': upper_counts,
     'is_in_braces': is_in_braces,
     'next_is_braces': next_is_braces,
     'prev_str': prev_str,
     'next_str': next_str,
     'next_like_verbs': next_like_verbs,
     'next_word_capital': next_word_capital,
    }

# these columns are for DEBUG purpose
columns_to_remove = ['doc_index', 'candidate_str', 'prev_str', 'next_str']

# split and save train and test data
X = pd.DataFrame(data=d)

X_train = X.loc[X['doc_index'].isin(train_index)]
X_test = X.loc[X['doc_index'].isin(test_index)]
X_train.loc[:, columns_to_remove].to_csv('train_index.csv', index=False)
X_test.loc[:, columns_to_remove].to_csv('test_index.csv', index=False)

y_train = X_train.loc[:, ['label']]
y_test = X_test.loc[:, ['label']]
X_train.drop(['label'] + columns_to_remove , axis=1, inplace=True)
X_test.drop(['label'] + columns_to_remove, axis=1, inplace=True)

X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

