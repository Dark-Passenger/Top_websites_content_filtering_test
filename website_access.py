from requests import get
from lxml.html import fromstring
from datetime import datetime
from requests.exceptions import ConnectionError
from csv import writer, reader
from itertools import islice
import os

website_list = "top-1m.csv"
filename = "results.csv"
cert_path = "SQTerminator.der"
websites = reader(open(website_list))
results = writer(open(filename,"w",newline=''))
proxy = {
    'http':'10.11.11.1:3128',
    'https':'10.11.11.1:3128'
    }

#Start calculating program running time
start_time = datetime.now().replace(microsecond=0)

#setup counters
website_counter = 0
blocked_counter = 0
not_blocked_counter = 0

def Stats():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    end_time = datetime.now().replace(microsecond=0)
    duration = end_time - start_time
    print("\n\t\t--Statistics--\n")
    print("Total running time :\t\t", duration)
    print("Total websites accessed :\t", website_counter)
    print("Total websites blocked :\t", blocked_counter)
    print("Total websites not blocked :\t", not_blocked_counter)

#Header block
results.writerow( ["WEBSITE NAME", "STATUS", "BLOCKED SITE", "CATEGORY"])

start_row = int(input("Starting row number: "))
end_row = int(input("Ending row number: "))

for website in islice(websites, start_row, end_row):

    name = "http://"+website[1]
    try :    
        webpage = get(name, proxies=proxy) # verify verify works else use cert=
        #webpage = get(name, verify = cert_path)
        #webpage = get(name, cert = cert_path)
        site_map = fromstring(webpage.content)
        website_counter = website_counter+1
    
        try:
            #Sites blocked
            result = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/h1/label//text()')[0]
            result = "Blocked"
            site = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()[1]')[0].replace(": ","",1)
            category = site_map.xpath('//*[@id="content"]/div[2]/div/div[2]/div[1]/div/strong/text()')[1].replace(": ","",1)
            blocked_counter=blocked_counter + 1
    
        except IndexError as e:
            #Oops sites not blocked
            result = "--"
            site = "--"
            category = "--"
            not_blocked_counter = not_blocked_counter + 1

    except ConnectionError :
    #Oops sites not blocked
        result = "not blocked"
        site = ""
        category = ""
        not_blocked_counter = not_blocked_counter + 1

    #Dumping into the file to have a report at the end
    results.writerow([website[1], result, site, category])

    if website_counter % 10 == 0:
        Stats()

Stats()
