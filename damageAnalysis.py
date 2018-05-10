import pandas as pd
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import sqlite3


sql = sqlite3.connect('tweets.db')
df = pd.read_sql_query("SELECT * FROM tweets", sql)
damdf = df[df['Tweet'].str.contains("damage|propert", na = False)==True]
damdf['chunks'] = ""
damdf = damdf.reset_index()
badwords = ['hurricaneharvey', 'harvey2017', 'harvey', 'hurricane','texas', 'trump', 'mexico']

#tokenize the text of a tweet to pull location metadata
def get_area(text, label):
    text = text[0].lower() + text[1:]
    tokenized = word_tokenize(text)
    filtered_tokenized_text = [word for word in tokenized if word.lower() not in badwords]
    chunked = ne_chunk(pos_tag(filtered_tokenized_text))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree and subtree.label() == label and subtree[0][1] == "NNP":
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
            return current_chunk[0]
        elif type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if subtree[0] == ',':
                current_chunk.append("".join(subtree[0]))
                # return " ".join(current_chunk)
            elif named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    for chunk in continuous_chunk:
        if len(chunk) > 5 and len(chunk.split(" ")[-1]) == 2:
            return chunk
    return 'None'


for index, row in damdf.iterrows():
    damdf.at[index, 'chunks'] = get_area(row['Tweet'], 'GPE')


damdf.to_sql("damageTweets", sql, if_exists = "replace")