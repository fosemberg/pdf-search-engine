import pandas as pd
import pdfplumber
from utils import storage_upload


def extract_table_to_dfs(page, threshold):
    """
    :param page: pdf page in bytes
    :param threshold: max percentage of nans
    :return: list of pandas DataFrames
    """
    with pdfplumber.load(page) as pdf_page:
        tables = pdf_page.pages[0].extract_tables()
        dfs = []
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            n, m = df.shape
            number_of_nans = df.isnull().sum().sum()
            if number_of_nans / (n * m) <= threshold:
                dfs.append(df)
        return dfs


# likely to change if not using urls but keys!
# also data can be lost when converting to csv, fix?
def save_df_as_csv_to_storage(df, name):
    csv = df.to_csv()
    key = '{}_key'.format(name)
    return storage_upload. fileobj2url(csv, key)
