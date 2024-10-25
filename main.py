import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description,DATE_FORMAT

class Csv:
    '''Csv data handler class'''
    CSV_FILE="finance_data.csv"
    FIELDNAMES=['date','amount','category','description']

    @classmethod
    def initialize_csv(cls) -> None:
        '''Initializing csv file'''
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.FIELDNAMES)
            df.to_csv(cls.CSV_FILE,index=False)

    @classmethod
    def add_entry(cls, date:str, amount:float, category:str, description:str):
        '''Add new finance tracker entry to scv file'''
        new_entry = {
            'date':date,
            'amount':amount,
            'category':category,
            'description':description
        }
        with open(cls.CSV_FILE,'a',newline='',encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=cls.FIELDNAMES)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions_by_date(cls,start_date:str,end_date:str):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'],format=DATE_FORMAT)
        start_date = datetime.strptime(start_date,DATE_FORMAT)
        end_date = datetime.strptime(end_date,DATE_FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)

        results_df = df.loc[mask]

        if results_df.empty:
            print('No transactions found for given date frame')
        else:
            print(f'Transactions for range: {start_date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}')
            print(
                results_df.to_string(
                    index=False,
                    formatters={'date': lambda x: x.strftime(DATE_FORMAT)}
                    )
                )

def add_datarow():
    Csv.initialize_csv()
    date=get_date("Provide transaction date in dd-mm-yyyy format: ")
    amount=get_amount()
    category=get_category()
    description=get_description()
    Csv.add_entry(date,amount,category,description)

Csv.get_transactions_by_date('12-10-2001','12-10-2001')