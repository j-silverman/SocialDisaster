import csv, sqlite3


sql = sqlite3.connect('tweets.db')
cur = sql.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS tweets (ID, Likes, Replies, Retweets, Time, Tweet)''')

with open('Hurricane_Harvey.csv','r', encoding = 'utf-8', errors = 'ignore') as f: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(f) # comma is default delimiter
    to_db = [(i['ID'], i['Likes'], i['Replies'], i['Retweets'], i['Time'], i['Tweet']) for i in dr]

cur.executemany("INSERT INTO tweets (ID, Likes, Replies, Retweets, Time, Tweet) VALUES (?, ?, ?, ?, ?, ?);", to_db)
sql.commit()
sql.close()