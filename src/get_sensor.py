import os
import requests
import datetime
from dotenv import load_dotenv

def get_data(month, day, year=2024, dur=24, keys='ts,latitude,longitude,BMP280 Barometer'):
	load_dotenv()
	THINGSBOARD_URL = os.getenv('THINGSBOARD_URL')
	ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
	DEV = os.getenv('DEVICE')

	beg_time = datetime.datetime(year, month, day, 0, 0, 0) + datetime.timedelta(hours=7)
	end_time = beg_time + datetime.timedelta(hours=dur)
	inter = int((end_time-beg_time).total_seconds() * 1000)
	btime = beg_time.strftime('%s') + '000'
	etime = end_time.strftime('%s') + '000'

	jwt = requests.post(
		f"{THINGSBOARD_URL}/api/auth/login",
		headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
		json={'username': 'tenant@thingsboard.org', 'password': 'tenant'}
	).json()['token']

	url = f"{THINGSBOARD_URL}/api/plugins/telemetry/DEVICE/" + DEV \
		+ '/values/timeseries?keys=' + keys \
		+ '&startTs=' + btime \
		+ '&endTs=' + etime \
		+ '&interval=' + str(inter) \
		+ '&limit=1000000000&agg=NONE'

	data = requests.get(
		url, headers={'Content-Type': 'application/json','X-Authorization': f'Bearer {jwt}'}
	).json()

	return data