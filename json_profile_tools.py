import json
from collections import Counter
import csv
import os.path
import os
from pathlib import PurePath

def main_processing(infile, outbase, unique = False, numeric = False):
    """Main function to start the analysis program. Pass it a filepath, and a path stem,
    plus flags about if you want certain calculations.
    This will create a new folder with natural numbers added to prevent overwriting.
    unique = calculates if all the values seen in this field are unique
    numeric = calculates the percent of the values seen in this field pass .isnumeric()"""

    rs = unpack_records(infile, unique, numeric)
    outfolder = PurePath(outbase)

    # chunk where the uniquness of the potential folder name is checked,
    # and a natural number added to the folder name until a unique name is found
    # will look nice until after 999 and increase the zfill if you need more.
    i = 0
    while True:
        if not os.path.isdir(outfolder):
            os.mkdir(outfolder)
            break
        else:
            outfolder = PurePath(outbase + str(i).zfill(3))
            i += 1
    # write out summary files
    write_result_json(rs, PurePath(outfolder, outbase + '.json'))
    write_result_csv(rs, PurePath(outfolder, outbase + '.csv'))

    return PurePath(outfolder)

def unpack_records(infile, unique, numeric):
    """Pass in a file path, then unique and numeric flags.
    Returns a dictionary of the fully analyzed records from this file.
    Parses the json file, sends each record throuh process_record,
    Sends the collective records to integrate_summaries"""
    alldata = []
    with open(infile, 'r') as jsonin:
        data = json.load(jsonin)

    for r in data:
        alldata.append(process_record(r))

    return integrate_summaries(alldata, unique, numeric)

def write_result_json(alldata, filename):
    """Pass a dictionary of an analyzed file and a file name.
    Writes that dictionary out as a json file with indent of 4 spaces."""
    with open(filename, 'w') as outfile:
        json.dump(alldata, outfile, indent = 4)

def write_result_csv(alldata, filename):
    """Pass dictionary of an analyzed file and a file name.
    Selects some data from that dict and writes it out as a CSV file."""
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
    """Recieves a list of records in json and profiles them. Presumes a similar schema.
    Will recursively traverse the object tree, flattening out the structure during profiling.
    Returns a dictionary of a complete profile."""


    def traverse_record(record, profile):
            """Pass a single data record and the base profile object.
            Calculates profile information about each field and adds it to the profile.
            Will recursively call itself if another dict is found as as value."""

            for key, value in record.items():
                added_already = False # sentinel to prevent dupes
                if key not in profile: # adds base case for unseen fields
                    profile[key] = {'count': 1, 'values': []}

                    added_already = True

                    if isinstance(value, dict): # adds this if the field is seen as a container
                        profile[key]['values'].append('USEDASCONTAINER')

                if not isinstance(value, dict): # add seen value of field if value not a dict
                    if not added_already:
                        profile[key]['count'] += 1
                    profile[key]['values'].append(value)
                else:
                    # recursively do this for each level of the tree
                    profile = traverse_record(value, profile)
            return profile

    # establishing base cases
    profile = {key: {'count': 1, 'values': []} for key in record.keys()}
    for key, value in record.items():
        if isinstance(value, dict):
            profile[key]['values'].append('USEDASCONTAINER')
    return traverse_record(record, profile)


def integrate_summaries(summaries, unique, numeric):
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

    if unique:
        determine_uniques(full)

    # add numeric checks
    if numeric:
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


