import pandas as pd
import os

path = 'Data/SalesAnalysis/Sales_Data'

monthly_sales_data = {

    'January': [],
    'February': [],
    'March': [],
    'April': [],
    'May': [],
    'June': [],
    'July': [],
    'August': [],
    'September': [],
    'October': [],
    'November': [],
    'December': []

}

for root, dirs, files in os.walk(path):
    for file in files:
        for month in monthly_sales_data:
            if month in file:
                monthly_sales_data[month] = pd.read_csv(os.path.join(root,file))
                print(monthly_sales_data[month])