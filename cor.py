# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 12:11:27 2020
@author: MUHAMMADUsman
"""

import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(database="corona", user="postgres", password="admin", host="127.0.0.1", port="5432")

    cursor = connection.cursor()
    
    create_table_query = '''CREATE TABLE country
          (ID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          TOTAL_CASES         REAL,
          LATITUDE			REAL,
          LONGITUDE			REAL); '''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")