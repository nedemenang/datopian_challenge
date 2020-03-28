import requests
from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime, timedelta


def get_beginning_date(date):
    date_string = date.split('to')[0].strip().replace('-', ' ').split(' ')
    string = " ".join(date_string)
    return datetime.strptime(string, '%Y %b %d').date()


DAILY_URL = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'
MONTHLY_URL = 'https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm'

# ============================================== daily hub data ============================================= #
henry_hub_daily = requests.get(DAILY_URL)
dialy_html = BeautifulSoup(henry_hub_daily.text, 'html.parser')

daily_table = dialy_html.find('table', summary='Henry Hub Natural Gas Spot Price (Dollars per Million Btu)')
daily_trs = daily_table.find_all('tr')
del daily_trs[0]
daily_data = {}
for tr in daily_trs:
    date_range = tr.find('td', class_='B6').text.strip() if tr.find('td', class_='B6') else None
    prices = tr.find_all('td', class_='B3')
    daily_data[date_range] = prices

with open('daily_gas_prices.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['Date', 'Price']
    csv_writer.writerow(headers)

    for k, v in daily_data.items():
        week_day = 0
        if k:
            beginning_date = get_beginning_date(k)
            for td in v:
                date = beginning_date + timedelta(days=week_day)
                price = td.text.strip()
                csv_writer.writerow([date, price])
                week_day += 1


# ====================================Monthly Hub data=========================================== #
henry_hub_monthly = requests.get(MONTHLY_URL)
monthly_html = BeautifulSoup(henry_hub_monthly.text, 'html.parser')

monthly_table = monthly_html.find_all('table')
monthly_trs = monthly_table[4].find_all('tr')
del monthly_trs[0]
monthly_data = {}
for tr in monthly_trs:
    year = tr.find('td', class_='B4').text.strip() if tr.find('td', class_='B4') else None
    prices = tr.find_all('td', class_='B3')
    monthly_data[year] = prices

# print(monthly_data)
with open('monthly_gas_prices.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['Date', 'Price']
    csv_writer.writerow(headers)
    for k, v in monthly_data.items():
        month = 1
        if k:
            for td in v:
                date = datetime.strptime(k + " " + str(month) + " 1", '%Y %m %d').date()
                price = td.text.strip()
                csv_writer.writerow([date, price])
                month += 1
