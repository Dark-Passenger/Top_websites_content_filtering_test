from __future__ import print_function, division
from requests import get
from requests.exceptions import ConnectionError
from lxml.html import fromstring
from datetime import datetime
from itertools import islice
from csv import reader
from os import system, name
from threading import Thread
from Queue import Queue

#Thread Variables
Users = 33
queue = Queue(Users * 2)

#URL Resources
filename = "top-1m.csv"
file = open(filename, 'r')
urls = reader(file)
proxy = {
    'http':'10.11.11.1:3128',
    'https':'10.11.11.1:3128'
    }

#setup counters
website_counter = 0
blocked_counter = 0
not_blocked_counter = 0
Error_counter = 0
response_list = []

#Give user importance
start_row = int(input("Starting row number: "))
end_row = int(input("Ending row number: "))

#Setup url queue:
for url in islice(urls, start_row, end_row):
    queue.put("http://"+url[1])
file.close()

def Stats():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

    end_time = datetime.now().replace(microsecond=0)
    duration = end_time - start_time
    avg_response_time = sum(response_list)/len(response_list)

    print("\n\t\t--Statistics--\n")
    print("Total running time :\t\t", duration)
    print("Total websites accessed :\t", website_counter)
    print("Total websites blocked :\t", blocked_counter)
    print("Total websites not blocked :\t", not_blocked_counter)
    print("Total websites that timedout :\t", Error_counter)
    print("Average response time in microseconds :\t",avg_response_time)

def WebsiteAccess():
    while true:
        website = "http://"+q.get()
        website_counter = website_counter+1
        try :    
            webpage = get(website, proxies=proxy)
            site_map = fromstring(webpage.content)
            response_list.append(webpage.elapsed.microseconds)
            try:
                #Sites blocked
                result = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/h1/label//text()')[0]
                site = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()[1]')[0]
                category = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()')[1]
                blocked_counter=blocked_counter + 1
    
            except IndexError as e:
                not_blocked_counter = not_blocked_counter + 1

        except ConnectionError :
            #Oops sites not blocked
            Error_counter = Error_counter + 1

        if website_counter % 10 == 0:
            Stats()
        queue.task_done()

#Start calculating program running time
start_time = datetime.now().replace(microsecond=0)    

for index in range(Users):

    user = Thread(target=WebsiteAccess)
    #thread = Thread(target=WebsiteAccess, daemon=True) #Uncomment if daemon threads are nessary
    user.start()

#threads spawned now wait for finale
queue.join()

Stats()