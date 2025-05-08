import pandas as pd
from tabulate import tabulate
import csv
import sys

csv_path = '/Users/asfalanoi/economics_lits/esg_map.csv'

def display_table():
    df = pd.read_csv(csv_path, quoting=csv.QUOTE_ALL)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

def export_to_csv():
    df = pd.read_csv(csv_path, quoting=csv.QUOTE_ALL)
    export_path = 'esg_map_export.csv'
    df.to_csv(export_path, index=False)
    print(f"Table exported to {export_path}")

def main():
    while True:
        print("\n==== ESG Map Table App ====")
        print("1. Display ESG Map Table")
        print("2. Export Table to CSV")
        print("3. Exit")
        choice = input("Select an option (1-3): ")
        if choice == '1':
            display_table()
        elif choice == '2':
            export_to_csv()
        elif choice == '3':
            print("Exiting app.")
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main() 