#Last update: 9/23 12:30am

#imports
	#need to clean up after switching methodology
import sys
from stackexchange import *
import requests
import collections
import csv
import urllib
from re import findall
from unidecode import unidecode

#declare variables
#create StackOverflow object for use with the API
so = stackexchange.Site(stackexchange.StackOverflow)
so.impose_throttling = True
so.throttle_stop = False
so.be_inclusive()

#create csv handler for output
with open('test2.csv', 'w') as csvfile:
	writer = csv.writer(csvfile)
	#write table header
	writer.writerow(['Question ID', 'Answer ID', 'Answer Score', 'Answer Accepted', 'Answer Text'])
#loop through each relevant question, then each relevant answer in that question
#store metadata and answer content
	for question in so.questions(tagged=['c'], pagesize=10, body = True):
		questionID = question.question_id
		answers = question.answers
		print(questionID, question.title)
		for answerID in answers:
			answerScore = answerID.score
			answerAccepted = answerID.accepted
#removes unwritable (non-ASCII) characters, puts each answer on a new line
			writer.writerow([questionID, answerID, answerScore, answerAccepted, unidecode(answerID.body)])