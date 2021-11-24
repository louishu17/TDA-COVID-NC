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
import os


def plot_landscapes(points, date):
    simplicies = gd.AlphaComplex(points=points).create_simplex_tree()
    dgmX = simplicies.persistence()

    # gd.plot_persistence_diagram(dgmX)
    # plt.show()

    #
    LS = gd.representations.Landscape(resolution=50, sample_range = [0, 1])
    L = LS.fit_transform([simplicies.persistence_intervals_in_dimension(1)])
    plt.plot(L[0][:50])
    plt.plot(L[0][50:100])
    plt.plot(L[0][100:150])
    plt.title("Landscape")
    filesday = day.replace('/',' ')
    plt.savefig('images/figure ' + filesday + '.png', bbox_inches='tight')
    plt.close()

    # PI = gd.representations.PersistenceImage(bandwidth=1e-4, weight=lambda x: x[1]**2, \
    #                                      im_range=[0,.004,0,.004], resolution=[100,100])
    # pi = PI.fit_transform([simplicies.persistence_intervals_in_dimension(1)])
    # plt.imshow(np.flip(np.reshape(pi[0], [100,100]), 0))
    # plt.title("Persistence Image")
    # plt.show()

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

def plot_counties(data):
    x_coords = []
    y_coords = []
    for x,y in data:
        x_coords.append(x)
        y_coords.append(y)
    x_fullcoords = []
    y_fullcoords = []
    with open("County_Location.csv", encoding='utf-8-sig') as csvf:
        csvReader= csv.DictReader(csvf)
        for rows in csvReader:
            # print (rows)
            x_fullcoords.append(float(rows['X']))
            y_fullcoords.append(float(rows['Y']))

    plt.style.use('seaborn-ticks')


    plt.scatter(x_fullcoords, y_fullcoords)
    plt.scatter(x_coords, y_coords)

    ax = plt.gca()
    ax.set_ylim([-90,-70])

    plt.show()


sdate = date(2021,11,7)   # start date
# sdate = date(2021, 10, 7)   # start date (test)
edate = date(2021,11,7)   # end date

delta = edate - sdate       # as timedelta
date_array_unformatted = []
zero_array = []
first_array = []
total_cases_array = []
for i in range(delta.days + 1):

    day = sdate + timedelta(days=i)
    day = day.strftime("%#m/%#d/%Y")
    total_county_sample = 20
    
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
        plot_counties(counties)
        # plot_landscapes(counties, day)