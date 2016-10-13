#/usr/bin/python
"""
    @author Giang Nguyen <ghnguyen@wpi.edu>
    @author Francisco Guerrero <afguerrerohernan@wpi.edu>
    @date 10/07/2016
"""
import os
import re
import csv
import json
import argparse
import subprocess
from bs4 import BeautifulSoup


def process_flawfinder(filename):
    """
    Function to process the provided file with FlawFinder

    :param filename: the file to process
    :return: the number of vulnerabilities, the severity of the vulnerability and the type of vulnerability
    """
    proc = subprocess.Popen(
        ['flawfinder', '--columns', '--omittime', '--dataonly', '--quiet', '--singleline', filename],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = proc.communicate()

    if out is not None and out:
        high = 0
        row = 0
        count = 0
        desc = None

        for line in out.split('\n'):
            if line:
                match = re.search('\.*?:(.*?):\d+:  \[(\d)\] \((\w+)\) (\w+): (.*)', line, re.M | re.I)

                if match:
                    count += 1
                    #sn = int(match.group(1))
                    row = match.group(1)
                    high = match.group(2)
                    typ = match.group(3) + ' ' + match.group(4)
                    desc = match.group(5)
                    
                else:
                    print "nomatch: ", line

        if count > 0:
            return count, row, typ, high, desc

    return 0, 0, None, 0, None


def process_json_file():
    """
    Process the JSON file with the list of vulnerabilites
    """
    json_file = os.path.expanduser(args.path)
    with open(json_file) as data_file:
        data = json.load(data_file)

        with open(args.output, 'wb') as csvfile:
            fieldnames = ['answer_id', 'snippet_no', 'parent_id', 'score', 'owner_id', 'ff_count', 'ff_line', 'ff_type', 'ff_severity', 'ff_description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ix in range(len(data)):
                filename = str(data[ix]["AnswerId"]) + "_" + str(data[ix]['SnippetNumber']) + "_" + str(
                    data[ix]["ParentId"]) + "_" + str(data[ix]["Score"]) + "_" + str(data[ix]["OwnerUserId"]) + ".c"

                # Write the code to a temporary file
                with open(filename, 'a') as the_file:
                    the_file.write(data[ix]["Code"].encode("utf-8"))
                (ff_count, ff_line, ff_type, ff_severity, ff_description) = process_flawfinder(filename)
                os.remove(filename)

                writer.writerow({'answer_id': str(data[ix]["AnswerId"]),
                                 'snippet_no': str(data[ix]['SnippetNumber']),
                                 'parent_id': str(data[ix]["ParentId"]),
                                 'score': str(data[ix]["Score"]),
                                 'owner_id': str(data[ix]["OwnerUserId"]),
                                 'ff_count': ff_count,
                                 'ff_line': ff_line,
                                 'ff_type': ff_type,
                                 'ff_severity': ff_severity,
                                 'ff_description': ff_description})


parser = argparse.ArgumentParser(description='Process Stack Overflow Answers JSON.')
parser.add_argument('-i', dest='path', metavar='path', help='path of the json file', required=True)
parser.add_argument('-o', dest='output', metavar='output', help='The name of the output file', required=True)
args = parser.parse_args()
process_json_file()