#/usr/bin/python
"""
    Parser module that will be used for the Expoist project.
    This parser will convert stack overflow metadata xml
    into useable information for the vulnerability assessment
    and evluation.


    @author Joshua T. Pritchett <jtpritchett@wpi.edu>
    @author Francisco Guerrero  <afguerrerohernan@wpi.edu>

    @date 09/26/2016
"""
from bs4 import BeautifulSoup
import sys
import getopt


"""
    Function to display the help for using the parsing system

"""
def display_help():
    print """
         -i input  file of choice
         -o output file of choice
         -h help
         example:
         parser.py -i <inputfile> -o <outputfile>
      """


"""
    Function that will parse the question information from the stack overflow
    metadata.

    @param xml  all of the parsed rows from the xml files

    @return void
"""
def get_question_information(rows):
    #@var list<string>
    #the associated question id that can be referenced on stack overflow
    question_ids                = []

   #@var list<string>
    #actual questions that were pulled from stack overflow
    questions                   = []

    #@var list<string>
    #question accepted answer ids
    question_accepted_ans_ids   = []

    #var list<string>
    #number of times the question was upvoted
    #could be important in determining how important the question is
    question_upvotes_scores     = []

    #var list<string>
    #titles? I feel like this may or may not be interesting consider revising later
    question_titles             = []

    question_code               = []
    #Iterate over all of the rows and append the associated values with their arrays
    for row in rows:
        print row.get('id')
        print row.get('body')
        if row.get('Id'):
            print 'there is an id'
            question_ids.append(row.get('Id'))
        else:
            print 'there is no Id tag'
        if row.get('Body'):
            questions.append(row.get('Body'))
        if row.get('AcceptedAnswerId'):
            question_accepted_ans_ids.append(row.get('AcceptedAnswerId'))
        if row.get('Score'):
            question_upvotes_scores.append(row.get('Score'))
        if row.get('Title'):
            question_titles.append(rows.get('Title'))
        if row.get('code'):
            print 'there is a code tag'
            question_code.append(rows.get('code'))
        else:
            print 'there is no code tag'
    print question_ids

"""
    Function to parse the xml files specified

    @param xml_file the input file to be parsed
    @param file     the output file to return any log information

    @return void
"""
def parse_xml(input_file, output_file):
    print 'Input file is: %s'   % input_file
    print 'Output file is: %s'  % output_file

    #Since we are parsing XML tag the file with xml
    #Pseudo html, required because xml parsing will ignore something like
    #<row /> within beautifulsoup
    soup = BeautifulSoup(open(input_file), "html.parser")
    rows = soup.find_all('row')
    print rows
    if rows:
        print 'there are rows'

    #print rows
    print get_question_information(rows)



"""
    The main function to run the parsing and sending for th http requests for
    the vargarant module

    @param list<string> the arguments that are inputted by the user

    @return void
"""
def main(argv):
    print 'WELCOME TO EXPOSIT'
    input_file = ''
    output_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'parser.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    #Check for input arguments
    if not opts:
        print 'Input incorrect try again'
        print 'parser.py -i <inputfile> -o <outputfile>'
    else:
        for opt, arg in opts:
            if opt == '-h':
                display_help()
                sys.exit()
            elif opt in ("-i", "--ifile"):
                input_file = arg
            elif opt in ("-o", "--ofile"):
                output_file = arg
        parse_xml(input_file, output_file)



if __name__ == "__main__":
    main(sys.argv[1:])
