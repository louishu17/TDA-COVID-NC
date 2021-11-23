import matplotlib.pyplot as plt
import numpy as np
# import diode
# import dionysus as d
import json
import json
from numpy.random import choice
import csv
from datetime import date, timedelta
import datetime as dt
import matplotlib.dates as mdates
from scipy.ndimage.filters import uniform_filter1d
import numpy as np
import gudhi as gd
import gudhi.representations
import matplotlib.pyplot as plt


def plot_landscapes(points):
    simplicies = gd.AlphaComplex(points=points).create_simplex_tree()
    dgmX = simplicies.persistence()

    gd.plot_persistence_diagram(dgmX)
    plt.show()

    LS = gd.representations.Landscape(resolution=1000)
    L = LS.fit_transform([simplicies.persistence_intervals_in_dimension(1)])
    plt.plot(L[0][:1000])
    plt.plot(L[0][1000:2000])
    plt.plot(L[0][2000:3000])
    plt.title("Landscape")
    plt.show()

def sample_counties(date, x, weighted):
    with open('Cases_By_County.json') as fp:
        json_data = json.load(fp)

        print(date)

        if not json_data.get(date) is None:
            countiesData = json_data[date]
        else:
            return None
        cases = []
        counties = []

        
        for key,values in countiesData.items():
            counties.append(key)
            if not weighted:
                cases.append(values[0])
            else:
                cases.append(values[2])
                #print(values[2])

        total = sum(cases)
        # print(total)
        for i in range(len(cases)):
            #print(cases[i])
            #print(total)
            cases[i] = cases[i] / total
            #print(cases[i])
    

        # print(cases)
        # for c in counties:
        #     cases.append(counties[c])
        list_of_counties = choice(counties, x, p= cases,replace=False)
        print(list_of_counties)

        data = []
        with open("County_Location.csv", encoding='utf-8-sig') as csvf:
            csvReader= csv.DictReader(csvf)
            for rows in csvReader:
                if rows['County'] in list_of_counties:
                    # print (rows)
                    data.append([float(rows['X']), float(rows['Y'])])

        data = np.asarray(np.stack(data))

        return data

sdate = date(2021, 9,11)   # start date
# sdate = date(2021, 10, 7)   # start date (test)
edate = date(2021, 9,11 )   # end date

delta = edate - sdate       # as timedelta
date_array_unformatted = []
zero_array = []
first_array = []
total_cases_array = []
for i in range(delta.days + 1):

    day = sdate + timedelta(days=i)
    day = day.strftime("%#m/%#d/%Y")
    total_county_sample = 40
    
    counties = sample_counties(day, total_county_sample, True)
    # print(counties)
    if not counties is None:
        date_array_unformatted.append(day)
        with open("TABLE_DAILY_CASE&DEATHS_METRICS.csv", encoding='utf-16') as csvf:
            csvReader= csv.DictReader(csvf)
            for rows in csvReader:
                
                if dt.datetime.strptime(rows['Date'], '%m/%d/%y').strftime("%#m/%#d/%Y") == day:
                    total_cases_array.append(float(rows['Cases']))
    else:
        continue
    
    zero_total = 0
    first_total = 0
    total_trials = 1
    for j in range(total_trials):
        counties = sample_counties(day, total_county_sample, True)
        plot_landscapes(counties)