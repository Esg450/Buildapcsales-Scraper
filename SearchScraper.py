import json, requests, re, decimal, sys, time, praw
from twilio.rest import Client
import requests.auth
from datetime import datetime

#Open Config file
with open('config.json') as jsonConfig:
	configData = json.load(jsonConfig)

#Authorize twilio client
client = Client(configData['twilio']['account_sid'], configData['twilio']['auth_token'])

#Create Item list and set initial runtime
item_list = []
initial_run = True
parsed_search = []
headers = {}

def authorizeReddit():
	global headers
	#Authorize Reddit
	client_auth = requests.auth.HTTPBasicAuth(configData['reddit']['client_key'], configData['reddit']['client_secret'])
	post_data = {"grant_type": "password", "username": configData['reddit']['username'], "password": configData['reddit']['password']}
	headers = {"User-Agent": "BuildAPCScraper/0.1 by Retrums"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers).json()

	headers = {"Authorization": "bearer " + response['access_token'] + "", "User-Agent": "BuildAPCScraper/0.1 by Retrums"}

def pullData():
	global parsed_search
	authorizeReddit()
	try:
		request = requests.get("https://oauth.reddit.com/r/buildapcsales/search.json?q=" + configData['search']['type'] + "&sort=new&restrict_sr=on", headers=headers)
		request.raise_for_status()
	except requests.exceptions.HTTPError as err:
	    print err
	    sys.exit(1)

	#Convert reddit response to json
	parsed_search = json.loads(request.text)

def parsePrice(title):
	matchObj = re.search('(\d+([.,]?)\d{0,}([.,]?)\d*(\s*)(\$))|((\$)(\s*)\d+([.,]?\d{0,}([.,]?\d+)))', title)
	if matchObj:
		strip_sign = re.sub('[\$,]', '', matchObj.group())
		return decimal.Decimal(strip_sign)

def sendText(text):
	for number in configData['twilio']['receive_phones']:
		client.messages.create(to=number, from_=configData['twilio']['send_phone'], body=text)

def initialRun():
	pullData()
	global item_list
	for item in parsed_search['data']['children']:
		title = item['data']['title']
		price = parsePrice(title)
		item_id = item['data']['id']

		if price >= configData['search']['start_price'] and price <= configData['search']['end_price']:
			if any(term in title for term in configData['search']['terms']):
				item_list.append(item_id)
				print "Adding initial item to list: " + title

def refreshList():
	pullData()
	global item_list
	for item in parsed_search['data']['children']:
		title = item['data']['title']
		price = parsePrice(title)
		item_id = item['data']['id']

		if price >= configData['search']['start_price'] and price <= configData['search']['end_price'] and item_id not in item_list:
			if any(term in title for term in configData['search']['terms']):
				item_list.append(item_id)
				print "Found new item: " + title
				sendText("New item: " + title + ". Link: " + item['data']['url'])

try:
	while True:
		if initial_run:
			initialRun()
			initial_run = False
		else:
			print "Refreshing list at " + str(datetime.now())
			refreshList()

		time.sleep(configData['refresh_time'])
except KeyboardInterrupt:
	print ("Manual user break")
