import pandas as pd
import pdfplumber
import io
import numpy as np
from django.http import HttpResponse
from rest_framework import status
from engine.utils import storage_upload
from engine.models import Table


NANS_THRESHOLD = 0.75


def save_tables_from_page(page, page_number):
    dfs = extract_table_to_dfs(page)
    table_number = 0
    tables = []
    for df in dfs:
        table_url = save_df_as_csv_to_storage(df, 'page_{}_table_{}.csv'.format(page_number, table_number))
        if table_url['error'] is not None:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        table_model = Table(url=table_url['url'], num=table_number)
        tables.append(table_model)
        table_number += 1
    return tables


def extract_table_to_dfs(page):
    pdf_page = pdfplumber.load(page)
    tables = pdf_page.pages[0].extract_tables()
    dfs = []
    for table in tables:
        df = pd.DataFrame(table[1:], columns=table[0])
        number_of_not_nans = np.sum(df.count())
        if number_of_not_nans > 0:
            number_of_nans = df.isnull().sum().sum()
            percentage_of_nans = number_of_nans / (number_of_not_nans + number_of_nans)
            if percentage_of_nans <= NANS_THRESHOLD:
                dfs.append(df)
    return dfs


# likely to change if not using urls but keys!
# also data can be lost when converting to csv, fix?
def save_df_as_csv_to_storage(df, name):
    towrite = io.BytesIO()
    df.to_excel(towrite)
    towrite.seek(0)
    return storage_upload.fileobj2url(towrite, name)
