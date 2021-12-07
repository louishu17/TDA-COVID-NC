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
import operator
import scipy


def plot_landscapes(points, prevLandscape, first):
    simplicies = gd.AlphaComplex(points=points).create_simplex_tree()
    dgmX = simplicies.persistence()

    # gd.plot_persistence_diagram(dgmX)
    # plt.show()

    #
    SH = gd.representations.Silhouette(resolution=50,weight=lambda x: np.power(x[1]-x[0],1), sample_range = [0, 1])
    sh = SH.fit_transform([simplicies.persistence_intervals_in_dimension(1)])
    if first:
        return sh[0]
    else:
        # print(prevLandScape)
        # print(sh[0])
        # print(np.linalg.norm(sh[0] - prevLandscape))
        return (sh[0], np.linalg.norm(sh[0] - prevLandscape))
    # plt.plot(sh[0])
    # plt.title("Landscape")
    # filesday = day.replace('/',' ')
    # plt.savefig('images/figure ' + filesday + '.png', bbox_inches='tight')
    # plt.show()
    # plt.close()

    # PI = gd.representations.PersistenceImage(bandwidth=1e-4, weight=lambda x: x[1]**2, \
    #                                      im_range=[0,.004,0,.004], resolution=[100,100])
    # pi = PI.fit_transform([simplicies.persistence_intervals_in_dimension(1)])
    # plt.imshow(np.flip(np.reshape(pi[0], [100,100]), 0))
    # plt.title("Persistence Image")
    # plt.show()

def sample_counties(date, x, weighted):
    with open('Cases_By_County.json') as fp:
        json_data = json.load(fp)

        # print(date)

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
        # print(list_of_counties)

        data = []
        with open("County_Location.csv", encoding='utf-8-sig') as csvf:
            csvReader= csv.DictReader(csvf)
            for rows in csvReader:
                if rows['County'] in list_of_counties:
                    # print (rows)
                    data.append([float(rows['X']), float(rows['Y'])])

        data = np.asarray(np.stack(data))

        return data

def plot_counties(date, weighted):

    countieslist = {}
    x_fullcoords = []
    y_fullcoords = []
    cases = []
    countiesData = {}
    with open("County_Location.csv", encoding='utf-8-sig') as csvf:
        csvReader= csv.DictReader(csvf)
        for rows in csvReader:
            countieslist.setdefault(rows['County'], [float(rows['X']),float(rows['Y']),])
    json_file_name = 'Cases_By_County.json'
    with open(json_file_name) as fp:
        json_data = json.load(fp)
        if not json_data.get(date) is None:
            countiesData = json_data[date]
        else:
            print("DID NOT FIND")
            return None
    
    # print(countieslist)
    for key,values in countiesData.items():
        # print(key)
        if key == "New":
            key = "New Hanover"
        if not weighted:
            countieslist[key].append(values[0])
            # counties_list.append(tuple((key, values[0])))
        else:
            countieslist[key].append(values[2])

    plt.style.use('seaborn-ticks')

    fig, ax = plt.subplots()

    for key,values in countieslist.items():
        x_fullcoords.append(values[0])
        y_fullcoords.append(values[1])
        cases.append(values[2])

    ax.scatter(x_fullcoords, y_fullcoords, c=cases, s=50, cmap='Blues')

    plt.xlabel("Longitude")
    plt.ylabel("Lattitude")

    ax = plt.gca()
    ax.set_ylim([-90,-70])

    plt.show()

def sample_section_counties(date, weighted, number):
    if number == 1:
        json_file_name = 'Cases_By_County.json'
    else:
        json_file_name = 'Cases_By_County_2.json'
    with open(json_file_name) as fp:
        json_data = json.load(fp)
        if not json_data.get(date) is None:
            countiesData = json_data[date]
        else:
            return None
        counties_list = {}
        for key,values in countiesData.items():
            if not weighted:
                counties_list[key] = values[0]
                # counties_list.append(tuple((key, values[0])))
            else:
                counties_list[key] = values[2]
                # cases.append(tuple((key, values[2])))
                #print(values[2])
        sorted_list = sorted(counties_list.items(), key=operator.itemgetter(1))
        sorted_list.reverse()
        #print(sorted_list)
        top_thirty = []
        mid_thirty = []
        last_thirty = []
        for i in range(len(sorted_list)-10):
            county, cases = sorted_list[i]
            if i<30:
                top_thirty.append(county)
            elif i<60:
                mid_thirty.append(county)
            else:
                last_thirty.append(county)
        data_top = []
        data_mid = []
        data_last = []
        with open("County_Location.csv", encoding='utf-8-sig') as csvf:
            csvReader= csv.DictReader(csvf)
            for rows in csvReader:
                if rows['County'] in top_thirty:
                    data_top.append([float(rows['X']), float(rows['Y'])])
                elif rows['County'] in mid_thirty:
                    data_mid.append([float(rows['X']), float(rows['Y'])])
                elif rows['County'] in last_thirty:
                    data_last.append([float(rows['X']), float(rows['Y'])])
#         print (data_top)
#         print (data_mid)
#         print (data_last)
        data_top = np.asarray(np.stack(data_top))
        data_mid = np.asarray(np.stack(data_mid))
        data_last = np.asarray(np.stack(data_last))
        return data_top

# sdate = date(2021,11,2)   # start date
sdate = date(2021, 9,11)   # start date (test)
edate = date(2021, 9, 11)   # end date

delta = edate - sdate       # as timedelta
date_array_unformatted = []
zero_array = []
first_array = []
total_cases_array = []
prevLandScape = []
avgL2NormLandscape = []
first = True

for i in range(delta.days + 1):

    day = sdate + timedelta(days=i)
    day = day.strftime("%#m/%#d/%Y")
    total_county_sample = 50
    
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
    total_diff = 0
    
    plot_counties(day, False)
    if first:
        prevLandScape = plot_landscapes(counties, prevLandScape, first)
        first = True
        continue
    else:
        for j in range(total_trials):
            # counties = sample_section_counties(day, True, 1)
            # print(counties)
            total_diff += plot_landscapes(counties, prevLandScape, first)[1]
        avgL2NormLandscape.append(total_diff / total_trials)
    
    prevLandScape = plot_landscapes(counties, prevLandScape, first)[0]

# print(avgL2NormLandscape)

# print(scipy.stats.pearsonr(avgL2NormLandscape, total_cases_array[1:]))
# date_array = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in date_array_unformatted]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
# plt.plot(avgL2NormLandscape)
# plt.show()