#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2013 Malte Bublitz, https://malte-bublitz.de
# Copyright (c) 2013 Benjamin Leuckefeld, http://atroxlp.de
# Copyright (c) 2012 Juan C. Olivares <juancri@juancri.com>
# based on original code by Christian Palomares <palomares.c@gmail.com>
# 
# Distributed under the MIT/X11 license. Check LICENSE for details.
# 

import time
import os
import _twitter
import sys

class RetweetBot(object):
	def run(self, me, hashtag, add_hashtags, sleep, count, native_retweet, con_key, con_sec, tok_key, tok_sec, check_conds):
		import log
		logger = log.Log(os.path.join(os.path.dirname(__file__), ".".join(os.path.basename(__file__).split(".")[:-1])+".log"))
		if len(sys.argv)>1:
			if sys.argv[1] == "-v":
				logger.setConsoleLogLevel(log.INFO)
	
		logger.info("----------------------------------")
		logger.info("     Flying Sheep Retweet Bot")
		logger.info("         Bot is starting!")
		logger.info("----------------------------------")
		logger.info("")
		
		print "----------------------------------"
		print "     Flying Sheep Retweet Bot"
		print "         Bot is starting!"
		print "----------------------------------"
		print ""
			
		api = _twitter.Api (
			consumer_key = con_key,
			consumer_secret = con_sec,
			access_token_key = tok_key,
			access_token_secret = tok_sec
		)
		
		logger.info("Bot started!")
		logger.info("Searching tweets containing '" + hashtag + "'.")
		
		print "Bot started!"
		print "Searching tweets containing '" + hashtag + "'."
		
		# loop
		lastid = None
		first = 1
		while 1:
			# get last tweets
			try:
				timeline = api.GetSearch(hashtag, since_id = lastid, per_page = count)
			except _twitter.TwitterError:
				logger.error("Could not get tweets!")
				continue
			
			# update last ID
			if len (timeline) > 0:
				lastid = timeline [0].id
				logger.info("Last ID updated:" + str(lastid))
			
			# skip the first time
			if first > 0:
				first = 0
				continue
			
			# check tweets
			for status in timeline:

				# do not rt own tweets
				if status.user.screen_name.lower() == me:
					continue
				
				# has additional hashtag
				if len(add_hashtags) > 0:
					send = False
					for ht in add_hashtags:
						if status.text.lower().find(ht) >= 0:
							send = True

					if not send:
						continue
				if not check_conds(status):
					continue
				
				try:
					# let's retweet
					if native_retweet:
						logger.info("Retweeting: " + status.user.screen_name + " " + status.text)
						api.PostRetweet (status.id)
					else:
						retweet = 'RT @' + status.user.screen_name + ": " + status.text
						if len (retweet) > 140:
							retweet = retweet [:137] + "..."
						logger.info("Tweeting: " + retweet)
						api.PostUpdate (retweet)
				except _twitter.TwitterError:
					logger.error("Could not retweet!")

			# zZzZzZ
			time.sleep(sleep)
			
def main():
	bot = RetweetBot()
	bot.run()

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
