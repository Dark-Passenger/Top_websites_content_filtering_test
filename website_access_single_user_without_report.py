from __future__ import print_function, division
from requests import get
from lxml.html import fromstring
from datetime import datetime
from requests.exceptions import ConnectionError
from csv import reader
from itertools import islice
from os import system, name

filename = "top-1m.csv"
websites = reader(open(filename))

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
            #Site blocked
            result = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/h1/label//text()')[0]
            site = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()[1]')[0]
            category = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()')[1]
            blocked_counter=blocked_counter + 1
    
        except IndexError as e:
            #Oops site not blocked
            not_blocked_counter = not_blocked_counter + 1

    except ConnectionError :
    #connection error
        error_counter = error_counter + 1

    if website_counter % 10 == 0:
        Stats()

Stats()
