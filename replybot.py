'''
This is my reddit bot.
Take 1
'''

import praw
import time
import reddit_cred
import sqlite3

'''
Define Global variables.  
'''


USERAGENT = "/u/redditbot101's first reddit bot (PRAW is awesome)"
USERNAME = reddit_cred.get_uname()
PASSWORD = reddit_cred.get_pword()
#For multiple subs, use 'sub1 + sub2' etc
SUBREDDIT = 'test'
#Test run, will change later to whatever
SEARCHQUERY = ['Python', 'Bot', 'Bots']
REPLY_STRING = "I am a python bot, what's your story?"
FETCH_POSTS_NUM = 100
WAIT_TIME = 10

print "Storing comment IDs in a database to ensure we don't recomment to the same post"
db = sqlite3.connect('comment_id_store.db')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
db.commit()
print "Done creating a database and a table to do so."


print "Connecting to reddit"
red = praw.Reddit(USERAGENT)
red.login(USERNAME, PASSWORD)
print "Successfully connected to reddit"

def reply_bot():
	print "Searching subreddit(s): " + SUBREDDIT
	subs = red.get_subreddit(SUBREDDIT)
	comments = subs.get_comments(limit=FETCH_POSTS_NUM)
	print "Got comments"
	for comment in comments:
		try:
			cid = comment.id
			print cid
			cur.execute('SELECT * FROM oldposts where ID = ?', [cid]) #SQL sanitisation
			if not cur.fetchone(): #i.e., we haven't come across this comment before
				cur.execute('INSERT INTO oldposts VALUES(?)', [cid])
				cbody = comment.body.lower() #shift everything to lower case, for comparison
				if any(search_key.lower() in cbody for search_key in SEARCHQUERY):
					#Don't reply to self
					if comment.author.name.lower() != USERNAME.lower():
						print "Replying to" + cid + "by " + comment.author.name
						comment.reply(REPLY_STRING)
		except AttributeError:
			print "Reddit user who posted this has deleted his account or had it deleted :("
	db.commit()

#reply_bot()

while True:
	reply_bot()
	db.commit()
	print('Running again in %d seconds' %WAIT_TIME)
	time.sleep(WAIT_TIME)
