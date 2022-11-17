#AUTHOR: Ryan Perez
#FILENAME: resumeParser.py
#SPECIFIACTION: Develop a resume parser that extracts all of the important information
# out of a resume. The expected input is a docx resume and the expected output is 
# data retrieved from the resume like name, email, phone number, education, and skills.
#FOR: CS 3368 Introduction to Artificial Intelligence Section 001

import spacy
import operator
import re
import ssl
import docx2txt
import nltk

DATABASE_SKILLS = [
    'javascript',
    'c#',
    'c',
    'c++',
    'python',
    'mysql',
    'angular',
    'microsoft powerpoint',
    'microsoft word',
    'java',
    'swift',
    'stocking and organizing',
    'psychology',
    'ethics',
    'social learning',
]

DATABASE_EDUCATION_KEYWORDS = [
    'school',
    'university',
    'institute',
    'college',
    'high school',
]

from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm') # Loads data from a pre trained model

# Error catching utilizing when downloading nltk data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# You need to uncomment these downloads when you initially run the program
#nltk.download('maxent_ne_chunker')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('words')

#NAME: extractTextDocx
#PARAMETERS: path, string of the resume file name
#PURPOSE: The function extracts the data from a docx document and converts it to raw text
#PRECONDITION: Input string leads to a valid document
#POSTCONDITION: String containing the raw text is returned
def extractTextDocx(path):
        try:
            text = docx2txt.process(path) # A string which stores the raw text from a document
            # Removes all of the tab spacing in the raw text
            if text:
                return text.replace('\t',' ')
        except:
            print('Error: ' + path + ' is an invalid document')
            return 0

#NAME: extractName
#PARAMETERS: text, string containing the raw text from an inputted resume
#PURPOSE: The function extracts a name out of the raw data from a resume
#PRECONDITION: Input string contains a first and last name
#POSTCONDITION: String containing a person's first and last name is returned
def extractName(text):
    # Creates a pattern for the first and last name, which are both proper nouns
    pattern = [{'POS': 'PROPN'},
               {'POS': 'PROPN'}]

    # NLP Matcher Object
    spacyMatcher = Matcher(nlp.vocab)
    spacyMatcher.add('NAME', [pattern])
    
    nlpText = nlp(text) # String containing raw resume text enabled for spacy package
    potentialMatches = spacyMatcher(nlpText) # Set holding the match id's of potential names
        
    # Returns a string of the matches that have the desired pattern
    for matchId, start, end in potentialMatches:
        match = nlpText[start:end]  # Spacy token that retrieves the string data from a match
        return match.text # Converts the spacy token to a string and returns it

#NAME: extractEmail
#PARAMETERS: text, string containing the raw text from an inputted resume
#PURPOSE: The function extracts an email out of the raw data from a resume 
#PRECONDITION: Input string contains a valid email
#POSTCONDITION: String containing a valid email is returned
def extractEmail(text):
    data = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", text) # A regular expression which is used to find special symbols such as @
    if data:
        email = data[0].split()[0].strip(';') # Extracts the email from the set data
        return email

#NAME: extractPhoneNumber
#PARAMETERS: text, string containing the raw text from an inputted resume
#PURPOSE: The function extracts a phone number out of the raw data from a resume
#PRECONDITION: Input string contains a valid phone number
#POSTCONDITION: String containing a valid phone number is returned
def extractPhoneNumber(text):
    regExp = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]') # A regular expression which is able to identify a phone number
    phoneNumber = re.findall(regExp, text) # A set that stores all of the phone numbers found in the raw text

    if phoneNumber:
        strNum = ''.join(phoneNumber[0]) # A string that is used to convert the phoneNumber variable from an array to a string
        
        return strNum

    return 0
        
#NAME: extractSkills
#PARAMETERS: text, string containing the raw text from an inputted resume
#PURPOSE: The function extracts all of the skills from a resumes raw data
#PRECONDITION: Input string contains atleast 1 valid skill
#POSTCONDITION: List containing all of the valid skills is returned
def extractSkills(text):
    stopWords = set(nltk.corpus.stopwords.words('english')) # A set that stores a copy of the most common stopwords
    tokens = nltk.tokenize.word_tokenize(text) # A set that stores a tokenized copy of the raw text
    tokensFiltered = [word for word in tokens if word not in stopWords] # A set that stores a filtered version of the tokens from the raw text
    tokensFiltered = [word for word in tokens if word.isalpha()]

    skills = [] # A list that stores all of the valid skills

    # Crossreferences the filtered tokens with the strings in the skills database and adds any matches to the skillsFound set
    for token in tokens:
        if token.lower() in DATABASE_SKILLS:
            skills.append(token)

    nounChunks = list(map(' '.join, nltk.everygrams(tokens, 2, 3))) # A list that stores bigrams/trigrams from the filtered tokens

    # Crossreferences the ngrams in the bigrams/trigrams with the strings in the skills database and adds any matches to the skillsFound set
    for token in nounChunks:
        token = token.lower().strip()
        if token in DATABASE_SKILLS:
            skills.append(token)
 
    return [i.capitalize() for i in set([i.lower() for i in skills])]

#NAME: extractEducation
#PARAMETERS: text, string containing the raw text from an inputted resume
#PURPOSE: The function extracts all of the education(s) from a resumes raw data
#PRECONDITION: Input string contains atleast 1 valid education
#POSTCONDITION: Set containing all of the education(s) is returned
def extractEducation(text):
    education = set() # A set that stores all of the educations found in organziations
    organizations = [] # A list that stores all of the tokens with the label ORGANIZATION

    # Breaks the raw text into tokens and finds all the tokens that are labeled as a ORGANIZAITON
    for t in nltk.sent_tokenize(text):
        for c in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(t))):
            if hasattr(c, 'label') and c.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in c.leaves()))
    
    # Crossreferences the filtered tokens(organizations) with the strings in the school related keywords database and adds any matches to the education set
    for organization in organizations:
        for keyword in DATABASE_EDUCATION_KEYWORDS:
            if operator.ne(organization.lower().find(keyword), -1):
                education.add(organization)
 
    return education

#NAME: if __name__ == '__main__' (main function)
#PARAMETERS: none
#PURPOSE: The function retrieves informataion from an inputted resume and prints it to the screen
#PRECONDITION: The user has access to the console in order to type in the name of the resume docx file
#POSTCONDITION: The name, email, phone number, education(s), and skill(s) are printed to the console. In the future they will be submitted into a database 
if __name__ == '__main__':
    print('\n')
    loopCondition = 0 # An integer that is used to determine whether or not a user has entered a valid document name
    documentName = '' # A string that stores the user inputted document name
    # Continually asks the user for a valid input until one is given
    while loopCondition == 0:
        documentName = input("Enter the name of your resume document without the .docx extension:") 
        text = extractTextDocx('./' + documentName + '.docx') # A string that stores the result of the extractTextDocx function
        if(text != 0):
            loopCondition = 1
    
    print('\nDATA FROM DOCUMENT ' + documentName.upper() + ':\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    name = extractName(text) # A string that stores the result of the extractName function
    email = extractEmail(text) # A string that stores the result of the extractEmail function
    phoneNumber = extractPhoneNumber(text) # A string that stores the result of the extractPhoneNumber function
    educations = extractEducation(text) # A list that stores the result of the extractEducation function
    skills = extractSkills(text) # A list that stored the result of the extractSkills function

    # Prints out the name found in the raw text if one is found
    if name:
        print('Name: ' + name)
         
    # Prints out the email found in the raw text if one is found
    if(email):
        print('\n' + 'Email: ' + email + '\n')

    # Prints out the phone number found in the raw text if one is found
    if(phoneNumber):
        print('Phone Number: ' + phoneNumber + '\n')
    
    # Prints out all of the educations found in the raw text if atleast one is found
    if (educations):
        print('Educations:')
        for education in educations:
            print(education)
        
    # Prints out all of the skills found in the raw text if atleast one is found
    if(skills):
        print('\nSkills:')
        for skill in skills:
            print('- ' + skill)

    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


#REFERENCES
# NLTK: https://www.nltk.org/book_1ed/ch07.html
#       https://www.nltk.org/install.html
# doc2txt: https://pypi.org/project/doc2text/
# Spacy: https://spacy.io/usage
# SSL: https://pypi.org/project/ssl/
# Github: https://gist.github.com/onyxfish/322906/2089c1f9eb10f320d552e69d99503dbeb677e19b
# APILayer: https://blog.apilayer.com/build-your-own-resume-parser-using-python-and-nlp/#Extracting_text_from_PDF_files
# Stack overflow: https://stackoverflow.com/questions/24398536/named-entity-recognition-with-regular-expression-nltk
# Towards Data Science: https://towardsdatascience.com/a-practitioners-guide-to-natural-language-processing-part-i-processing-understanding-text-9f4abfd13e72

