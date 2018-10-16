import jsonlines
import re
import string
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import pandas as pd

# ----------------------------
# DATA RETRIEVAL
# ----------------------------

def getData(strings, limit=200000):

    out = []
    count = 0

    with jsonlines.open('inputs/charitybase.jsonl') as reader:
        for obj in reader:

            if count >= limit:
                break

            if len(strings) == 1:

                try:
                    out.append(obj[strings[0]])

                except:
                    out.append(None)

            if len(strings) == 2:

                try:
                    out.append(obj[strings[0]][strings[1]])

                except:
                    out.append(None)

            if len(strings) == 3:

                try:
                    out.append(obj[strings[0]][strings[1]][strings[2]])

                except:
                    out.append(None)

            count += 1

    return out

# ----------------------------
# TEXT SORTING
# ----------------------------

def word_stemmer(string_array):

    ps = PorterStemmer()
    regex_punc = re.compile('[%s]' % re.escape(string.punctuation))

    cleaned   = [regex_punc.sub('', string) for string in string_array]           # remove all punctuation
    tokenised = [word_tokenize(string) for string in cleaned]                     # tokenise input strings
    stemmed   = [[ps.stem(word) for word in string] for string in tokenised ]     # stem each word in each string
    out       = [' '.join(words) for words in stemmed]                            # join back together into string

    return out

# when passed an array of strings will convert each into regex
# which can be used to search for that sequence of words + spaces
def regexer(words):
    out = []
    for w in words:
        s = str("\\b"+re.sub(r'\s', '\\\s', w)+"\\b")
        out.append(re.compile(r'{}'.format(s)))

    return out


# given text data, pos & neg regex keys and match index, will search for all positive terms
# will ignore key matches where there is also a negative match
# negative keys should be list of lists, same length of positive keys
# (because positive keys can have multiple negative keys)
# match index should be list of ids for text data list, in same order, used to index output table

def keyword_match(desc, text_data, positive_keys, negative_keys, match_index):

    match_results = {'%s_matched_words' % desc:[], '%s_match_count' % desc:[]}
    table_index = []

    # loop through text fields
    for t_index, text in enumerate(text_data):

        # positive match indicator starts as false
        pos_ind = False
        matched_keys = []
        match_count = 0
#         neg_count = 0

#         print('-----activity-------')

        # loop through positive regex keys
        for r_index, pos in enumerate(positive_keys):

            neg_ind = False # reset negative match indicator

            p_test = re.search(pos, text)
#             print('pos: ', p_test)

            # if there is a match from a positive key, and there are negative keys present, test them
            if p_test:

                if len(negative_keys[r_index])> 0:

#                     print('testing negatives')
                    for n_regex in negative_keys[r_index]:

#                         print('neg: ', re.search(n_regex, text))

                        if re.search(n_regex, text):

                            neg_ind = True
#                             neg_count +=1

#                 print(neg_ind)
                # if the negative match indicator stays false, then the positive was valid
                if neg_ind == False:

                    pos_ind = True

                    # append the matched value and increment the counter
                    matched_keys.append(p_test.group())
                    match_count += 1

#         neg_counts.append(neg_count)

        # add all matched values and counter to dict for positive matches
        if pos_ind:

            match_results['%s_matched_words' % desc].append(matched_keys)
            match_results['%s_match_count' % desc].append(match_count)
            table_index.append(match_index[t_index]) # look up the index value for the current text field


    return pd.DataFrame(match_results, index=table_index)
