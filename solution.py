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
    """ Converts Timestamp and adds 3 hours (Pacfic to Eastern)
    caps fullname,
    zeros added to < 5 zipcode lengths
    converts duration time to seconds"""
    for row in csv_list:
        dt = datetime.strptime(row['Timestamp'], '%m/%d/%y %I:%M:%S %p') + timedelta(hours=3)
        row['Timestamp'] = dt.isoformat('T')
        row['FullName'] = row['FullName'].upper()
        row['ZIP'] = (row['ZIP'].rjust(5, '0'))
        row['BarDuration'] = format_time_to_seconds(row['BarDuration'])
        row['FooDuration'] = format_time_to_seconds(row['FooDuration'])
        row['TotalDuration'] = int(row['BarDuration']) + int(row['FooDuration'])
    return csv_list

        
def format_time_to_seconds(value):
    time = value.replace('.',":").split(':')
    return str((int(time[0]) * 60 * 60) + (int(time[1]) * 60) + int(time[2]))


try:
    lists_from_csv, headers = open_file(sys.argv[1])
    data = data_manipulation(lists_from_csv)
    write_file(sys.argv[2], data, headers)
except(IndexError):
    sys.exit("Please input a csv file in the format: $python3 solution.py sample.csv output.csv ")
