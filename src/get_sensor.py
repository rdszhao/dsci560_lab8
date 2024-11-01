import requests
import json
import datetime

# duration in hours
dur = 24

# sensor device and labels
keys = "temperature,pressure" # your sensor keys - NEED TO MATCH YOUR CONFIGURATION
dev = "26b780b0-2b12-11ee-b632-1d3c39b59be8" # device - NEED TO MATCH YOUR CONFIGURATION

# begin time need to be adjusted for time zone: PST add 7 hours
beg_time = datetime.datetime(2024, 9, 20, 0, 0, 0)+datetime.timedelta(hours=7)
end_time = beg_time+datetime.timedelta(hours=24)  # 24 hours of collected data
inter = int((end_time-beg_time).total_seconds()*1000) # total interval in miliseconds
btime = beg_time.strftime('%s')+'000' # begin time
etime = end_time.strftime('%s')+'000' # end time

# Get JWT Security Token from Thingsboard IO
jwt = requests.post(
	'http://YOUR_THINGSBOARD_ADDRESS:8080/api/auth/login',
	headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
	json={'username': 'tenant@thingsboard.org', 'password': 'password'}
).json()['token']

url = 'http://YOUR_THINGSBOARD_ADDRESS:8080/api/plugins/telemetry/DEVICE/' + dev \
	+ '/values/timeseries?keys=' + keys \
	+ '&startTs=' + btime \
	+ '&endTs=' + etime \
	+ '&interval=' + str(inter) \
	+ '&limit=1000000000&agg=NONE'

data = requests.get(
	url, headers={'Content-Type': 'application/json','X-Authorization': f'Bearer {jwt}'}
).json()