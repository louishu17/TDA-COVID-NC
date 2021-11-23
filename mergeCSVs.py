import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json():
    csvFilePath = r'covid_cases_2.csv'
    jsonFilePath = r'Cases_By_County.json'

    population_density = []

    with open('County_Location.csv', encoding='utf-8', newline='\n') as countycsvfile:
        countyreader = csv.reader(countycsvfile)

        for row in countyreader:
            # temp = '\t'.join(row)
            # temp2 = temp.split('t')
            # print(row)
            # print(temp2)
            population_density.append(float(row[3].replace(',','')))


    with open('Cases_and_Deaths_By_County.csv', encoding='utf-16', newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data_set = {}
        total_cases = []
        total_deaths = []
        weighted_cases = 0
        weighted_deaths = 0

        for row in spamreader:
            temp = '\t'.join(row)
            temp2 = temp.split('\t')

            #get rid of row number
            temp2.pop(0)

            #because Mcdowell is weird
            if temp2[1] != 'McDowell':
                temp2.pop(2)
            #print(temp2)

            date = temp2[0]
            county = temp2[1]
            cases = int(temp2[2])
            deaths = int(temp2[3])

            #create a json

            if date not in data_set:
                data_set[date] = {county:[cases, deaths, weighted_cases, weighted_deaths]}
                total_cases.append(cases)
                total_deaths.append(deaths)
            elif county not in data_set[date]:
                data_set[date][county] = [cases, deaths, weighted_cases, weighted_deaths]
                total_cases[-1] += cases
                total_deaths[-1] += deaths
        mylist = data_set.keys()

        weighted_avg_cases = [0]*179*100
        weighted_avg_deaths = [0]*179*100
        
        i = 0
        checker = 0
        for date in mylist:
            for idx, county in enumerate(data_set[date].keys()):
                case_and_death_data = data_set[date][county]
                case_and_death_data[2] = case_and_death_data[0]/population_density[idx]
                if total_deaths[i] == 0:
                    continue
                case_and_death_data[3] = case_and_death_data[1]/population_density[idx]
            i+=1
        with open("Cases_By_County.json", "w") as outfile:
            json.dump(data_set, outfile)
    return


if __name__ == "__main__":
    make_json()
