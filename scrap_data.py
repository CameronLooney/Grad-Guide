import csv
from datetime import datetime
import requests
import bs4 as bs
import pandas as pd

# ID = ceeafa80939cc7ab5d71fbd1ce306362690d1b8988bdb73a77cfc077cc3341dc
# password = 6a1Ehe7JMq6PGpdNzbS3m71OuO8A7nFaxV8ieR4cA2cTfyPvkphTbQOOEH0yQDkn


def scrap_data(job,location):

    def get_url(position, location):
        '''
        :param position: position to search for (e.g. "data scientist")
        :param location: location to search for (e.g. "Dublin")
        :return: url to search for jobs
        '''

        url_template = "https://ie.indeed.com/jobs?q={}&l={}" # url template
        url = url_template.format(position, location) # url to search for jobs
        print(url)
        return url


    def get_job_details(card):
        '''
        :param card: card to extract job details from Indeed
        :return: job details
        '''
        # get the a tag from the card
        atag = card.h2.a
        # get the title from the a tag
        job_title = atag.span.get("title")
        # get the link from the a tag
        job_link = "https://ie.indeed.com" + atag.get("href")
        # get the company from the card
        job_company = card.find("span", class_="companyName").get_text()
        # get the location from the card
        job_location = card.find("div", "companyLocation").get_text()
        # get the summary from the card
        job_summary = card.find("div", "job-snippet").get_text().strip().strip('\n')
        # get the date from the card
        job_date = card.find("span", class_="date").get_text()
        current_date = datetime.today().strftime("%d/%m/%Y") # get the current date

        try: # try to get the additional info from the card
            job_additional_info = card.find("div", "attribute_snippet").get_text() # get the additional info
        except: # if there is no additional info, set it to None
            job_additional_info = ""
        return (job_title, job_company, job_location, job_summary, job_additional_info, job_date, current_date,job_link)


    def fetch_data(position,location):
        '''
        :param position: position to search for (e.g. "data scientist")
        :param location: location to search for (e.g. "Dublin")
        :return: dataframe of jobs
        '''
        records = [] # list to store the jobs
        url = get_url(position,location) # get the url to search for jobs
        while True: # loop until there are no more jobs
            response = requests.get(url) # get the response from the url
            soup = bs.BeautifulSoup(response.text, "html.parser") # parse the response
            cards = soup.find_all("div", class_="cardOutline") # get the cards from the response
            for card in cards: # for each card
                job_details = get_job_details(card) # get the job details
                records.append(job_details) # append the job details to the list
            try: # try to get the next page
                url = "https://ie.indeed.com" + soup.find("a",{'aria-label':'Next'}).get("href")


            except: # if there is no next page, break the loop
                break
        return records

    def convert_to_df():
        '''
        :param data: data to convert to dataframe
        :return: dataframe of jobs
        '''
        data = fetch_data(job,location) # get the data
        df = pd.DataFrame(data,
                          columns=["Job Title", "Job Company", "Job Location", "Job Summary", "Job Additional Info",
                                   "Job Date", "Current Date", "Job Link"]) # convert the data to a dataframe
        df = df.drop_duplicates(
            ["Job Title", "Job Company", "Job Location", "Job Summary", "Job Additional Info","Job Date",
             "Current Date"], keep='first') # drop duplicates
        return df

    def set_current_date():
        df = convert_to_df() # get the dataframe
        todays_date = datetime.today().strftime('%d/%m/%Y') # get the current date
        df_complete = df[df['Current Date'] == todays_date].reset_index(drop=True) # get the jobs from the current date
        return df_complete # return the jobs from the current date


    def drop_old_jobs():
        df_complete = set_current_date()
        df_complete = df_complete[~df_complete['Job Date'].isin(['Posted30+ days ago'])] # drop the jobs that are posted 30+ days ago
        df_complete['Job Link'] = '<a href=' + df_complete['Job Link'] +\
                                  '><div>' + df_complete['Job Company'] + '</div></a>' # add a link to the job company
        return df_complete
    df = drop_old_jobs()
    return df





