import requests
import time
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import seaborn as sns
from IPython.display import display



head = {"USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
shot_url = 'http://stats.nba.com/stats/shotchartdetail?Period=0&VsConference=&LeagueID=00&LastNGames=0&TeamID=0&PlayerPosition=&Location=&Outcome=&ContextMeasure=FGA&DateFrom=&StartPeriod=&DateTo=&OpponentTeamID=0&ContextFilter=&RangeType=&Season=2015-16&AheadBehind=&PlayerID=1626156&EndRange=&VsDivision=&PointDiff=&RookieYear=&GameSegment=&Month=0&ClutchTime=&StartRange=&EndPeriod=&SeasonType=Regular+Season&SeasonSegment=&GameID='
try:
    response = requests.get(shot_url, headers=head)
except:
    time.sleep(1)
    response = requests.get(shot_url, headers=head)
print(shot_url)
print(response.json())

headers = response.json()['resultSets'][0]['headers']
shots = response.json()['resultSets'][0]['rowSet']
shot_df = pd.DataFrame(shots, columns=headers)
with pd.option_context('display.max_columns', None):
    display(shot_df.head())




