
# coding: utf-8

# In[6]:


import requests
import numpy as np
import json 
import csv
from urllib.request import urlopen
import numpy as np
import json
from pygeocoder import Geocoder
import pandas as pd
import datetime
import tzlocal  # $ pip install tzlocal
import xml.etree.ElementTree as ET 
def main(req,req1):
    
    
    def getplace(lat, lon):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=true&key=AIzaSyCD1CzClGEI3LmcYIXtV0LCNhpc4A86wa8" % (lat, lon)
        v = urlopen(url).read()
        j = json.loads(v)
        #print(j)
        components = j['results'][0]['address_components']
        town = None
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
            if "locality" in c['types']:
                town = c['long_name']
    
        return town
    
    def make_city_totals(transactions):
    
        datafile = open('transactions.csv', 'r')
        datareader = csv.reader(datafile, delimiter=',')
        city_totals = open('./city_totals.csv', 'w')
        csvwriter1 = csv.writer(city_totals)
        data = []
        for row in datareader:
            if not(len(row) ==0):
                data.append(row)  
        #x = data[0][0].split(",")
        data = np.array(data)[1:]
        city_name = data[:,5]
        city_totals_header = ['City_Name','Total_Amount','Unique_Customers','Total_Transactions']
        city_name = list(set(city_name))
        csvwriter1.writerow(city_totals_header)
        city_row = []

        for j in range(len(city_name)):
            Total_Transactions = 0
            Total_Amount = 0
            Unique_Customers = []
            city_row = []
            print(city_name[j])
            for i in range(data.shape[0]):
                if (data[i][5] == city_name[j]):
            
                    Total_Transactions = Total_Transactions + 1
                    Total_Amount = Total_Amount + float(data[i][4]) 
                    Unique_Customers.append(data[i][2])
            city_row.append(city_name[j])
            uni_cust = list(set(Unique_Customers))
            print(len(uni_cust))
            city_row.append(Total_Amount)
            city_row.append(len(uni_cust))
            city_row.append(Total_Transactions)
            csvwriter1.writerow(city_row)
            
            
            
    
    root = ET.fromstring(req1.content)
    
    
    # open a file for writing

    transactions = open('./transactions.csv', 'w')
    
    # create the csv writer object

    csvwriter = csv.writer(transactions)
    transaction_header = ["Transaction_Id","DateTime","Customer_Id","Customer_Name","Amount","City_name"]
    
    csvwriter.writerow(transaction_header)
    
    transaction_row = []
    
    
    # making dictionary of customers  
    index = 0
    customer_list = []
    for child in root.iter('*'):
        #customer_list[child.text] = child.text
        #print(child.tag,child.text)
        if (not(child.tag == 'customers')):
            if (not(child.tag == 'customer')):
                customer_list.append(child.text)  
    customer_list = np.array(customer_list).reshape(-1,2)
    #print(customer_list[0][0])
    json_response = json.loads(req.content)
    for transaction in range(len(json_response)):
        transaction_row.append(transaction+1)
        
        ts = json_response[transaction].get("timestamp")
        ts = str(ts)
        ts = ts[:10]
        ts = int(ts)
        
        readable = datetime.datetime.fromtimestamp(ts).isoformat()
        
        transaction_row.append(readable)
        
        transaction_row.append(json_response[transaction].get("customerId"))
        id_ = json_response[transaction].get("customerId")
        #print(type(id_))
        for i in range(customer_list.shape[0]):
            if (customer_list[i][0] == str(id_)):
                name = customer_list[i][1]
                #print(name)
                transaction_row.append(name)
            
            #if (child.text == id):
        # printing the city name using lat and long 
        transaction_row.append(json_response[transaction].get("amount"))
        lat = json_response[transaction].get("latitude")
        long = json_response[transaction].get("longitude")
        #print(getplace(lat, long))
        city = getplace(lat, long)
        #print(city)
        transaction_row.append(city)
        csvwriter.writerow(transaction_row)
        transaction_row = []
    
    transactions.close()
    make_city_totals('transactions.csv')


# In[7]:



req = requests.get('https://df-alpha.bk.rw/interview01/transactions')
    
req1 = requests.get('https://df-alpha.bk.rw/interview01/customers')
main(req,req1)


# In[ ]:


pwd

