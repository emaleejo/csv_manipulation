import csv
import sys
from datetime import datetime, timedelta
import os

def open_file(file):
    with open(file, 'r', encoding='utf8', errors='replace') as file:
        lists_from_csv = []
        reader = csv.DictReader(file, dialect='excel', delimiter=',')
        headers = next(reader)
        for row in reader:
            lists_from_csv.append(row)
        file.close()
    return lists_from_csv, headers


def write_file(file_name, lists_from_csv, headers):
    with open(file_name, 'w', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in lists_from_csv:
            writer.writerow(row)
    os.system(f"open {sys.argv[2]}")
    file.close()
    

def data_manipulation(csv_list):
    for row in csv_list:
        dt = datetime.strptime(row['Timestamp'], '%m/%d/%y %I:%M:%S %p') + timedelta(hours=4)
        row['Timestamp'] = dt.isoformat('T')
        row['FullName'] = row['FullName'].upper()
        row['ZIP'] = zero_zip(row['ZIP'])
        row['BarDuration'] = format_time(row['BarDuration'])
        row['FooDuration'] = format_time(row['FooDuration'])
    return csv_list


def zero_zip(zipcode):
    num = 5 - len(zipcode)
    if num == 1:
        zipcode = '0' + str(zipcode)
    elif num == 2:
        zipcode = '00' + str(zipcode)
    elif num == 3:
        zipcode = '000' + str(zipcode)
    elif num == 4:
        zipcode = '0000' + str(zipcode)
    return zipcode

        
def format_time(value):
    a = value.replace('.',":").split(':')
    return str((int(a[0]) * 60 * 60) + (int(a[1]) * 60) + int(a[2]))


def cal_total(csv_list):
    for row in csv_list:
        row['TotalDuration'] = str(int(row['FooDuration']) + int(row['BarDuration']))
    return csv_list


try:
    lists_from_csv, headers = open_file(sys.argv[1])
    time = data_manipulation(lists_from_csv)
    write_file(sys.argv[2], time, headers)
except(IndexError):
    sys.exit("Please input a csv file in the format: $python3 solution.py sample.csv output.csv ")
