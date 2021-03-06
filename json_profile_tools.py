import json
from collections import Counter
import csv
import os.path
import os
from pathlib import PurePath
import pandas as pd

def main_processing(infile, outbase, unique = False, numeric = False, html = False, excel = False):
    """Main function to start the analysis program, returns a PurePath object of the results folder.

    Pass a filepath, and a path stem, plus optional flags about if you want certain calculations.
    This will create a new folder with natural numbers added to prevent overwriting.

    Keyword arguments:
    unique --  calculates if all the values seen in this field are unique
    numeric --  calculates the percent of the values seen in this field pass .isnumeric()
    html -- flag to create the html output
    excel -- flag to create the excel file output
    """
    rs = unpack_records(infile, unique, numeric)

    outfolder = PurePath(outbase)

    # chunk where the uniquness of the potential folder name is checked,
    # and a natural number added to the folder name until a unique name is found
    # will look nice until after 999 and increase the zfill if you need more.
    i = 0
    while True:
        if not os.path.isdir(outfolder):
            os.mkdir(PurePath(outfolder))
            break
        else:
            outfolder = PurePath(outbase + str(i).zfill(3))
            i += 1
    # write out summary files


    write_result_json(rs, PurePath(outfolder, PurePath(outfolder).stem + '.json'))
    write_result_csv(rs, PurePath(outfolder, PurePath(outfolder).stem + '.csv'))

    if html:
        write_html_profile(rs, PurePath(outfolder, PurePath(outfolder).stem + '.html'))

    if excel:
        write_excel_values(rs, PurePath(outfolder, PurePath(outfolder).stem + '.xlsx'))

    return PurePath(outfolder)


# functions to drive the initial analylsis
def unpack_records(infile, unique, numeric):
    """Pass in a file path, then unique and numeric flags, returns a dict of a analyzed records.

    Parses the json file, sends each record throuh process_record,
    Sends the collective records to integrate_summaries"""
    alldata = []
    with open(infile, 'r', encoding='utf-8') as jsonin:
        data = json.load(jsonin)

    if isinstance(data, dict): # attempt to force this into a records like structure
        data = [data]

    for r in data:
        alldata.append(process_record(r))

    return integrate_summaries(alldata, unique, numeric)

def process_record(record):
    """Recieves a list of records in json and profiles them, returns the dict profile of data.

    Presumes a similar schema across all records.
    Will recursively traverse the object tree, flattening out the structure during profiling.
    Returns a dictionary of a complete profile."""


    def traverse_record(record, profile):
            """Processes a single record, to be used recursively, returning the updated profile object.

            Pass a single data record and the current profile object.
            Calculates profile information about each field and adds it to the profile.
            Will recursively call itself if another dict is found as as value."""

            for key, value in record.items():
                added_already = False # sentinel to prevent dupes
                if key not in profile: # adds base case for unseen fields
                    profile[key] = {'count': 1, 'values': []}
                    added_already = True

                    if isinstance(value, dict) or isinstance(value, list): # adds this if the field is seen as a container
                        profile[key]['values'].append('USEDASCONTAINER')

                if not isinstance(value, dict) and not isinstance(value, list): # add seen value of field if value not a dict
                    profile[key]['values'].append(value)
                elif isinstance(value, list):
                    for r in value:
                        profile = traverse_record(r, profile)
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
    """Processes a list of profile summaries and returns a synthesized dictionary of values.

    pass this a list of dicts with the summaries, and calculation flags, and it'll integrate them into
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

    count_values(full)

    if unique:
        determine_uniques(full)

    # add numeric checks
    if numeric:
        percent_numeric(full)

    return full


# functions to calculate information about the profile
def percent_numeric(full):
    """Calculates the percent of values within each field that are numeric, updates the profile data.

    Pass a dict of the full profile data.
    Mutates the profile dict to have the percent_is_numeric value.
    This runs .isnumeric() on string versions of all values, and calculates the percentage that are True"""
    for key, value in full.items():
        numericsQ = [str(str(v).isnumeric()) for v in value['values'].keys()].count('True') / len(value['values'].values())
        full[key]['percent_is_numeric'] = numericsQ

def determine_uniques(full):
    """Calculates the percent of unique values within the fields, updates the profile data.

    Pass a dict of the full profile data.
    Mutates the profile dict to have the all_unique_Q value.
    This calculates if all values seens for a field appear one and only one time, and thus it is a
    unique field."""
    for key, value in full.items():
        counts = set(value['values'].keys())
        if len(counts) == 1:
            full[key]['all_unique_Q'] = True
        else:
            full[key]['all_unique_Q'] = False

def count_values(full):
    """Counts the number of unique values seen within that field, updates the profile data.

    Pass it a dict of the full profile data. Counts the number of times each unique value seen for that field appears.

    """
    for key, value in full.items():
        full[key]['values'] = Counter(full[key]['values'])


# functions to write values out
def write_result_json(alldata, filename):
    """Writes dictionary values out as json file.

    Pass a dictionary of an analyzed file and a file name, will
    Writes that dictionary out as a json file with indent of 4 spaces."""
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(alldata, outfile, indent = 4)

def write_result_csv(alldata, filename):
    """Formats and writes dict results as a CSV file.

    Pass dictionary of an analyzed file and a file name.
    Selects some data from that dict and writes it out as a CSV file."""
    rows = []
    headers = ['field','num_times_seen' ]

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

    with open(filename, 'w', encoding='utf-8') as csvout:
        out = csv.writer(csvout)
        out.writerow(headers)
        out.writerows(rows)

def write_html_profile(full, filename):
    """Writes out the HTML version of the data profile.

    pass a dict of the full profile data and file name,
    loads as a pandas data frame, and writes it to and HTML file"""
    df = pd.read_json(json.dumps(full))
    df = df.T
    html = df.to_html()
    with open(filename, 'w', encoding = 'utf-8') as out:
        out.write(html)

def write_excel_values(full, filename):
    """Writes out the Excel formatted version of the data profile.

    pass a dict of the full profile data and file name,
    loads it as a data frame, loops over the values seen in the fields,
    writes out the values and their counts as separate excel sheets."""
    df = pd.read_json(json.dumps(full))
    writer = pd.ExcelWriter(filename)

    for name in df.columns:
        minidf = pd.DataFrame([[k, v] for k,v in df[name]['values'].items()], columns = ['value', 'count'])
        minidf.to_excel(writer, str(name), index = False, encoding = 'utf-8')

    writer.save()
