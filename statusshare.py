#!/usr/bin/env python

import daemon, urllib2, json, twitter, time, urllib

"""
	Insert the URL to the IBM Sametime Connect Web API,
	normally http://localhost:59449/stwebapi/
"""

ST_WEB_API = "http://localhost:59449/stwebapi/"

"""
	The user id whom status shall be shared.
"""
USER_ID = "john.doe@foo.com"

"""
	The credentials file for the Twitter API, 
	as given in the example.
"""
CREDENTIALS_FILE = "credentials.json"

"""
	Defines the interval between a new status checkup is.
"""
POLL_SLEEP = 5

def getStatus(getStatusUrl, truncateLocation=False):
	"""
		Gets the status message via the IBM Sametime
		Connect Web API and retuns it. If truncateLocation
		is set to True, it removes possible location remarks.
	"""	

	response = urllib2.urlopen( getStatusUrl )
	html = response.read()
	status = json.loads( html )
	statusMsg = status[u'statusMessage']

	if truncateLocation:
		lastAtSign = statusMsg.rfind("@")
		statusMsg = statusMsg[:lastAtSign]

	return statusMsg

if __name__ == "__main__":
	with open(CREDENTIALS_FILE, 'r') as f:
		c = json.load(f)

	getStatusUrl = "{0}/{1}{2}".format(ST_WEB_API.rstrip('/'), "getstatus?userId=", urllib.urlencode(USER_ID))
	api = twitter.Api(consumer_key=c["consumer-key"], consumer_secret=c["consumer-secret"], access_token_key=c["accesstoken-key"], access_token_secret=c["accesstoken-secret"])
		
	lastStatus = ""
	while True:
		curStatus = getStatus(getStatusUrl)
		if lastStatus != curStatus:
			try:
				api.PostUpdate(curStatus)
			except twitter.TwitterError:
				pass
		lastStatus = curStatus
		time.sleep(POLL_SLEEP)

	