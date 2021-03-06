from __future__ import print_function, division
from sys import version_info
from requests import get
from lxml.html import fromstring
from datetime import datetime
from requests.exceptions import ConnectionError
from csv import writer, reader
from itertools import islice
from os import system, name

website_list = "top-1m.csv"
filename = "results.csv"
websites = reader(open(website_list))
if version_info.major == 3:
    results = writer(open(filename,"w",newline=''))
else:
    results = writer(open(filename,"w"))
proxy = {
    'http':'10.11.11.1:3128',
    'https':'10.11.11.1:3128'
    }

#setup counters
website_counter = 0
blocked_counter = 0
not_blocked_counter = 0
error_counter = 0
response_time = []

def Stats():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    end_time = datetime.now().replace(microsecond=0)
    duration = end_time - start_time
    avg_response_time = sum(response_time)/len(response_time)
    print("\n\t\t--Statistics--\n")
    print("Total running time :\t\t", duration)
    print("Total websites accessed :\t", website_counter)
    print("Total websites blocked :\t", blocked_counter)
    print("Total websites not blocked :\t", not_blocked_counter)
    print("Totol websites closed with error :\t",error_counter)
    print("Average Response time :\t",avg_response_time)

#Header block
results.writerow( ["WEBSITE NAME", "STATUS", "BLOCKED SITE", "CATEGORY", "RESPONSE TIME"])

start_row = int(input("Starting row number: "))
end_row = int(input("Ending row number: "))

#Start calculating program running time
start_time = datetime.now().replace(microsecond=0)

for website in islice(websites, start_row, end_row):

    website_name = "http://"+website[1]
    website_counter = website_counter+1
    try :    
        webpage = get(website_name, proxies=proxy)
        site_map = fromstring(webpage.content)
        response_time.append(webpage.elapsed.microseconds)
    
        try:
            #Sites blocked
            result = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/h1/label//text()')[0]
            result = "Blocked"
            site = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()[1]')[0].replace(": ","",1)
            category = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()')[1].replace(": ","",1)
            blocked_counter=blocked_counter + 1
    
        except IndexError as e:
            #Oops sites not blocked
            result = "Not Blocked"
            site = "--"
            category = "--"
            not_blocked_counter = not_blocked_counter + 1

    except ConnectionError :
    #Oops sites not blocked
        result = "Error"
        site = "--"
        category = "--"
        error_counter = error_counter + 1

    #Dumping into the file to have a report at the end
    results.writerow([website[1], result, site, category,response_time[-1])

    if website_counter % 10 == 0:
        Stats()

Stats()
