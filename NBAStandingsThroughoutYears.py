import requests
import pandas as pd
import time
import pickle

head = {"USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

#Seasons gathering data
seasons = ['2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]

#Dates at which standings are gathered
dates = ['11%2F15', '12%2F01', '12%2F15', '01%2F15', '02%2F15', '03%2F15', '04%2F20']

dfEast_dict = dict()
dfWest_dict = dict()


#Gather the NBA API and enter in the season and year into the url
for (season, year) in zip(seasons, years):
    urlUse = ''
    url = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=10%2F25%2F' + str(year) + '&DateTo=&Division=&GameScope=' \
                '&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=' \
                '&PlayerPosition=&PlusMinus=N&Rank=N&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
    dfEast = pd.DataFrame()
    dfWest = pd.DataFrame()
    for date in dates:
        urlList = url.split("DateTo=")
        if date.startswith('1'): #If in the first year of the season ex. in 2016 part of 2016-17 season
            urlUse = urlList[0] + "DateTo=" + date + '%2F' + str(year) + urlList[1]
        else:
            year2 = year + 1
            urlUse = urlList[0] + "DateTo=" + date + '%2F' + str(year2) + urlList[1]

        #split string so can add conferences
        urlEW = urlUse.split("?Conference=")

        #url for west standings
        urlW = urlEW[0] + "?Conference=" + 'West' + urlEW[1]

        #url for east standings
        urlE = urlEW[0] + "?Conference=" + 'East' + urlEW[1]

        responseE = requests.get(urlE, headers = head)
        responseW = requests.get(urlW, headers = head)

        #gather data frame headers and data for both east & west
        headers = responseW.json()['resultSets'][0]['headers']
        standingsEast = responseE.json()['resultSets'][0]['rowSet']
        standingsWest = responseW.json()['resultSets'][0]['rowSet']

        dfE = pd.DataFrame(standingsEast, columns=headers)
        dfW = pd.DataFrame(standingsWest, columns=headers)

        dfE.set_index('TEAM_NAME', inplace=True)
        dfW.set_index('TEAM_NAME', inplace=True)

        #sort values by win percentage
        dfE.sort_values(inplace=True, by='W_PCT', ascending=False)
        dfW.sort_values(inplace=True, by='W_PCT', ascending=False)

        #print out season, date, and top 8 teams from each conference
        #print season + " " + date[0:2] + '/' + date[5:]

        column_name = 'W_PCT' + date
        dfE = dfE[['W_PCT']]
        dfE.rename(columns={'W_PCT': column_name}, inplace=True)
        dfW = dfW[['W_PCT']]
        dfW.rename(columns={'W_PCT': column_name}, inplace=True)
        if dfEast.empty:
            print "EMPTY"
            dfEast = dfE
            dfWest = dfW
        else:
            dfEast = dfEast.join(dfE)
            dfWest = dfWest.join(dfW)
        time.sleep(0.5)
    dfEast_dict[season] = dfEast
    dfWest_dict[season] = dfWest

pickle_out = open("east.pickle", "wb")
pickle.dump(dfEast_dict, pickle_out)
pickle_out.close()

pickle_out = open("west.pickle", "wb")
pickle.dump(dfWest_dict, pickle_out)
pickle_out.close()







