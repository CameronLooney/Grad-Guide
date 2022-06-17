# streamlit app that takes job title and location from user

import streamlit as st
from streamlit_tags import st_tags
from resume_parser import process_resume
from form import preprocess_for_url,all_param_combinations,print_table
from scrap_data import scrap_data
import pandas as pd
from csv_download import excel, convert_url_for_csv
from email_sender import send_email
from time import sleep
# from st_aggrid import AgGrid

st.set_page_config(page_title = "Grad Guide", layout='wide') # wide, boxed, tall, fullscreen
def main_page():
    def email_df(df,email):
        try:
            # send email with the dataframe
            send_email(df,email)
            return True
        except:
            return False

    st.title("Grad Guide",page_icon="chart_with_upwards_trend") # set the title of the page
    with st.sidebar:
        st.title("Enter your Search Criteria")
        with st.form("my_form"):
            resume = st.file_uploader("Upload your resume for additional keywords", type=["pdf"])


            job = st_tags(
                label='Enter Keywords / Job Titles:',
                text='Press enter to add more',
                value=[],
                suggestions=[],
                maxtags=10,
                key='1') # set the tags for the job title

            location = st.multiselect(
                'Select Location',
                ['Antrim', 'Armagh', 'Carlow', 'Cavan', 'Clare', 'Cork', 'Derry', 'Donegal', 'Down', 'Dublin',
                 'Fermanagh',
                 'Galway', 'Kerry', 'Kildare', 'Kilkenny', 'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth', 'Mayo',
                 'Meath',
                 'Monaghan', 'Offaly', 'Roscommon', 'Sligo', 'Tipperary', 'Tyrone', 'Waterford', 'Westmeath', 'Wexford',
                 'Wicklow']
                ,
                [])# set the tags for the location
            email = st.text_input("Enter your email address to get the results")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
    if submitted:# if the submit button is pressed
        if location is None:
            st.error("Please select at least one location") # if there is no location, show an error
        if job is None and resume is None:
            st.error("Please enter at least one job title or update a CV") # if there is no job title, show an error
        if resume is not None:
            key_phrases = process_resume(resume,5-len(job)) # get the key phrases from the resume
            job.extend(key_phrases) # add the key phrases to the job title


        job = preprocess_for_url(job) # preprocess the job title and location
        query_data = all_param_combinations(job, location) # get all the combinations of job title and location
        job_dataframes = []
        for query in query_data:
           job_dataframes.append(scrap_data(query[0], query[1])) # get the data from the website
        df = pd.concat(job_dataframes) # concatenate all the dataframes
        df = df.drop_duplicates(
            ["Job Title", "Job Company", "Job Location", "Job Summary", "Job Additional Info", "Job Date",
             "Current Date"], keep='first').reset_index(drop=True) # drop duplicates and reset the index
        print_table(df.head(5))
        if email is not None:
            email_df(df,email) # send the dataframe to the email address
        df_csv = convert_url_for_csv(df) # convert the dataframe to csv
        buffer = excel(df_csv) # convert the dataframe to excel
        with st.sidebar:
            st.download_button(
                label="Download your Jobs",
                data=buffer,
                file_name="Jobs.xlsx",
                mime="application/vnd.ms-excel"
            ) # download the dataframe to excel






main_page()