# importing the requests library 
import requests 
import psycopg2
from psycopg2 import Error
# api-endpoint 
URL = "https://pomber.github.io/covid19/timeseries.json"

# sending get request and saving the response as response object 
r = requests.get(url = URL) 

# extracting data in json format 
data = r.json() 
# https://ourworldindata.org/coronavirus-testing-source-data
country_info = {}
#print(data.keys())

sum = 0

for country in sorted(data.keys()):
	for index in range(0,len(data[country])):
		sum = sum + data[country][index]["confirmed"]
	#print country , ' = ' , sum , '\n'
	country_info[country] = sum
	sum=0

#print(country_info)


import json

with open('countries.json') as f:
  data = json.load(f)

country = {}

for index in range(0,len(data["data"])):
	temp = {}
	temp["latitude"] = data["data"][index][1]
	temp["longitude"] = data["data"][index][2]
	country[data["data"][index][0]] = temp


try:
   connection = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")
   cursor = connection.cursor()

   postgres_insert_query = """ INSERT INTO country (ID, NAME, TOTAL_CASES, LATITUDE, LONGITUDE) VALUES (%s,%s,%s,%s,%s)"""
   id = 0
   for key in country_info.keys():
   		id = id + 1
   		if key in country.keys():
   			record_to_insert = (id, key, country_info[key], country[key]["latitude"], country[key]["longitude"])
   		else:
   			record_to_insert = (id, key, country_info[key], 0, 0)
   		cursor.execute(postgres_insert_query, record_to_insert)

   connection.commit()
   count = cursor.rowcount
   print (count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")