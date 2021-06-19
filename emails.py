import csv
import requests
import time
from bs4 import BeautifulSoup

# Method to get the name and email of a society
def getData(link):

    # Deals with occasional requests error
    try:
        socPage = requests.get(base_url + link['href'])
    except:
        time.sleep(5)
        getData(link)
        return
    
    tempSoup = BeautifulSoup(socPage.text, 'html.parser')
    emailLink = tempSoup.find("a", class_="msl_email")

    # Not all society pages have an email
    try:
        mailTo = emailLink['href']
    except:
        return

    # Eliminated the 'mailto:' part before the actual email
    email = (mailTo.split(':'))[1]

    title = tempSoup.find('li', class_="current-page")
    name = title.get_text()
    myData.append([name, email])

# url needed later
base_url = "https://www.warwicksu.com"

# Conatins the list of all the societies
suPage = "https://www.warwicksu.com/societies-sports/societies/"

source = requests.get(suPage)
soup = BeautifulSoup(source.text, 'html.parser')

# A list to store the data
myData = [["Name", "Email"]]

for links in soup.find_all('a', class_="msl-gl-link"):
    # links contains the url for each society's page
    getData(links)

# writes myData to csv file using csv library
with open('emails.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerows(myData)