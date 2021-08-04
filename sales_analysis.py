import pandas as pd
import matplotlib.pyplot as plt
import os

path = '../Sales_Data_Analysis/Data/SalesAnalysis/Sales_Data'
path_absolute = 'C:/Users/Daniel/Desktop/Sales_Data_Analysis/Data/SalesAnalysis/Sales_Data'

#Dictionary assigning each month to a Pandas DataFrame
monthly_sales_data = {

    'January': pd.DataFrame() ,
    'February': pd.DataFrame(),
    'March': pd.DataFrame(),
    'April': pd.DataFrame(),
    'May': pd.DataFrame(),
    'June': pd.DataFrame(),
    'July': pd.DataFrame(),
    'August': pd.DataFrame(),
    'September': pd.DataFrame(),
    'October': pd.DataFrame(),
    'November': pd.DataFrame(),
    'December': pd.DataFrame()

}

#files variable is a list of all the file names within the data directory
files = []
#final is a dataframe to be created holding all the csv data of all files
final = pd.DataFrame()

#Read each csv into a single Pandas DataFrame holding all the data
for file in os.listdir(path):

    files.append(file)
    for month in monthly_sales_data:

        if month in file:

            temp = monthly_sales_data[month] = pd.read_csv(path + '/' + file)
            final = pd.concat([final, temp])

            print(file)
            print(monthly_sales_data[month])
            print('---------------------------------------------------------------')

final.to_csv(path + '/Sales_All_Months.csv', index=False)

print('Sales_All_Months.csv')
print(final)

print('---------------------------------------------------------------')
print('---------------------------------------------------------------')

#Dictionary to hold a data link between months an profit of each month
monthly_sales_profit = {

    'January': 0,
    'February': 0,
    'March': 0,
    'April': 0,
    'May': 0,
    'June': 0,
    'July': 0,
    'August': 0,
    'September': 0,
    'October': 0,
    'November': 0,
    'December': 0

}

#Loop through the DataFrames to clean the data
for e in monthly_sales_data:

    #Cleaning up each month by removing NaN values and duplicate column names in some rows
    df = monthly_sales_data[e].dropna(how='all')
    df = df[df['Quantity Ordered'] != 'Quantity Ordered']

    #Converting string values to int and float values for performing calculations
    df['Quantity Ordered'].astype(int)
    df['Price Each'].astype(float)

    #Iterate all rows to find the profit of each month by use of an accumulator
    accumulator = 0
    for index, row in df.iterrows():

        accumulator += int(row['Quantity Ordered']) * float(row['Price Each'])

    #Print each months profit
    monthly_sales_profit[e] = accumulator
    print('Month of ' + e + ' had profit of ' + str(int(monthly_sales_profit[e])) + ' $')

#Print month with the most profit
print('---------------------------------------------------------------')

#Store the values inside variables
highest_profit = max(monthly_sales_profit, key=monthly_sales_profit.get)
highest_profit_value = str(int(monthly_sales_profit[highest_profit]))
print('Month with the most profit was ' + highest_profit + ' with profit of ' + highest_profit_value + ' $.')


#Add a column which has the profit of each transaction
#After adding said column calculate the monthly profit by use of the sum method, placing all profits inside a list
profits = []
for e in monthly_sales_data:

    # Cleaning up each month by removing NaN values and duplicate column names in some rows
    monthly_sales_data[e] = monthly_sales_data[e].dropna(how='all')
    monthly_sales_data[e] = monthly_sales_data[e][monthly_sales_data[e]['Quantity Ordered'] != 'Quantity Ordered']

    # Converting string values to int and float values for performing calculations
    monthly_sales_data[e]['Quantity Ordered'].astype(int)
    monthly_sales_data[e]['Price Each'].astype(float)

    #Adding a Transaction Profit column for each transaction by performing series multiplication
    monthly_sales_data[e]['Transaction Profit of Sale:'] = monthly_sales_data[e]['Quantity Ordered'].astype(int) * monthly_sales_data[e]['Price Each'].astype(float)

    #Append to a list of profits the profits of each month by summing the profit of each transaction which occured in said month
    profits.append(int(monthly_sales_data[e]['Transaction Profit of Sale:'].sum()))


#Plot the results in our monthly profits dictionary
#Pass in monthly_sales_profit as the variable for this
def plot_pie_chart(monthly_sales_profit):

    #Firstly, define data
    keys = monthly_sales_profit.keys()
    values = monthly_sales_profit.values()

    #Secondly, draw a PieChart:
    plt.pie(values, None, keys, None, autopct='%1.1f%%')
    plt.savefig('PieChart.png')
    plt.show()

#Pass in monthly_sales_profit as the variable for this
def plot_bar_chart(monthly_sales_profit):

    # Firstly, define data
    keys = monthly_sales_profit.keys()
    values = monthly_sales_profit.values()

    #Secondly, draw a BarChart:
    plt.bar(keys, values)
    plt.xlabel('Month Number')
    plt.xticks(fontsize=7)
    plt.ylabel('Sales in USD ($)')
    plt.savefig('BarChart.png')
    plt.show()

def city_most_profit_generated_in_month(monthly_sales_data):

    #Create a new column in our Sales dataframe containg the city of each sale
    city_profit = []
    city_with_most_profit = []
    for e in monthly_sales_data:

        #Cleaning up each month by removing NaN values and duplicate column names in some rows
        monthly_sales_data[e] = monthly_sales_data[e].dropna(how='all')
        monthly_sales_data[e] = monthly_sales_data[e][monthly_sales_data[e]['Quantity Ordered'] != 'Quantity Ordered']

        #Adding a address column for each transaction by using string manipulation
        monthly_sales_data[e]['City'] = monthly_sales_data[e]['Purchase Address'].str.split(',').str[1]

        df = pd.DataFrame(monthly_sales_data[e].groupby(['City']).sum())
        #city_profit.append(df)

        df = pd.DataFrame(df.loc[df['Transaction Profit of Sale:'] == float(df.max())])

        city_profit.append(df.iloc[0])
        city_with_most_profit.append(float(df.max()))
        #city_profit.append(monthly_sales_data[e].groupby(['City']).sum())
        #city_with_most_profit.append(float(monthly_sales_data[e].groupby(['City']).sum().max()))


    print(city_profit)
    print('---------------------------------------------------------------')
    print(city_with_most_profit)

#city_most_profit_generated_in_month(monthly_sales_data)

#Use date_time to parse the date and time of each purchase to then process the data
for e in monthly_sales_data:
    monthly_sales_data[e]['Order Date'] = pd.to_datetime(monthly_sales_data[e]['Order Date'])
    monthly_sales_data[e]['Order Hour'] = monthly_sales_data[e]['Order Date'].dt.hour
    monthly_sales_data[e]['Order Minute'] = monthly_sales_data[e]['Order Date'].dt.minute

#Plot our data to realize what correlation may exist between buying time and possible optimisations
for e in monthly_sales_data:

    #For each month in the monthly data dictionary place ammount of sales which occured in that hour inside that hour using group_by()
    #Count each sale by the hour its in and define how many purchases occurs in each hour
    hours = [hour for hour, df in monthly_sales_data[e].groupby('Order Hour')]
    plt.plot(hours, monthly_sales_data[e].groupby(['Order Hour']).count())
    plt.xticks(hours)
    plt.grid()
    plt.ylim([0, 1500])
    '../Sales_Data_Analysis/Grid Plots/GridPlot'
    plt.savefig('../Sales_Data_Analysis/Grid Plots/GridPlot' + str(e) + '.png')
    plt.show()

'''
After looking at all months we realize the peak for sales is between 10 to 12, so a good time to place
an ad may be between 9 to 11.
'''

