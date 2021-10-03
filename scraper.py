import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

from requests.models import Response

#function to get the desired position for the search
def get_position(position):
    position = input("What position are you searching for?")
    return position

#function to get the location of the search
def get_location(location):
    location = input("Where are you searching for this position?(city,state, zipcode)")
    return location

#Function to create the url of the site
def get_url(position, location):
    url_template = "https://www.indeed.com/jobs?q={}&l={}"
    url = url_template.format(position, location)
    return url

#Function to pull the different pieces of job data from the different listings
def record_collector(card):

    job_title = card.find('h2', 'jobTitle', 'title').text
    company_name = card.find('span', 'companyName').text.strip()
    company_location=card.find('div', 'companyLocation').text
    job_descrip=card.find('div', 'job-snippet').text
    job_date = card.find('span', 'date').text.strip()

# because not every job has a salary posted, there needs to be a conditional
    job_pay = card.find('class', 'salary-snippet')
    if job_pay:
        salary = job_pay.text
    else:
        salary = ''
    record = ( job_title, company_name, company_location, salary, job_date, job_descrip)
    return record
    

def main(position, location):
    records = []
    position = get_position(position)
    location = get_location(location)
    url = get_url(position, location)


    
    while True:

        page = requests.get(url)
    
        soup = BeautifulSoup(page.text, 'html.parser')

        cards = soup.find_all('div', 'slider_item')
        for card in cards:
            record = record_collector(card)
            records.append(record)
            print(record)
        #num = 10
        #To continue to the next page
        try:
            #url = f"https://www.indeed.com/jobs?q={position}&l={location}&start={num}"
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
        
        #break

    #print(records)
    #writes everything to a csv file
    with open(f'{position + location}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'Pay', 'Posted', 'Description.'])
        writer.writerows(records)
#print(records)
main('', '')
