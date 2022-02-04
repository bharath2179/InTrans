class ClearGuideApiHandler:
    import requests

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.refresh_token = None
        self.access_token = None
        self.authenticate()

    def authenticate(self):
        data = {"username": self.username, "password": self.password}
        response = self.requests.post('http://auth.iteris-clearguide.com/api/token/', data=data)
        if response.status_code == 200:
            response_dict = response.json()
            self.refresh_token = response_dict.get('refresh')
            self.access_token = response_dict.get('access')
            if self.refresh_token and self.access_token:
                return True
        raise Exception(
            "Error while authenticating... Status Code: {response.status_code} Message: {response.text}")

    def refreshing_token(self):
        data = {"refresh": self.refresh_token}
        response = self.requests.post('http://auth.iteris-clearguide.com/api/token/refresh/', data=data)
        if response.status_code == 200:
            self.access_token = response.json().get('access')
        else:
            return self.authenticate()

    @property
    def auth_header(self):
        return {'Authorization': 'Bearer {self.access_token}'}

    def call(self, url):
        response = self.requests.get(url=url, headers=self.auth_header)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            self.refreshing_token()
            return self.call(url)
        else:
            raise Exception(
                "Error fetching response from ClearGuide... Status Code: {response.status_code} Message: {response.text}")
import sys
sys.setrecursionlimit(10000)
import pandas as pd
import datetime
import pytz
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--START', default=None, type=str) # date format should be yyyy-mm-dd
parser.add_argument('--END', default=None, type=str) # not included
# parser.add_argument('--METRIC', default=None, type=str)
args = parser.parse_args()
start = args.START
end = args.END
metric = 'avg_travel_time'

def get_meta(cg_api_handler, route_list):
    now = int(time.time())
    URL = "https://api.iteris-clearguide.com/v1/route/performance/?customer_key=udot&s_timestamp=%s&e_timestamp=%s&metrics=avg_travel_time&route_ids="%(now-10,now)
    for route_id in set(route_list.API_ID):
        route_id = int(route_id)
        suffix = '%2C'+str(route_id)
        URL += suffix
    r = cg_api_handler.call(url=URL)
    tz = r['timezone']
    df = pd.DataFrame(r['datasets']['all'])
    return tz, df

def to_unix(dt_str, tz):
    local_time = pytz.timezone(tz)
    dt = datetime.datetime.strptime(dt_str,'%Y-%m-%d')
    local_dt = local_time.localize(dt)
    timestamp = local_dt.astimezone(pytz.utc).timestamp()
    return timestamp

def download_data(cg_api_handler, route_list, metric, start, end):
    df = []
    for route_id in set(route_list.API_ID):
        route_id = int(route_id)
        print (route_id)
        corridor_name = route_list.loc[route_list['API_ID']==route_id, 'corridor'].values[0]
        direction = route_list.loc[route_list['API_ID']==route_id, 'direction'].values[0]
        # multi-route does not have time series
        # URL = "https://api.iteris-clearguide.com/v1/route/performance/?customer_key=udot&route_ids=33545%2C33546&s_timestamp=1607068000&e_timestamp=1607069173&metrics=avg_travel_time&granularity=5min"
        URL = "https://api.iteris-clearguide.com/v1/route/timeseries/?customer_key=udot&route_id=%s&s_timestamp=%s&e_timestamp=%s&metrics=%s&granularity=5min"%(route_id, int(start), int(end), metric)
        r = cg_api_handler.call(url=URL)
        # print (r)
        data = r['series']['all'][metric]['data']
        temp = pd.DataFrame(data)
        temp.columns=['time', metric]
        temp['route_id']=route_id
        temp['corridor']=corridor_name
        temp['direction']=direction
        df.append(temp)
    return df

if __name__ == '__main__':
    USER_NAME = "anuj.sharma@etalyc.com"
    PASSWORD = "Husker$123"
    cg_api_handler = ClearGuideApiHandler(username=USER_NAME, password=PASSWORD)
    route_list = pd.read_csv('corridor_here_matched.csv', header=0)
    route_list = route_list.dropna()
    tz, meta = get_meta(cg_api_handler, route_list)
    start = to_unix(start, tz)
    end = to_unix(end, tz)
    res = download_data(cg_api_handler, route_list, metric, start, end)
    res = pd.concat(res)
    # convert back to local date time
    res['time']=pd.to_datetime(res.time, unit='s', utc=True).dt.tz_convert(tz).dt.strftime('%Y-%m-%d %H:%M:%S')
    meta = meta[['route_id','route_length']]
    final = pd.merge(res, meta, on=['route_id'])
    final['travel_rate']=final['avg_travel_time']/final['route_length'] # min per mile
    final.to_csv('%s_data.csv'%metric, index=False)
