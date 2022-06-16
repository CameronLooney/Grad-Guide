import pandas as pd
import streamlit as st
import re



def excel(excl_merged):
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, date_format='dd/mm/yyyy', datetime_format='dd/mm/yyyy',engine = 'xlsxwriter') as writer:

        excl_merged.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        workbook = writer.book
        format = workbook.add_format({'text_wrap': True})
        worksheet.set_column('A:H', None, format)

        # Get the dimensions of the dataframe.
        (max_row, max_col) = excl_merged.shape

        # Set the column widths, to make the dates clearer.
        worksheet.set_column(1, max_col, 25)
        writer.save()
    return buffer


def process_url_for_csv(row):
    row["job_link"] = re.split(r'((?:<a href=")?https?://\S+[^\s,.:;])(?:><div)', row["job_link"])[1]
    return row['job_link']

def convert_url_for_csv(df):
    df["job_link"] = df.apply(process_url_for_csv, axis=1)
    return df



