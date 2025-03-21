import csv
import requests
import json

url = "https://7zb7o864ci.execute-api.us-east-1.amazonaws.com/prod/mp9-v3-autograder-test"

student = {
    "submitterEmail": "fridkis2@illinois.edu", #<Your coursera account email>
    "secret": "nXjxJiu7GIXroKl3" #<Your secret token from coursera>
}

etl3_job1 = [71870, 9, 7] #<The deliverable (array)for Glue job 3, task 1: deduplication
etl3_job2 = "C:\\Users\\Annjamin\\Documents\\Benj's Stuff\\UIUC MCS\\CS498-CloudComputingApplications\\CS498-CloudComputingApplications-MPs\\MP9\\Submission-Output\\TopTenRoutes.csv" #<The deliverable (string filepath) for Glue job 3, task 2: top n routes
etl3_job3 = "day" #<The deliverable (string) for Glue job 3, task 3: correlation

sql1_numFilteredEntries = 184 #<The count of the filtered entries from 3.3 SQL query 1>
sql2_numFilteredEntries = 1277 #<The count of the filtered entries from 3.3 SQL query 2>
sql3_numFilteredEntries = {"Night":50} #<The time of day with most average delay, and the correponding avergae delay as a dictionary from 3.3 SQL query 3>

viz0CsvPath = "" #<Filepath for your tableau viz0 csv/tsv file>
viz1CsvPath = "" #<Filepath for your tableau viz1 csv/tsv file>
viz2CsvPath = "" #<Filepath for your tableau viz2 csv/tsv file>

route = 0
count = 1

# The column ordering in the tsv file may not be preserved when you export the data.
# Therefore, please check and modify the respective column index below

viz0DestAirportColumn = 0 # <index of 'Destination Airport' column (0-indexed)>
viz0CountAirlineColumn = 1 # <index of 'Count of Airline' column (0-indexed)>
viz0LatitudeColumn = 2 # <index of 'Latitude' column (0-indexed)>
viz0LongitudeColumn = 3 # <index of 'Longitude' column (0-indexed)>

viz1StopOverColumn = 0 # <0 if the first column is the airport title, else 1>
viz2ArrivalDelayColumn = 0 # <0 if the first column is the arrival delay, else 1>

def route_analysis(filePath, route, count):
    topndata = {}

    with  open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter=',') 

        header = reader.__next__()

        for row in reader:
            if len(row) == 2:
                topndata[row[route]] = str(row[count])
    return topndata

def readViz0(filePath, destAirportColumn, countAirlineColumn, latitudeColumn, longitudeColumn):
    vizData = {}

    with  open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter='\t')

        header = reader.__next__()

        for row in reader:
            if len(row) == 4:
                vizData[row[destAirportColumn]] = [str(row[countAirlineColumn]), str(row[latitudeColumn]), str(row[longitudeColumn])]

    return vizData

def readViz12(filePath, keyColumn):
    vizData = {}
    valueColumn = int(not keyColumn)

    with  open(filePath, encoding="utf8", errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0','') for line in csvfile), delimiter='\t')

        header = reader.__next__()

        for row in reader:
            if len(row) == 2:
                vizData[row[keyColumn]] = int(row[valueColumn])

    return vizData

def sendToAutograder(payload):
    r = requests.post(url, data=json.dumps(payload))
    print(r.status_code, r.reason)
    print(r.text)

def main():
    topndata = route_analysis(etl3_job2, route, count)
    viz0Data = {} # readViz0(viz0CsvPath, viz0DestAirportColumn, viz0CountAirlineColumn, viz0LatitudeColumn, viz0LongitudeColumn)
    viz1Data = {} # readViz12(viz1CsvPath, viz1StopOverColumn)
    viz2Data = {} # readViz12(viz2CsvPath, viz2ArrivalDelayColumn)

    payload = {}
    payload['student'] = student
    # added in v3
    payload['etl3_job1'] = etl3_job1
    payload['etl3_job2'] = topndata
    payload['etl3_job3'] = etl3_job3
    payload['sql3_numFilteredEntries'] = sql3_numFilteredEntries # is a dictionary
    # end
    payload['sql1_numFilteredEntries'] = sql1_numFilteredEntries
    payload['sql2_numFilteredEntries'] = sql2_numFilteredEntries
    payload['viz0'] = viz0Data
    payload['viz1'] = viz1Data
    payload['viz2'] = viz2Data
    print(json.dumps(payload))
    sendToAutograder(payload)

if __name__== "__main__":
    main()