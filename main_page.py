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

st.set_page_config(page_title = "Grad Guide", layout='wide')
def main_page():
    def email_df(df,email):
        try:

            send_email(df,email)
            return True
        except:
            return False

    st.title("Grad Guide")
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
                key='1')

            location = st.multiselect(
                'Select Location',
                ['Antrim', 'Armagh', 'Carlow', 'Cavan', 'Clare', 'Cork', 'Derry', 'Donegal', 'Down', 'Dublin',
                 'Fermanagh',
                 'Galway', 'Kerry', 'Kildare', 'Kilkenny', 'Laois', 'Leitrim', 'Limerick', 'Longford', 'Louth', 'Mayo',
                 'Meath',
                 'Monaghan', 'Offaly', 'Roscommon', 'Sligo', 'Tipperary', 'Tyrone', 'Waterford', 'Westmeath', 'Wexford',
                 'Wicklow']
                ,
                [])
            email = st.text_input("Enter your email address to recieve the results")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
    if submitted:
        if resume is not None:
            key_phrases = process_resume(resume,5-len(job))
            job.extend(key_phrases)


        job = preprocess_for_url(job)
        query_data = all_param_combinations(job, location)
        job_dataframes = []
        for query in query_data:
           job_dataframes.append(scrap_data(query[0], query[1]))
        df = pd.concat(job_dataframes)
        df = df.drop_duplicates(
            ["job_title", "job_company", "job_location", "job_summary", "job_additional_info", "job_date",
             "current_date"], keep='first').reset_index(drop=True)
        print_table(df.head(5))
        if email is not None:
            email_df(df,email)
        df_csv = convert_url_for_csv(df)
        buffer = excel(df_csv)
        with st.sidebar:
            st.download_button(
                label="Download your Jobs",
                data=buffer,
                file_name="Jobs.xlsx",
                mime="application/vnd.ms-excel"
            )



















main_page()