import requests
import csv
from bs4 import BeautifulSoup
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
def record_collector(slider):

    job_title = slider.find('h2', 'jobTitle', 'title').text.strip()
    company_name = slider.find('span', 'companyName').text.strip()
    company_location=slider.find('div', 'companyLocation').text.strip()
    job_descrip=slider.find('div', 'job-snippet').text.strip()
    job_date = slider.find('span', 'date').text.strip()

# because not every job has a salary posted, there needs to be a conditional
    job_pay = slider.find('class', 'salary-snippet')
    if job_pay:
        salary = job_pay.text
    else:
        salary = ''
    record = ( job_title, company_name, company_location, salary, job_date, job_descrip)
    return record
    
#main function to run everything
def main(position, location):
    records = []
    position = get_position(position)
    location = get_location(location)
    url = get_url(position, location)


    #while statement that allows the files to record while there are some
    while True:

        page = requests.get(url)
    
        whole_page = BeautifulSoup(page.text, 'html.parser')

        sliders = whole_page.find_all('div', 'slider_item')
        #goes through each slider and extracts the necessary information
        for slider in sliders:
            record = record_collector(slider)
            records.append(record)
            #print(record)
        #num = 10
        #To continue to the next page
        try:
            #url = f"https://www.indeed.com/jobs?q={position}&l={location}&start={num}"
            url = 'https://www.indeed.com' + whole_page.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
        
    # A check to see if there is a captcha in effect or if there wasn't any information that was inputed   
    if records == 0:
        print("The program was unable to detect any information. Check to ensure there isn't a captcha in effect")
        exit
    else:
    #writes everything to a csv file
        with open(f'{position + location}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['JobTitle', 'Company', 'Location', 'Pay', 'Posted', 'Description.'])
            writer.writerows(records)


main('', '')
