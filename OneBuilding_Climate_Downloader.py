import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os

url = 'https://climate.onebuilding.org/'

print('1. Africa')
print('2. Asia')
print('3. South America')
print('4. North-Central America')
print('5. Southwest Pacific')
print('6. Europe')
print('7. Antarctica')
print()

while True:
    try:
        zone = int(input('Enter the number of your choice (1 to 7): '))
        if zone == 1:
            url = url + 'WMO_Region_1_Africa/'
            break
        elif zone == 2:
            url = url + 'WMO_Region_2_Asia/'
            break
        elif zone == 3:
            url = url + 'WMO_Region_3_South_America/'
            break
        elif zone == 4:
            url = url + 'WMO_Region_4_North_and_Central_America/'
            break
        elif zone == 5:
            url = url + 'WMO_Region_5_Southwest_Pacific/'
            break
        elif zone == 6:
            url = url + 'WMO_Region_6_Europe/'
            break
        elif zone == 7:
            url = url + 'WMO_Region_7_Antarctica/'
            break
        else:
            print()
            print('Number must be an integer from 1 to 7')
            print()
    except ValueError:
        print("Invalid input. Please restart the script and enter a valid number.")
print()

try:
    country = input('Enter the country of your choice, following the format of Climate.OneBuilding.Org (ex: FRA_France): ')
    url = url + country
except ValueError:
    print("Invalid input. Please restart the script.")
print()

reqs = requests.get(url)
not_found = reqs.text.find('404 Not Found')
if not_found != -1:
    print('404 Not Found, please restart the script with different values.')
    exit()
soup = BeautifulSoup(reqs.text, 'html.parser')

print('1. Climate data from 2004 to 2018')
print('2. Climate data from 2007 to 2021')
print('3. All data available')
print()

while True:
    try:
        zone = int(input('Enter the number of your choice (1 to 3): '))
        if zone == 1:
            data_time = '18.zip'
            break
        elif zone == 2:
            data_time = '21.zip'
            break
        elif zone == 3:
            data_time = 'Yx.zip'
            break
        else:
            print()
            print('Number must be an integer from 1 to 3')
            print()
    except ValueError:
        print("Invalid input. Please restart the script and enter a valid number.")
print()

print('1. EPW')
print('2. CLM')
print('3. WEA')
print('4. PVSyst')
print('5. DDY')
print('6. RAIN')
print('7. STAT')
print()

while True:
    try:
        zone = int(input('Enter the number of your choice (1 to 7): '))
        if zone == 1:
            climate_file = '.epw'
            break
        elif zone == 2:
            climate_file = '.clm'
            break
        elif zone == 3:
            climate_file = '.wea'
            break
        elif zone == 4:
            climate_file = '.pvsyst'
            break
        elif zone == 5:
            climate_file = '.ddy'
            break
        elif zone == 6:
            climate_file = '.rain'
            break
        elif zone == 7:
            climate_file = '.stat'
            break
        else:
            print()
            print('Number must be an integer from 1 to 7')
            print()
    except ValueError:
        print("Invalid input. Please restart the script and enter a valid number.")
print()

save_path = input('Enter the complete path to the folder where climate files will be saved: ')
print()
if not os.path.isdir(save_path):
    print('Invalid folder path, please restart the script with different value.')
    exit()

urls = []
for link in soup.find_all('a'):
    file_link = str(link.get('href'))
    if file_link.endswith(data_time):
        link = url + '/' + file_link
        urls.append(link)

urlnumber = len(urls)
counter = 0

for x in urls:
    r = requests.get(x)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    zip_content = z.namelist()
    for f in zip_content:
        if f.endswith(climate_file):
            z.extract(f, path=save_path)
    counter = counter + 1
    print (counter, '/', urlnumber)

print("Done !")