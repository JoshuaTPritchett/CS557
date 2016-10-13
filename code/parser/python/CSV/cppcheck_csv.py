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


def process_cppcheck(filename):
    """
    Function to process the provided file with cppcheck

    :param filename: the file to process
    :return: the number of vulnerabilities, the severity of the vulnerability and the type of vulnerability
    """
    proc = subprocess.Popen(['cppcheck', '--enable=warning', '--xml', filename], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    (out, err) = proc.communicate()
    xml_parser = BeautifulSoup(out, features='xml')

    if xml_parser.error:
        errors = xml_parser.findAll('error')
        typ = None
        line = None
        count = 0
        desc = None

        for error in errors:
            if error['severity'] == "error":
                typ = 'error'
                line = error['line']
                count += 1
                desc = error['msg']
            elif error['severity'] == 'warning':
                typ = 'warning'
                line = error['line']
                desc = error['msg']
                count += 1

        if count > 0:
            return typ, count, line, desc

    return None, 0, None, None


def process_json_file():
    """
    Process the JSON file with the list of vulnerabilites
    """
    json_file = os.path.expanduser(args.path)
    with open(json_file) as data_file:
        data = json.load(data_file)

        with open(args.output, 'wb') as csvfile:
            fieldnames = ['answer_id', 'snippet_no', 'parent_id', 'score', 'owner_id', 'cpp_type', 'cpp_count', 'cpp_error_line', 'cpp_description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ix in range(len(data)):
                filename = str(data[ix]["AnswerId"]) + "_" + str(data[ix]['SnippetNumber']) + "_" + str(
                    data[ix]["ParentId"]) + "_" + str(data[ix]["Score"]) + "_" + str(data[ix]["OwnerUserId"]) + ".c"

                # Write the code to a temporary file
                with open(filename, 'a') as the_file:
                    the_file.write(data[ix]["Code"].encode("utf-8"))
                (cpp_type, cpp_count, cpp_error_line, cpp_description) = process_cppcheck(filename)
                os.remove(filename)

                writer.writerow({'answer_id': str(data[ix]["AnswerId"]),
                                 'snippet_no': str(data[ix]['SnippetNumber']),
                                 'parent_id': str(data[ix]["ParentId"]),
                                 'score': str(data[ix]["Score"]),
                                 'owner_id': str(data[ix]["OwnerUserId"]),
                                 'cpp_type': cpp_type,
                                 'cpp_count': cpp_count,
                                 'cpp_error_line': cpp_error_line,
                                 'cpp_description': cpp_description
                                 })


parser = argparse.ArgumentParser(description='Process Stack Overflow Answers JSON.')
parser.add_argument('-i', dest='path', metavar='path', help='path of the json file', required=True)
parser.add_argument('-o', dest='output', metavar='output', help='The name of the output file', required=True)
args = parser.parse_args()
process_json_file()