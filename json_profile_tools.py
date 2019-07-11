import json
from collections import Counter
import csv
import os.path
import os
import pathlib

def main_processing(infile, outbase):
    rs = unpack_records(infile)
    outfolder = outbase + '/'
    i = 0
    while True:
        if not os.path.isdir(outfolder):
            os.mkdir(outfolder)
            break
        else:
            outfolder = outbase + str(i).zfill(3) + '/'
            i += 1
    write_result_json(rs, outfolder + outbase + '.json')
    write_result_csv(rs, outfolder + outbase + '.csv')

def unpack_records(infile):
    alldata = []
    with open(infile, 'r') as jsonin:
        data = json.load(jsonin)

    for r in data:
        alldata.append(process_record(r))

    return integrate_summaries(alldata)

def write_result_json(alldata, filename):
    with open(filename, 'w') as outfile:
        json.dump(alldata, outfile, indent = 4)

def write_result_csv(alldata, filename):

    rows = []
    headers = ['field','num_unique_values' ]

    for key, value in alldata.items():
        row = []
        row.append(key) # add the field
        row.append(len(set(value['values'].keys()))) # add the number of unique values

        if 'all_unique_Q' in value: # add uniqueQ if present
            row.append(value['all_unique_Q'])
            if not 'all_unique_Q' in headers:
                headers.append('all_unique_Q')

        if 'percent_is_numeric' in value: # add the percent numeric if present
            row.append(value['percent_is_numeric'])
            if not 'percent_is_numeric' in headers:
                headers.append('percent_is_numeric')
        rows.append(row)

    with open(filename, 'w') as csvout:
        out = csv.writer(csvout)
        out.writerow(headers)
        out.writerows(rows)



def process_record(record):
    """Recieves a list of records in json and profiles them. Presumes a similar schema."""
    def traverse_record(record, profile):
            """recieves one record as dict and profiles it"""
            for key, value in record.items():
                added_already = False
                if key not in profile:
                    profile[key] = {'count': 1, 'values': []}
                    added_already = True
                    if isinstance(value, dict):
                        profile[key]['values'].append('USEDASCONTAINER')
                if not isinstance(value, dict):
                    if not added_already:
                        profile[key]['count'] += 1
                    profile[key]['values'].append(value)
                else:
                    # recursively do this for each level of the tree
                    profile = traverse_record(value, profile)
            # print(profile)
            return profile

    # establishing base cases
    profile = {key: {'count': 1, 'values': []} for key in record.keys()}
    for key, value in record.items():
        if isinstance(value, dict):
            profile[key]['values'].append('USEDASCONTAINER')
    return traverse_record(record, profile)


def integrate_summaries(summaries):
    """pass this a list of dicts with the summaries, and it'll integrate them into
    a single dictionary that aggregates all the values.
    Will currently only aggregate counts counted values."""
    full = {}
    for d in summaries:
        for key, value in d.items():
            if key not in full:
                full[key] = {'count': value['count'], 'values': value['values']}
            else:
                full[key]['count'] += value['count']
                full[key]['values'] += value['values'] # concat b/c needing to flatten it

    # summarize the values areas

    count_values(full)

    # add all unique value to the summary

    determine_uniques(full)

    # add numeric checks
    percent_numeric(full)

    return full


def percent_numeric(full):
    for key, value in full.items():
        numericsQ = [str(str(v).isnumeric()) for v in value['values'].keys()].count('True') / len(value['values'].values())
        print(numericsQ)
        full[key]['percent_is_numeric'] = numericsQ


def determine_uniques(full):
    for key, value in full.items():
        counts = set(value['values'].keys())
        if len(counts) == 1 and counts[0] == 1:
            full[key]['all_unique_Q'] = True
        else:
            full[key]['all_unique_Q'] = False


def count_values(full):
    for key, value in full.items():
        full[key]['values'] = Counter(full[key]['values'])


