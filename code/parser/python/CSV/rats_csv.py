#/usr/bin/python
"""
    @author Giang Nguyen <ghnguyen@wpi.edu>
    @author Francisco Guerrero <afguerrerohernan@wpi.edu>
    @date 10/11/2016
"""
import os
import re
import csv
import json
import argparse
import subprocess
from bs4 import BeautifulSoup


def process_rats(filename):
    """
    Function to process the provided file with RATS

    :param filename: the file to process
    :return: the number of vulnerabilities, the severity of the vulnerability and the type of vulnerability
    """
    proc = subprocess.Popen(['rats', '--xml', '--noheader', filename], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    xml_parser = BeautifulSoup(out, features='xml')

    if xml_parser.vulnerability:
        vulnerabilities = xml_parser.findAll('vulnerability')
        high = None
        typ = None
        desc = None
        line = 0

        for vulnerability in vulnerabilities:
            if vulnerability.severity.text:
                high = vulnerability.severity.text
            if vulnerability.type:
                typ = vulnerability.type.text
            if vulnerability.message:
                desc = vulnerability.message.text
            if vulnerability.file.line.text:
                line = vulnerability.file.line.text
            

        return len(vulnerabilities), typ, high, line, desc

    else:
        return 0, None, None, 0, None


def process_json_file():
    """
    Process the JSON file with the list of vulnerabilites
    """
    json_file = os.path.expanduser(args.path)
    with open(json_file) as data_file:
        data = json.load(data_file)

        with open(args.output, 'wb') as csvfile:
            fieldnames = ['answer_id', 'snippet_no', 'parent_id', 'score', 'owner_id', 'rats_count', 'rats_type',
                          'rats_severity', 'rats_line', 'rats_desc']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ix in range(len(data)):
                filename = str(data[ix]["AnswerId"]) + "_" + str(data[ix]['SnippetNumber']) + "_" + str(
                    data[ix]["ParentId"]) + "_" + str(data[ix]["Score"]) + "_" + str(data[ix]["OwnerUserId"]) + ".c"

                # Write the code to a temporary file
                with open(filename, 'a') as the_file:
                    the_file.write(data[ix]["Code"].encode("utf-8"))
                (rats_count, rats_type, rats_severity, rats_line, rats_desc) = process_rats(filename)
                os.remove(filename)

                writer.writerow({'answer_id': str(data[ix]["AnswerId"]),
                                 'snippet_no': str(data[ix]['SnippetNumber']),
                                 'parent_id': str(data[ix]["ParentId"]),
                                 'score': str(data[ix]["Score"]),
                                 'owner_id': str(data[ix]["OwnerUserId"]),
                                 'rats_count': rats_count,
                                 'rats_type': rats_type,
                                 'rats_severity': rats_severity,
                                 'rats_line': rats_line,
                                 'rats_desc': rats_desc
                                 })


parser = argparse.ArgumentParser(description='Process Stack Overflow Answers JSON.')
parser.add_argument('-i', dest='path', metavar='path', help='path of the json file', required=True)
parser.add_argument('-o', dest='output', metavar='output', help='The name of the output file', required=True)
args = parser.parse_args()
process_json_file()