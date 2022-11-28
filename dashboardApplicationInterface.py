#AUTHOR: Ryan Perez
#FILENAME: dashboardApplicationInterface.py
#SPECIFIACTION: Develop a Python based user interface that has the ability to search
# through a database of resumes. The user(employer) can search for a candidates resume
# by their name, email, phone number, skill, or education. The database of resumes contains
# all of the resumes that have been submitted through the submutApplicationInterface program.
# The expected input is the csv resume database and the expected output is resume data for the
# resumes that match the user's search conditions such as a name or skill.
#FOR: CS 3368 Introduction to Artificial Intelligence Section 001

import PySimpleGUI as sg
import csv
import re
from itertools import chain

# A PySimpleGUI theme that is customized for the dashboard application
newTheme = {'BACKGROUND': '#404258',
                'TEXT': 'white',
                'INPUT': 'white',
                'TEXT_INPUT': '#000000',
                'SCROLL': 'white',
                'BUTTON': ('white', '#6B728E'),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 3,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0
            }

# Adds the newly created theme to the PySimpleGUI themes
sg.theme_add_new('DashboardTheme', newTheme)
# Switches the default theme to the new theme
sg.theme('Dashboard Theme')

whiteSpace = "                                        "
occupied = False # A boolean statement that is used to determine whether a window is currently occupying window2
pressed1 = False # A boolean statement that is used to determine whether or not a button is toggled
pressed2 = False # A boolean statement that is used to determine whether or not a button is toggled
pressed3 = False # A boolean statement that is used to determine whether or not a button is toggled
pressed4 = False # A boolean statement that is used to determine whether or not a button is toggled
pressed5 = False # A boolean statement that is used to determine whether or not a button is toggled
mode = 0 # A integer that determines which kind of search is being utilized
#mode 0 = none, mode 1 = name, mode 2 = email, mode 3 = phonenumber, mode 4 = skill, mode 5 = education

#NAME: formatPhonenumber
#PARAMETERS: text, string containing a raw phone number a.k.a only digits
#PURPOSE: The function formats a raw phone number into a phone number that contains dashes and parenthesis ex: 2101234567 -> (210) 123-4567
#PRECONDITION: Input string contains a valid phone number
#POSTCONDITION: String containing a formatted phone number is returned
def formatPhonenumber(phoneNumber):
    # Checks if the phone number is a valid # of digits
    if(len(phoneNumber) >= 7):
        # Attempts to format a phone number using parenthesis and dashes
        try:
            return('(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', phoneNumber)))
        # If the phone number lacks the # of digits to use parenthesis, it simply uses dashes
        except:
            return('%s-%s' % tuple(re.findall(r'\d{4}$|\d{3}', phoneNumber)))
    else:
        return "n/a"

#NAME: searchName
#PARAMETERS: text, string containing a name (can be first, last, or both)
#PURPOSE: The function checks to see if the inputted name matches one in the database
#PRECONDITION: Input string contains a valid first, last, or full name
#POSTCONDITION: List of resumes that have a matching name is returned
def searchName(name):
    resumeList = [[None for _ in range(7)] for _ in range(100)] # An empty list that is created for the resumes that are returned
    name = name.lower() # A string containing the inputted name which is converted to lowercase in order to avoid capitalization issues
    index = 0 # A integer that is used to keep track of the index(row) in the resumeList variable
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file) # A list which contains the contents from the csv file
        for row in csvreader:
            lowercaseFirstName = row[1].lower() # A string which stores the current rows first name in lowercase form in order to avoid capitalization issues
            lowercaseLastName = row[2].lower() # A string which stores the current rows last name in lowercase form in order to avoid capitalization issues
            lowercaseFullName = row[1].lower() + " " + row[2].lower() # A string which stores the current rows full name in lowercase form in order to avoid capitalization issues
            # Compares the inputted name to each resume candidates full name
            if(lowercaseFullName == name): 
                resumeList[index][0] = row[0]
                resumeList[index][1] = row[1]
                resumeList[index][2] = row[2]
                resumeList[index][3] = row[3]
                resumeList[index][4] = row[4]
                resumeList[index][5] = row[5]
                resumeList[index][6] = row[6]
                index += 1
            # Compares the inputted name to each resume candidates first name
            elif(lowercaseFirstName == name):
                resumeList[index][0] = row[0]
                resumeList[index][1] = row[1]
                resumeList[index][2] = row[2]
                resumeList[index][3] = row[3]
                resumeList[index][4] = row[4]
                resumeList[index][5] = row[5]
                resumeList[index][6] = row[6]
                index += 1
            # Compares the inputted name to each resume candidates last name
            elif(lowercaseLastName == name):
                resumeList[index][0] = row[0]
                resumeList[index][1] = row[1]
                resumeList[index][2] = row[2]
                resumeList[index][3] = row[3]
                resumeList[index][4] = row[4]
                resumeList[index][5] = row[5]
                resumeList[index][6] = row[6]
                index += 1
    return resumeList

#NAME: searchEmail
#PARAMETERS: text, string containing a email
#PURPOSE: The function checks to see if the inputted email matches one in the database
#PRECONDITION: Input string contains a valid email
#POSTCONDITION: List of resumes that have a matching email is returned
def searchEmail(email):
    resumeList = [[None for _ in range(7)] for _ in range(100)] # An empty list that is created for the resumes that are returned
    email = email.lower() # A string containing the inputted email which is converted to lowercase in order to avoid capitalization issues
    index = 0 # A integer that is used to keep track of the index(row) in the resumeList variable
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file) # A list which contains the contents from the csv file
        for row in csvreader:
            lowercaseEmail = row[3].lower() # A string containing a rows(candidates) email which is converted to lowercase in order to avoid capitalization issues
            # Compares the inputted email to each resume candidates email
            if(lowercaseEmail == email):
                resumeList[index][0] = row[0]
                resumeList[index][1] = row[1]
                resumeList[index][2] = row[2]
                resumeList[index][3] = row[3]
                resumeList[index][4] = row[4]
                resumeList[index][5] = row[5]
                resumeList[index][6] = row[6]
                index += 1
    return resumeList

#NAME: searchPhonenumber
#PARAMETERS: text, string containing a phone number
#PURPOSE: The function checks to see if the inputted phone number matches one in the database
#PRECONDITION: Input string contains a valid phone number
#POSTCONDITION: List of resumes that have a matching phone number is returned
def searchPhonenumber(phonenumber):
    resumeList = [[None for _ in range(7)] for _ in range(100)] # An empty list that is created for the resumes that are returned
    index = 0 # A integer that is used to keep track of the index(row) in the resumeList variable
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file) # A list which contains the contents from the csv file
        phonenumber = re.sub(r'[^0-9]','',phonenumber) # Converts the input phone number which possibly contains dashes and parenthesis into a plain phone number
        for row in csvreader:
            plainPhonenumber = row[4] # A string which stores the current rows phone number in order to compare
            plainPhonenumber = re.sub(r'[^0-9]','',plainPhonenumber) # Converts the phone number which possibly contains dashes and parenthesis into a plain phone number

            # Compares the inputted phone number to each resume candidates phone number
            if(plainPhonenumber == phonenumber):
                resumeList[index][0] = row[0]
                resumeList[index][1] = row[1]
                resumeList[index][2] = row[2]
                resumeList[index][3] = row[3]
                resumeList[index][4] = row[4]
                resumeList[index][5] = row[5]
                resumeList[index][6] = row[6]
                index += 1
    return resumeList

#NAME: searchSkill
#PARAMETERS: text, string containing a skill
#PURPOSE: The function checks to see if the inputted skill matches one in the database
#PRECONDITION: Input string contains a valid skill
#POSTCONDITION: List of resumes that have a matching skill is returned
def searchSkill(skill):
    resumeList = [[None for _ in range(7)] for _ in range(100)] # An empty list that is created for the resumes that are returned
    skill = skill.lower() # A string containing the inputted skill which is converted to lowercase in order to avoid capitalization issues
    index = 0 # A integer that is used to keep track of the index(row) in the resumeList variable
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file) # A list which contains the contents from the csv file
        for row in csvreader:
            skillsList = row[6].split(".") # A list which splits up each rows(candidates) skills into individual elements using . as a delimeter  
            # Compares each rows(candidates) skills to the inputted skill
            for s in skillsList:
                s = s.lower() # A String representing a skill which is converted to lowercase in order to avoid capitalization issues

                if(s == skill and s != ''):
                    resumeList[index][0] = row[0]
                    resumeList[index][1] = row[1]
                    resumeList[index][2] = row[2]
                    resumeList[index][3] = row[3]
                    resumeList[index][4] = row[4]
                    resumeList[index][5] = row[5]
                    resumeList[index][6] = row[6]
                    index += 1
    return resumeList

#NAME: searchEducation
#PARAMETERS: text, string containing a education
#PURPOSE: The function checks to see if the inputted education matches one in the database
#PRECONDITION: Input string contains a valid education
#POSTCONDITION: List of resumes that have a matching education is returned
def searchEducation(education):
    resumeList = [[None for _ in range(7)] for _ in range(100)] # An empty list that is created for the resumes that are returned
    education = education.lower() # A string containing the inputted education which is converted to lowercase in order to avoid capitalization issues
    index = 0 # A integer that is used to keep track of the index(row) in the resumeList variable
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file) # A list which contains the contents from the csv file
        for row in csvreader:
            educationsList = row[5].split(".") # A list which splits up each rows(candidates) educations into individual elements using . as a delimeter  

            # Compares each rows(candidates) educations to the inputted education
            for e in educationsList:
                e = e.lower()  # A String representing a education which is converted to lowercase in order to avoid capitalization issues

                if(e == education and e != ''):
                    resumeList[index][0] = row[0]
                    resumeList[index][1] = row[1]
                    resumeList[index][2] = row[2]
                    resumeList[index][3] = row[3]
                    resumeList[index][4] = row[4]
                    resumeList[index][5] = row[5]
                    resumeList[index][6] = row[6]
                    index += 1
    return resumeList

#NAME: getAllNames
#PARAMETERS: none
#PURPOSE: The function gets all of the names within the resume database
#PRECONDITION: Resume database contains atleast 1 resume
#POSTCONDITION: List of all name(s) from the resume database is returned
def getAllNames():
    nameList = [] # A list which stores the names found in the database
    skip = 1 # A integer that is used to skip the first row in a csv file, as that is the structure row
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # Skips the first row / index in the csvreader list
            if skip == 1:
                skip = 0
            else:
                nameList.append(row[1] + " " + row[2]) # Appends a rows(candidates) full name to the list of names
    return nameList

#NAME: getAllEmails
#PARAMETERS: none
#PURPOSE: The function gets all of the emails within the resume database
#PRECONDITION: Resume database contains atleast 1 email
#POSTCONDITION: List of all email(s) from the resume database is returned
def getAllEmails():
    emailList = [] # A list which stores the emails found in the database
    skip = 1 # A integer that is used to skip the first row in a csv file, as that is the structure row
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file)
        # Skips the first row / index in the csvreader list
        for row in csvreader:
            if skip == 1:
                skip = 0
            else:
                emailList.append(row[3]) # Appends a rows(candidates) email to the list of emails
    return emailList

#NAME: getAllPhonenumbers
#PARAMETERS: none
#PURPOSE: The function gets all of the phone numbers within the resume database
#PRECONDITION: Resume database contains atleast 1 phone number
#POSTCONDITION: List of all phone number(s) from the resume database is returned
def getAllPhonenumbers():
    phoneList = [] # A list which stores the phone numbers found in the database
    skip = 1 # A integer that is used to skip the first row in a csv file, as that is the structure row
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file)
        # Skips the first row / index in the csvreader list
        for row in csvreader:
            if skip == 1:
                skip = 0
            else:
                phoneList.append(formatPhonenumber(row[4])) # Appends a rows(candidates) phone number to the list of phone numbers
    return phoneList

#NAME: getAllSkills
#PARAMETERS: none
#PURPOSE: The function gets all of the skills within the resume database
#PRECONDITION: Resume database contains atleast 1 skill
#POSTCONDITION: List of all skill(s) from the resume database is returned
def getAllSkills():
    skillList = [] # A list which stores the skills found in the database
    skip = 1 # A integer that is used to skip the first row in a csv file, as that is the structure row
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file)
        # Skips the first row / index in the csvreader list
        for row in csvreader:
            if skip == 1:
                skip = 0
            else:
                skillList.append(row[6]) # Appends a rows(candidates) skill(s) to the list of skill(s)
    return skillList

#NAME: getAllEducations
#PARAMETERS: none
#PURPOSE: The function gets all of the educations within the resume database
#PRECONDITION: Resume database contains atleast 1 education
#POSTCONDITION: List of all education(s) from the resume database is returned
def getAllEducations():
    educationList = [] # A list which stores the educations found in the database
    skip = 1 # A integer that is used to skip the first row in a csv file, as that is the structure row
    with open("./resumeData.csv", 'r') as file:
        csvreader = csv.reader(file)
        # Skips the first row / index in the csvreader list
        for row in csvreader:
            if skip == 1:
                skip = 0
            else:
                educationList.append(row[5]) # Appends a rows(candidates) education(s) to the list of education(s)
    return educationList

#NAME: make_mainWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the main UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The main UI window is returned
def make_mainWin():
    layout = [[sg.Text(whiteSpace + "Search for candidates based on the following conditions:",pad=(0,20),font=('Arial', 15, 'bold'))],
            [sg.Button('Name',size=(30,1),pad=(20,20)), sg.Button('Email',size=(30,1),pad=(20,20)), sg.Button('Phone Number',size=(30,1),pad=(20,20))],
            [sg.Button('Skill(s)',size=(30,1),pad=(20,20)), sg.Button('Education(s)',size=(30,1),pad=(20,20)), sg.Exit(size=(30,1),pad=(20,20))]]
    return sg.Window('Employer Overview', layout, location=(800,600), margins=(10,10), finalize=True)

#NAME: make_nameWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the name search UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The name search UI window is returned
def make_nameWin():
    layout = [[sg.Text('Enter the name (first, last, or both) you desire:')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(50,1), k='-OUTPUT-')],
              [sg.Button('Submit'),sg.Button('Searchable Names')],
              [sg.Multiline(size=(50,15), k='-TEXTBOX-')],
              [sg.Button('Exit')]]
    return sg.Window('Name', layout, finalize=True)

#NAME: make_emailWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the email search UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The email search UI window is returned
def make_emailWin():
    layout = [[sg.Text('Enter the email you desire:')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(50,1), k='-OUTPUT-')],
              [sg.Button('Submit'),sg.Button('Searchable Emails')],
              [sg.Multiline(size=(50,15), k='-TEXTBOX-')],
              [sg.Button('Exit')]]
    return sg.Window('Email', layout, finalize=True)

#NAME: make_phonenumberWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the phonenumber search UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The phonenumber search UI window is returned
def make_phonenumberWin():
    layout = [[sg.Text('Enter the phone number you desire:')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(50,1), k='-OUTPUT-')],
              [sg.Button('Submit'),sg.Button('Searchable Phone Numbers')],
              [sg.Multiline(size=(50,15), k='-TEXTBOX-')],
              [sg.Button('Exit')]]
    return sg.Window('Phone Number', layout, finalize=True)

#NAME: make_skillWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the skill search UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The skill search UI window is returned
def make_skillWin():
    layout = [[sg.Text('Enter the skill you desire:')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(50,1), k='-OUTPUT-')],
              [sg.Button('Submit'),sg.Button('Searchable Skills')],
              [sg.Multiline(size=(50,15), k='-TEXTBOX-')],
              [sg.Button('Exit')]]
    return sg.Window('Skill(s)', layout, finalize=True)

#NAME: make_educationWin
#PARAMETERS: none
#PURPOSE: The function sets up the layout for the education search UI window  
#PRECONDITION: The program is running a.k.a the program hasn't been exited
#POSTCONDITION: The education search UI window is returned
def make_educationWin():
    layout = [[sg.Text('Enter the education you desire:')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(50,1), k='-OUTPUT-')],
              [sg.Button('Submit'),sg.Button('Searchable Educations')],
              [sg.Multiline(size=(50,15), k='-TEXTBOX-')],
              [sg.Button('Exit')]]
    return sg.Window('Education(s)', layout, finalize=True)

window1, window2 = make_mainWin(), None # Initializes the first window as the main window and initally disables the second window
# window1 represents the main window which never closes
# window2 represents the second window which can only have 1 up at a time like name, email, phonenumber, etc

# Event loop
while True:             
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        # If window2 is closing, mark as closed and make window2 unoccupied
        if window == window2:       
            window2 = None
            occupied = False
        # If window1 is closing, exit the program
        elif window == window1:     
            break
    elif event == '-IN-':
        # Used to display the users input in simulated realtime
        window['-OUTPUT-'].update(f'You entered {values["-IN-"]}')
    elif event == 'Name' and occupied == False:
        mode = 1
        occupied = True
        window2 = make_nameWin()
        nameList = getAllNames()
    elif event == 'Email' and occupied == False:
        mode = 2
        occupied = True
        window2 = make_emailWin()
        emailList = getAllEmails()
    elif event == 'Phone Number' and occupied == False:
        mode = 3
        occupied = True
        window2 = make_phonenumberWin()
        phoneList = getAllPhonenumbers()
    elif event == 'Skill(s)' and occupied == False:
        mode = 4
        occupied = True
        window2 = make_skillWin()
        skillsList = getAllSkills()
    elif event == 'Education(s)' and occupied == False:
        mode = 5
        occupied = True
        window2 = make_educationWin()
        educationList = getAllEducations()
    elif event == 'Searchable Names':
        pressed2 = not(pressed2) # Initially set to false, toggles back and forth when the button is pressed 
        s = '\n'.join([str(i) for i in nameList]) # A string which formats the spacing for the list of names
        if(pressed2):
            window['-TEXTBOX-'].update(s)
        else:
            window['-TEXTBOX-'].update('')
    elif event == 'Searchable Emails':
        pressed1 = not(pressed1) # Initially set to false, toggles back and forth when the button is pressed 
        s = '\n'.join([str(i) for i in emailList]) # A string which formats the spacing for the list of emails
        if(pressed1):
            window['-TEXTBOX-'].update(s)
        else:
            window['-TEXTBOX-'].update('')
    elif event == 'Searchable Phone Numbers':
        pressed3 = not(pressed3) # Initially set to false, toggles back and forth when the button is pressed 
        s = '\n'.join([str(i) for i in phoneList]) # A string which formats the spacing for the list of phone numbers
        if(pressed3):
            window['-TEXTBOX-'].update(s)
        else:
            window['-TEXTBOX-'].update('')
    elif event == 'Searchable Skills':
        pressed4 = not(pressed4) # Initially set to false, toggles back and forth when the button is pressed 
        skillsList2 = [] # A list that stores all of the skills from the resume database
        finalSkillsList = "" # A string that contains all of the skills from the resume database, with duplicates and blank entries deleted

        for skill in skillsList:
            # Ignores any n/a entries which means that they didn't have any skill(s) in their resume
            if(skill != 'n/a'): 
                skillsList2 += skill.split(".") # Adds all of the skill(s) from a row(candidate) to the total skill(s) list
        
        skillsList2 = [*set(skillsList2)] # Gets rid of any duplicate skills

        # Fills up the finalSkillsList string with all of the valid skill(s) from skillsList2, ignoring any blank entries
        for skill in skillsList2:
            if(skill != ''):
                finalSkillsList += skill + "\n"

        if(pressed4):
            window['-TEXTBOX-'].update(finalSkillsList)
        else:
            window['-TEXTBOX-'].update('')
    elif event == 'Searchable Educations':
        pressed5 = not(pressed5) # Initially set to false, toggles back and forth when the button is pressed 
        educationsList2 = [] # A list that stores all of the educations from the resume database
        finalEducationsList = "" # A string that contains all of the educations from the resume database, with duplicates and blank entries deleted

        for education in educationList:
            # Ignores any n/a entries which means that they didn't have any education(s) in their resume
            if(education != 'n/a'):
                educationsList2 += education.split(".") # Adds all of the education(s) from a row(candidate) to the total education(s) list
        
        educationsList2 = [*set(educationsList2)] # Gets rid of any duplicate educations

        # Fills up the finalEducationsList string with all of the valid education(s) from educationsList2, ignoring any blank entries
        for education in educationsList2:
            if(education != ''):
                finalEducationsList += education + "\n"

        if(pressed5):
            window['-TEXTBOX-'].update(finalEducationsList)
        else:
            window['-TEXTBOX-'].update('')
    elif event == 'Submit' and window2:
        Input = values["-IN-"]
        finalString = "" # A string that stores the final string which is displayed when a user(employer) hits the submit button
        if(mode == 1):
            nameFoundList = searchName(Input)
        elif(mode == 2):
            nameFoundList = searchEmail(Input)
        elif(mode == 3):
            nameFoundList = searchPhonenumber(Input)
        elif(mode == 4):
            nameFoundList = searchSkill(Input)
        elif(mode == 5):
            nameFoundList = searchEducation(Input)
        for row in nameFoundList:
            if(row[0] != None):
                # Formats the name portion of the final string
                firstName = "First Name: " + str(row[1]) + "\n"
                lastName = "Last Name: " + str(row[2]) + "\n"

                # Formats the email portion of the final string
                email = "Email: " + str(row[3]) + "\n"

                # Formats the phonenumber portion of the final string
                phone = str(row[4])
                phone = formatPhonenumber(phone)
                phone = "Phone: " + phone + "\n"   

                # Formats the education portion of the final string
                educations = "Education: \n"
                educationsList = row[5].split(".")
                for education in educationsList:
                    if(education != ''):
                        educations += "- " + education + "\n"

                # Formats the skill portion of the final string
                skills = "Skills: \n"
                skillsListFinal = row[6].split(".")
                for skill in skillsListFinal:
                    if(skill != ''):
                        skills += "- " + skill + "\n"

                finalString += firstName + lastName + email + phone + educations + skills + "\n" # A string that concatenates all of the portions of a resume

        window['-TEXTBOX-'].update(finalString)

window.close()