import pickle
import pandas as pd

seasons = ['2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
dates = ['11%2F15', '12%2F01','12%2F15', '01%2F15', '02%2F15', '03%2F15', '04%2F20']

pickle_in = open("west.pickle", "rb")
west = pickle.load(pickle_in)

pickle_in_east = open("east.pickle", "rb")
east = pickle.load(pickle_in_east)

for season in seasons:
    column_name = 'W_PCT' + dates[1]
    column_two = 'W_PCT' + dates[-1]
    try:
        west[season]['PCT_CHANGE'] = (west[season][column_two]/west[season][column_name]) * 100
        print season
        season_sorted = west[season].sort_values(by='PCT_CHANGE', ascending=False)
        print season_sorted[[column_name, column_two, 'PCT_CHANGE']]
    except:
        print season

for season in west:
    column_name = 'W_PCT' + dates[1]
    column_two = 'W_PCT' + dates[-1]
    if season=="2011-12":
        continue
    else:
        season_sorted = west[season].sort_values(inplace=True, by='PCT_CHANGE', ascending=False)
        #print season_sorted

