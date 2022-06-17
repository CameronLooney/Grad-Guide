from itertools import product
from scrap_data import scrap_data
import streamlit as st
def all_param_combinations(job,location):
    combination_list = list(product(job, location))
    return combination_list


def preprocess_for_url(list):
    '''
    :param list: list
    :return: list with white spaces replaced with + and converted to lowercase
    '''
    for i in range(len(list)):
        list[i] = list[i].strip().lower() # remove white spaces
        list[i]="+".join([x for x in list[i].split(" ") if x]) # replace white spaces with +

    return list

def print_table(df):
    st.subheader("Table Example")
    df["key"] = df["Job Title"]+df["Job Company"]+df["Job Location"]
    # drop duplicates based on key keep first
    df = df.drop_duplicates(["key"], keep='first')
    # drop the key column
    df = df.drop(columns=["key"])
    return st.write(df.to_html(escape=False), unsafe_allow_html=True)





