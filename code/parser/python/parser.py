#!/usr/bin/python
"""
    Parser module that will be used for the Expoist project.
    This parser will convert stack overflow metadata xml
    into useable information for the vulnerability assessment
    and evluation.

    Python 2.7.12

    @author Joshua T. Pritchett <jtpritchett@wpi.edu>
    @copyright ALAS LAB WPI, 2016
"""
#User defined variable
from    tables  import session, Questions, Answers
#Built in Modules
from    bs4     import BeautifulSoup
import  sys
import  getopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


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
    # Questions
    post_id                     = 0
    title                       = ''
    view_count                  = 0
    answer_count                = 0
    favorite_count              = 0
    accepted_answer_id          = 0

    # Answers
    answer_id                   = 0
    parent_id                   = 0
    code                        = ''

    # Common
    score                       = 0
    comment_count               = 0
    owner_user_id               = 0
    last_editor_user_id         = 0
    last_editor_display_name    = ''
    last_edit_date              = '' #datetime
    last_activity_date         = '' #datetime
    creation_date               = '' #datetime
    community_owned_date        = '' #datetime
    body                        = ''
    tags                        = ''

    #Database objects
    new_question    = None
    new_answer      = None
    #  Iterate over the entire metadata dump file to produce the
    #  results for the data base. NOTE: the tags are not capital
    #  specific
    for row in rows:
        #Check for post to exist based on post type id
        if row.get('posttypeid'):
            post_type_id = int(row.get('posttypeid'))

            #Check for tags for the given post
            if row.get('tags'):
                tags = row.get('tags')
            else:
                continue

            print tags
            #Make sure tags match either C or C++
            if (tags.find('<c>') and tags.find('<c++>'))  != -1:
                #Generic types that should be pulled for either question or answer
                if row.get('score'):                    score                       = int(row.get('score'))
                if row.get('commentcount'):             comment_count               = int(row.get('commentcount'))
                if row.get('owneruserid'):              owner_user_id               = int(row.get('owneruserid'))
                if row.get('lasteditoruserid'):         last_editor_user_id         = row.get('lasteditoruserid')
                if row.get('lasteditordisplayname'):    last_editor_display_name    = row.get('lasteditordisplayname')
                if row.get('lasteditdate'):             last_edit_date              = datetime.strptime(row.get('lasteditdate'), "%Y-%m-%dT%H:%M:%S.%f")
                if row.get('lastactivitydate'):         last_activity_date          = datetime.strptime(row.get('lasta:tivitydate'), "%Y-%m-%dT%H:%M:%S.%f")
                if row.get('creationdate'):             creation_date               = datetime.strptime(row.get('creationdate'), "%Y-%m-%dT%H:%M:%S.%f")
                if row.get('communityowneddate'):       community_owned_date        = datetime.strptime(row.get('communityowneddate'), "%Y-%m-%dT%H:%M:%S.%f")
                if row.get('body'):                     body                        = row.get('body')

                #The post type id is a question
                if post_type_id == 1:
                    print 'it is a question'
                    if row.get('id'):               post_id             = int(row.get('id'))
                    if row.get('title'):            title               = row.get('title')
                    if row.get('viewcount'):        view_count          = int(row.get('viewcount'))
                    if row.get('answercount'):      answer_count        = int(row.get('answercount'))
                    if row.get('favoritecount'):    favorite_count      = int(row.get('favoritecount'))
                    if row.get('acceptedanswerid'): accepted_answer_id  = int(row.get('acceptedanswerid'))
                    print title
                    print creation_date
                    new_question = Questions(post_id = post_id, creation_date = creation_date, title = title, tags = tags, body = body, score = score, view_count = view_count, \
                                        answer_count = answer_count, comment_count = comment_count, favorite_count = favorite_count, owner_user_id = owner_user_id, \
                                        accepted_answer_id = accepted_answer_id, last_editor_user_id = last_editor_user_id, last_editor_display_name = last_editor_display_name, \
                                        last_edit_date = last_edit_date, last_activity_date = last_activity_date, community_owned_date = community_owned_date)
                #This type of post is an answer
                elif post_type_id == 2:
                    if row.get('answerid'): answer_id   = int(row.get('answerid'))
                    if row.get('parentid'): parent_id   = int(row.get('parentid'))
                    if row.get('code'):     code        = int(row.get('code'))

                    new_answer = Answers(answer_id, parent_id = parent_id, owner_user_id = owner_user_id, tags = tags, code = code, body = body, score = score, \
                                         comment_count = comment_count, last_editor_user_id = last_editor_user_id, last_editor_display_name = last_editor_display_name, \
                                         last_edit_date = last_edit_date, last_activity_date = last_activity_date, creation_date = creation_date, community_owned_date = community_owned_date)
                else:
                    print 'Not a question or answer skipping'
                    continue
                #END Post Type CHECK
                try:
                    if new_question:
                        print 'there is a question to add'
                        session.add(new_question)
                    elif new_answer:
                        print 'there is a new answer'
                        session.add(new_answer)
                    else:
                        print 'there is nothing'

                except:
                    print 'something went wrong with db session'
            else:
                print 'Not the tag we are looking for'
                #END TAG TYPE CHECK
        else:
            print 'There is no post type id'
            continue

    #Commit all the values we found
    session.commit()
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
