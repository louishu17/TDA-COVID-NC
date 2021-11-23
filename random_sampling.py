import json
import random
from numpy.random import choice

def sample_counties(date, x):
    with open('Cases_By_County.json') as fp:
        countiesData = json.load(fp)[date]
        cases = []
        counties = []

        
        for key,values in countiesData.items():
            counties.append(key)
            cases.append(values[2])

        # total = sum(cases)
        # print(total)
        # for i in range(len(cases)):
        #     cases[i] = cases[i] / total

        print(cases)
        # for c in counties:
        #     cases.append(counties[c])
        print(choice(counties, x, p= cases,replace=False))
        
sample_counties("11/7/2021", 5)