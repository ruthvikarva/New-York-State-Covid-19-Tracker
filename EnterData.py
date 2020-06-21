import time
import urllib
import json
import sqlite3
from datetime import datetime as dt, date, timedelta

startingDate = date(2020, 3, 2)
unixTime = 0
endDate = date.today()

dateCounter = 1
conn = sqlite3.connect('Covid.db')
curs = conn.cursor()

county = ['Albany', 'Allegany', 'Bronx', 'Broome', 'Cattaraugus', 'Cayuga', 'Chautauqua', 'Chemung', 'Chenango',
          'Clinton', 'Columbia', 'Cortland', 'Delaware', 'Dutchess', 'Erie', 'Essex', 'Franklin', 'Fulton', 'Genesee',
          'Greene', 'Hamilton', 'Herkimer', 'Jefferson', 'Kings', 'Lewis', 'Livingston', 'Madison', 'Monroe', 'Montgomery',
          'Nassau', 'New York', 'Niagara', 'Oneida', 'Onondaga', 'Ontario', 'Orange', 'Orleans', 'Oswego', 'Otsego',
          'Putnam', 'Queens', 'Rensselaer', 'Richmond', 'Rockland', 'Saratoga', 'Schenectady', 'Schoharie', 'Schuyler',
          'Seneca', 'St. Lawrence', 'Steuben', 'Suffolk', 'Sullivan', 'Tioga', 'Tompkins', 'Ulster', 'Warren', 'Washington',
          'Wayne', 'Westchester', 'Wyoming', 'Yates']


while startingDate <= endDate:
    covid_website_data = "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + str(startingDate) + "T00:00:00.000"
    print(covid_website_data)
    with urllib.request.urlopen(covid_website_data) as url1:
            # "https://health.data.ny.gov/resource/xdss-u53e.json?test_date=" + date_string + "T00:00:00.000") as url1:
        data1 = json.loads(url1.read().decode())

        if len(data1) > 1:
            #county_names = [str(county['county']) for county in data1]
            county_new_positives = [int(county['new_positives']) for county in data1]
            cumulative_number_of_positives = [int(county['cumulative_number_of_positives']) for county in data1]
            total_number_of_tests = [int(county['total_number_of_tests']) for county in data1]
            cumulative_number_of_tests = [int(county['cumulative_number_of_tests']) for county in data1]

            unixTime = int(time.mktime(startingDate.timetuple()))
            unixDate = date.fromtimestamp(unixTime)
            print(startingDate, unixTime, unixDate)

            for i in range(62):
                #print(unixTime, county[i], county_new_positives[i], cumulative_number_of_positives[i], total_number_of_tests[i], cumulative_number_of_tests[i])
                curs.execute("INSERT INTO CORONA(Date, County, Positives_Today, Cumulative_Positive, Tests_Performed_Today, Cumulative_Tests) VALUES(?,?,?,?,?,?)",
                             (unixTime, county[i], county_new_positives[i], cumulative_number_of_positives[i], total_number_of_tests[i], cumulative_number_of_tests[i]))
                conn.commit()
            startingDate += timedelta(days=dateCounter)


            # curs.execute('SELECT * FROM CORONA WHERE Date = 1583211600 AND County = "Albany"')
            # getInfo = curs.fetchall()
            # print(type(getInfo))
            # for row in getInfo:
            #     print(row)
            # formatted_row = '{:<10} {:<6} {:>6} {:>6} {:<9} {:<9}'
            # print(formatted_row.format("Date", "County", "New +", "Cum +", "Test ^|^", "Cum test"))
            # for Row in q:
            #     print(formatted_row.format(*Row))

