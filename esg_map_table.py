import pandas as pd
from tabulate import tabulate
import csv

# Read the CSV file with proper quoting
csv_path = '/Users/asfalanoi/economics_lits/esg_map.csv'
df = pd.read_csv(csv_path, quoting=csv.QUOTE_ALL)

# Print the table nicely
print(tabulate(df, headers='keys', tablefmt='psql', showindex=False)) 