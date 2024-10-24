import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description

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

def add_datarow():
    Csv.initialize_csv()
    date=get_date("Provide transaction date in dd-mm-yyyy format: ")
    amount=get_amount()
    category=get_category()
    description=get_description()
    Csv.add_entry(date,amount,category,description)

add_datarow()