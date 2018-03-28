# coding: utf-8

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

def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        companies.append(span.text.strip())
  return(companies)

def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return(locations)

def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    try:
      salaries.append(div.find('nobr').text)
    except:
      try:
        div_two = div.find(name="div", attrs={"class":"sjcl"})
        div_three = div_two.find("div")
        salaries.append(div_three.text.strip())
      except:
        salaries.append("Nothing_found")
  return(salaries)

def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll('span', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)



## Scrape

max_results_per_city = 100
city_set = ['Toronto', 'Waterloo']
columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns = columns)

## TODO: clean this code, move into functions, use more variables
for city in city_set:
  for start in range(0, max_results_per_city, 10):
    page = requests.get('http://www.indeed.com/jobs?q=sustainability%2C+environment&l=' + str(city) + '&start=' + str(start))
    time.sleep(1)  #ensuring at least 1 second between page grabs
    soup = BeautifulSoup(page.text, "html.parser")
    for div in soup.find_all(name="div", attrs={"class":"row"}): 
      #specifying row num for index of job posting in dataframe
      num = (len(sample_df) + 1) 
      #creating an empty list to hold the data for each posting
      job_post = [] 
      #append city name
      job_post.append(city) 
      #grabbing job title
      for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
        job_post.append(a["title"]) 
      #grabbing company name
      company = div.find_all(name="span", attrs={"class":"company"}) 
      if len(company) > 0: 
        for b in company:
          job_post.append(b.text.strip()) 
      else: 
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
          job_post.append(span.text) 
      #grabbing location name
      c = div.findAll('span', attrs={'class': 'location'}) 
      for span in c: 
        job_post.append(span.text) 
      #grabbing summary text
      d = div.findAll('span', attrs={'class': 'summary'}) 
      for span in d:
        job_post.append(span.text.strip()) 
      #grabbing salary
      try:
        job_post.append(div.find('nobr').text) 
      except:
        try:
          div_two = div.find(name="div", attrs={"class":"sjcl"}) 
          div_three = div_two.find("div") 
          job_post.append(div_three.text.strip())
        except:
          job_post.append("Nothing_found") 
      #appending list of job post info to dataframe at index num
      sample_df.loc[num] = job_post

#saving sample_df as a local csv file — define your own local path to save contents 
sample_df.to_csv("C:\Users\Business Co-op\Desktop\Lindsay\Random\Job Postings Scraper\postings.csv", encoding='utf-8')