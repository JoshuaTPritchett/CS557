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
        count = 0
        desc = None

        for line in out.split('\n'):
            if line:
                match = re.match('.*:  \[(\d)\] \((\w+)\) (\w+):.*', line, re.M | re.I)

                if match:
                    count += 1
                    sn = int(match.group(1))

                    if sn == 5:
                        high = 5
                        desc = match.group(2) + ' ' + match.group(3)
                    elif sn == 4:
                        if high < 4:
                            high = 4
                            desc = match.group(2) + ' ' + match.group(3)
                    elif sn == 3:
                        if high < 3:
                            high = 3
                            desc = match.group(2) + ' ' + match.group(3)

                else:
                    print "nomatch: ", line

        if count > 0:
            return count, high, desc

    return 0, None, None


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
        high = 0
        count = 0
        desc = None

        for error in errors:
            if error['severity'] == "error":
                high = 4
                count += 1
                desc = 'error'
            elif error['severity'] == 'warning':
                if high < 3:
                    high = 3
                    desc = 'warning'
                count += 1

        if high > 0:
            return count, high, desc

    return 0, None, None


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
        high = 0
        desc = None

        for vulnerability in vulnerabilities:
            if vulnerability.severity.text == 'Very High':
                high = 4
                if vulnerability.type:
                    desc = vulnerability.type.text
                break
            elif vulnerability.severity.text == 'High':
                high = 3
                if vulnerability.type:
                    desc = vulnerability.type.text
            elif vulnerability.severity.text == 'Medium':
                if high < 2:
                    high = 2
                    if vulnerability.type:
                        desc = vulnerability.type.text
            else:
                if high < 1:
                    high = 1
                    if vulnerability.type:
                        desc = vulnerability.type.text

        return len(vulnerabilities), high, desc

    else:
        return 0, None, None


def process_json_file():
    """
    Process the JSON file with the list of vulnerabilites
    """
    json_file = os.path.expanduser(args.path)
    with open(json_file) as data_file:
        data = json.load(data_file)

        with open(args.output, 'wb') as csvfile:
            fieldnames = ['answer_id', 'snippet_no', 'parent_id', 'score', 'owner_id', 'rats_count', 'rats_severity',
                          'rats_type', 'cpp_count', 'cpp_severity', 'cpp_type', 'ff_count', 'ff_severity', 'ff_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for ix in range(len(data)):
                filename = str(data[ix]["AnswerId"]) + "_" + str(data[ix]['SnippetNumber']) + "_" + str(
                    data[ix]["ParentId"]) + "_" + str(data[ix]["Score"]) + "_" + str(data[ix]["OwnerUserId"]) + ".c"

                # Write the code to a temporary file
                with open(filename, 'a') as the_file:
                    the_file.write(data[ix]["Code"].encode("utf-8"))
                (rats_count, rats_severity, rats_type) = process_rats(filename)
                (cpp_count, cpp_severity, cpp_type) = process_cppcheck(filename)
                (ff_count, ff_severity, ff_type) = process_flawfinder(filename)
                os.remove(filename)

                writer.writerow({'answer_id': str(data[ix]["AnswerId"]),
                                 'snippet_no': str(data[ix]['SnippetNumber']),
                                 'parent_id': str(data[ix]["ParentId"]),
                                 'score': str(data[ix]["Score"]),
                                 'owner_id': str(data[ix]["OwnerUserId"]),
                                 'rats_count': rats_count,
                                 'rats_severity': rats_severity,
                                 'rats_type': rats_type,
                                 'cpp_count': cpp_count,
                                 'cpp_severity': cpp_severity,
                                 'cpp_type': cpp_type,
                                 'ff_count': ff_count,
                                 'ff_severity': ff_severity,
                                 'ff_type': ff_type})


parser = argparse.ArgumentParser(description='Process Stack Overflow Answers JSON.')
parser.add_argument('-i', dest='path', metavar='path', help='path of the json file', required=True)
parser.add_argument('-o', dest='output', metavar='output', help='The name of the output file', required=True)
args = parser.parse_args()
process_json_file()