import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description,DATE_FORMAT

class Csv:
    '''Csv data handler class'''
    CSV_FILE="finance_data.csv"
    FIELDNAMES=['date','amount','category','description']
    CURRENCY_SYMBOL='$'

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
            total_income=results_df[results_df['category']=='Income']['amount'].sum()
            total_expense=results_df[results_df['category']=='Expense']['amount'].sum()
            overall=total_income-total_expense

            print(f'\nTransactions for range: {start_date.strftime(DATE_FORMAT)} - {end_date.strftime(DATE_FORMAT)}')
            cls.present_transactions(results_df)
            print(f'Your ballance for a given timeframe is {overall:.2f} {cls.CURRENCY_SYMBOL}\n')
            print()
            

    @classmethod
    def present_transactions(cls,transactions: pd.DataFrame):
        print('='*30)
        print(
            transactions.sort_values(by=['date']).to_string(
                index=False,
                formatters={
                    'date': lambda x: x.strftime(DATE_FORMAT),
                    'amount': lambda x: f'{x:.2f} {cls.CURRENCY_SYMBOL}'
                    }
                )
            )
        print('='*30)

def add_transaction():
    date=get_date("Provide transaction date in dd-mm-yyyy format: ")
    amount=get_amount()
    category=get_category()
    description=get_description()
    Csv.add_entry(date,amount,category,description)

def check_transactions():
    start_date=get_date("Provide start date in dd-mm-yyyy format: ")
    end_date=get_date("Provide end date in dd-mm-yyyy format: ")
    Csv.get_transactions_by_date(start_date,end_date)


def main():
    Csv.initialize_csv()

    while True:
        print('\n1. Add new transaction')
        print('2. View summary for a given date range')
        print('3. Exit')
        choice = input('Enter your choice (1-3): ')

        if choice=='1':
            add_transaction()
        elif choice=='2':
            check_transactions()
        elif choice=='3':
            print('Exiting...')
            break
        else:
            print('Incorrect input, try again.')

main()
