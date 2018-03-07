import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

print('JOB POSTINGS SCRAPER')

URL = "https://www.indeed.ca/jobs?q=sustainability%2C+environment&l=Toronto%2C+ON"
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")


def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
	    jobs.append(a["title"])
  return(jobs)

jobs = extract_job_title_from_result(soup)
print(jobs)