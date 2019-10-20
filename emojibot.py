import praw
import pdb
import re
import os
import time
import datetime

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit('memes')

emoji_unicode_prefix = "\\U000"
sarcasm = "/s"
emojis = ["1f600", "1f923", "1f602"]
max_member_since = 2592000

while(True):
	print("Woke up...")
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	for submission in subreddit.rising(limit=100):
		print("Title: ",submission.title)
		#print("Text: ",submission.selftext)
		#print("Score: ",submission.score)
		
		submission.comments.replace_more(limit=None)
		flat_comments = submission.comments.list()
		for comment in flat_comments:
			if comment.id not in comments_replied_to:
				comment_body = comment.body.encode('unicode-escape')
				#print("Comments: ", comment_body)
				for emoji in emojis:
					reply_string = ""
					#print((emoji_unicode_prefix+emoji))
					if (emoji_unicode_prefix+emoji) in comment_body:
						if sarcasm not in comment_body:
							member_since = time.time() - comment.author.created_utc
							if(member_since < max_member_since):
								print("Normie comment detected! Replying...")
								reply_string += "Hello there! You must be new to Reddit. Hope you enjoy the quality memes and the great community."
							elif comment.author.comment_karma > 0:
								print("Rebel comment detected! Replying...")
								reply_string += "Emoji detected! I see you are not that new to Reddit. You absolute rebel!"
							else:
								print("Negative karma detected! Replying...")
								reply_string += "Really? Doing this on purpose? Enjoy..."
						else:
							print("Sarcasm detected! Replying...")
							reply_string += "I detect use of sarcasm. I see you are a person of culture as well!"

						reply_string += "  \n"
						reply_string += ">*I am a bot. How did I do? DM me with your feedback*"
						comments_replied_to.append(comment.id)
						comment.reply(reply_string)
						time.sleep(5) #because rate_limit
						break #one reply for one comment; if multiple emojis used

	with open("comments_replied_to.txt", "w") as f:
		for comment_id in comments_replied_to:
			f.write(comment_id + "\n")
	print("Sleeping..")
	time.sleep(120)
