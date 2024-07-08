# -*- coding: utf-8 -*-
"""
@author: Akshay Suresh Phadtare
"""

import requests
from bs4 import BeautifulSoup

# Session started
session = requests.Session()

# URL of the page with the form
form_page_url = 'https://jamabandi.nic.in/land%20records/NakalRecord'

# Headers (if necessary)
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br, zstd',
    'Accept-Language':'en-US,en;q=0.9',
    'Referer':'https://jamabandi.nic.in/land%20records/NakalRecord',
    'Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'Sec-Ch-Ua-Platform':'"Windows"',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# To get the initial form page to retrieve hidden fields viewstate, viewstate_generator, event_validation
response = session.get(form_page_url, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraction of hidden fields
viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
viewstate_generator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

#2
district_code = input('Please enter district code')
tehsil_code = input('Please enter tehsil code')
village_code = input('Please enter village code')
jamabandi_year = [option['value'] for option in soup.find('select', {'name': 'ctl00$ContentPlaceHolder1$ddlPeriod'}).find_all('option')]
survey_number = input('Please enter survey number')

# Form data with selected dropdown options is created
form_data = {
    'ctl00$ContentPlaceHolder1$a': 'RdobtnKhasra',     # Selecting the radio button
    'ctl00$ContentPlaceHolder1$ddldname':str(district_code),         # district
    'ctl00$ContentPlaceHolder1$ddltname':str(tehsil_code),        # taluka
    'ctl00$ContentPlaceHolder1$ddlvname':str(village_code),      # village
    'ctl00$ContentPlaceHolder1$ddlPeriod':'2019-2020', # jamabandi year
    'ctl00$ContentPlaceHolder1$ddlkhasra':str(survey_number),    # khasra
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstate_generator,
    '__EVENTVALIDATION': event_validation,
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': ''
}

# URL of the form action (Same as form_page_url)
form_action_url = 'https://jamabandi.nic.in/land%20records/NakalRecord'

# Sending the POST request to select the dropdown options
response = session.post(form_action_url, headers=headers, data=form_data)
soup = BeautifulSoup(response.text, 'html.parser')
print("Form submission response:", response.status_code)

#3

# Finding the nakal button presence that appears after selecting dropdowns
button = soup.find('a', {'href': "javascript:__doPostBack('ctl00$ContentPlaceHolder1$GridView1','Select$0')"})

if button:
    print("Button found, simulating click...")
    
    # Updating the form data to simulate the __doPostBack event
    form_data.update({
        '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$GridView1',
        '__EVENTARGUMENT': 'Select$0',
        '__VIEWSTATE': soup.find('input', {'name': '__VIEWSTATE'})['value'],
        '__VIEWSTATEGENERATOR': soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
        '__EVENTVALIDATION': soup.find('input', {'name': '__EVENTVALIDATION'})['value'],
    })

    # Sending the POST request to trigger the postback
    response = session.post(form_action_url, headers=headers, data=form_data)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Postback response:", response.status_code)

    # Extracting a URL from an anchor tag with target="_blank"
    new_tab_url = soup.find('a', {'target': '_blank'})['href']

    print("New tab URL:", new_tab_url)

    # Making the request to the new tab URL
    new_tab_response = session.get(new_tab_url, headers=headers)
    new_tab_soup = BeautifulSoup(new_tab_response.text, 'html.parser')
    print("New tab response:", new_tab_response.status_code)

    # Extracting data from a table in the report
    table = new_tab_soup.find('table')
    data = []

    if table:
        headers = [header.text for header in table.find_all('th')]
        rows = table.find_all('tr')
        
        for row in rows:
            columns = row.find_all('td')
            data.append([column.text for column in columns])

    print("Extracted data:", data)
else:
    print("Button not found after selecting dropdown options.")

