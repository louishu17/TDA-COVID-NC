import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
	return


if __name__ == "__main__":
    # Driver Code

    # Decide the two file paths according to your
    # computer system
    #csvFilePath = r'Cases_And_Deaths_By_County.csv'
    csvFilePath = r'covid_cases_2.csv'
    jsonFilePath = r'Cases_By_County.json'

    with open('Cases_And_Deaths_By_County.csv', encoding='utf-16', newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        data_set = {}
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
            cases = temp2[2]
            deaths = temp2[3]
            
            #create a json
            if date not in data_set:
                data_set[date] = {county:[int(cases), int(deaths)]}
            elif county not in data_set[date]:
                data_set[date][county] = [int(cases), int(deaths)]

        with open("Cases_By_County.json", "w") as outfile:
            json.dump(data_set, outfile)
                

