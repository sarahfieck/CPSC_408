# Sarah Fieck
# Assignment 1: SQLite
# ID: 2374389

# Imports
import sqlite3
import csv
import requests
import json
import random
import string # https://www.geeksforgeeks.org/string-punctuation-in-python/

# Open Connection & Cursor
conn = sqlite3.connect('./StudentDB')
mycursor = conn.cursor()

# Importing the data from a CSV file
def import_data():
    data = open('./students.csv') # Path to CSV

    for row in csv.reader(data):
        fac = assign_faculty()
        mycursor.execute("INSERT INTO Students ('FirstName','LastName','Address','City','State','ZipCode','MobilePhoneNumber','Major','GPA','FacultyAdvisor') VALUES(?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],fac))

    conn.commit()

# Assign a Faculty at Random
def assign_faculty():
    import random
    faculty = ["Rene German","Nicole Elizabeth Polizzi","William Afton","Trixie Mattel","Michael Fahy"]
    random = random.randint(0,4)

    return faculty[random]

# Display the students
def display_students():
    mycursor.execute("SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Students WHERE isDeleted IS NULL")

    for row in mycursor.fetchall():
        print(row)

# Add a new Student to the table
def add_student():
    print("\n-----ADD A STUDENT-----")

    incomplete = True
    # Cycle through prompts until added

    while incomplete:

    # Checking First Name
        fname_rep = True
        while fname_rep:
            ready = True
            firstName = input("Please provide the student's first name using NO numbers or special characters: ")
            for chars in firstName:
                # print(chars)
                if chars.isdigit() is True or chars in string.punctuation:
                    ready = False
                    break

            if ready is False:
                print("The First Name provided is invalid. Please try again.")
            if ready is True:
                fname_rep = False
                break

    # Checking Last Name
        lname_rep = True
        while lname_rep:
            ready = True
            lastName = input("Please provide the student's last name using NO numbers or special characters: ")
            for chars in lastName:
                # print(chars)

                if chars.isdigit() is True or chars in string.punctuation:
                    ready = False

            if ready is False:
                print("The Last Name provided is invalid. Please try again.")
            if ready is True:
                lname_rep = False
                break

    # Checking GPA
        gpa = add_gpa()

    # Checking Major
        major = add_major()

    # Checking Faculty
        faculty = add_faculty()

    # Checking Address
        addy_rep = True
        while addy_rep:

            addy_num_rep = True
            addy_street_rep = True

            while addy_num_rep:
                ready = True
                addy_num = input("Please provide the student's address number using four integers only: ")
                for chars in addy_num:
                    # print(chars)

                    if chars.isdigit() is False:
                        ready = False

                if ready is False:
                    print("The address number can only be comprised of integers. Please try again.")

                if len(addy_num) > 4:
                    print("The address number can only be four digits long. Please try again.")
                    ready = False

                elif ready is True:
                    addy_num_rep = False
                    # break

            while addy_street_rep:
                ready = True
                addy_street = input("Please provide the student's street name using no numbers or punctuation: ")

                for chars in addy_street:
                    # print(chars)
                    if chars.isdigit() is True or chars in string.punctuation:
                        ready = False

                if ready is False:
                    print("The street name is invalid. Please only use street names with no numbers or punctuation.")

                if ready is True:
                    addy_street_rep = False

            addy = addy_num + " " + addy_street
            print("The address you have provided is ", addy)

            resp_rep = True
            while resp_rep:
                response = input("Is this correct? Type Y for Yes, and N for No.")

                if response.upper() == "Y":
                    resp_rep = False
                    addy_rep = False
                    print("Yay!")
                elif response.upper() == "N":
                    resp_rep = False

                    addy_rep = True
                    print("Okay, let's try again.")
                else:
                    print("Please answer with Y or N only.")

    # Checking City
        city = add_city()

    # Checking State
        state = add_state()

     # Checking Zipcode
        zip_rep = True
        while zip_rep:
            zip = input("Please provide the student's five digit zipcode number: ")
            try:
                zip = int(zip)
            except ValueError:
                print("That is not a proper zip code number, please try again.")
            else:
                if len(str(zip)) > 5 or len(str(zip)) <= 4:
                    print("Please provide 5 digit zip codes only!")
                else:
                    zip_rep = False

        # Checking Phone Number
        number = add_phone()

        # Confirmation
        print("\n-----Does the following information look correct?-----")
        print("\nFirst Name: ",firstName,"\nLast Name: ",lastName,"\nGPA: ",gpa,"\nMajor: ",major,"\nFaculty: ",faculty,"\nAddress: ",addy,"\nCity: ",city,"\nState: ",state,"\nZip Code: ",zip,"\nMobile Phone Number: ",number)

        while True:
            ready = input("\n-----Please type Y or N to confirm.-----")

            if ready.upper() == "Y":
                mycursor.execute(
                        "INSERT INTO Students ('FirstName','LastName','GPA','Major','FacultyAdvisor','Address','City','State','ZipCode','MobilePhoneNumber') VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (firstName, lastName, gpa, major, faculty, addy, city, state, zip, number))
                conn.commit()
                print("Student added!")

                incomplete = True
                break

            elif ready.upper() == "N":
                print("Please fill out the correct student information. Here we go again!")
                break

            else:
                print("Please answer with Y or N only.")

        if ready.upper() == "Y":
            incomplete = False
            break

# Input & Check a Major
def add_major():
    major_rep = True

    # List of majors
    possible_majors = ["Math","History","Computer Science","Communications","Physics","Psychology","Music","Theater","Data Science","Mechanical Engineering","Electrical Engineering","Dance","Business"]

    while major_rep:
        print("From the following majors: ")
        print("")

        for maj in possible_majors:
            print("   ",maj)

        major = input("\nPlease provide the correct major. Note the input is CASE SENSITIVE: ")

        for maj in possible_majors:
            if major == maj:
                major_rep = False
                break

        if major_rep == True:
            print("That is not a valid major. Please provide majors from the list only.")

    return major

# Add/Check GPA Function
def add_gpa():
    gpa_rep = True
    while gpa_rep:
        gpa = input("Please provide the student's GPA as a float value between 0.0 and 5.0: ")

        if float(gpa) <= 5.0: # Cannot be above 5.0 (Honor roll?)
            try:
                gpa = float(gpa)
                return gpa
            except ValueError:
                print("That is not a proper GPA value, please try again.")
            else:
                gpa_rep = False
        else:
            print("That is not a proper GPA value, please try again.")

# Add/Check Faculty Function
def add_faculty():
    faculty_rep = True

    # Established list of Esteemed Advisors
    faculty_list = ["Rene German", "Nicole Elizabeth Polizzi", "William Afton", "Trixie Mattel", "Michael Fahy"]

    while faculty_rep == True:
        print("From the following advisors: ")
        print("")
        for fac in faculty_list:
            print("   ", fac)

        faculty = input("\nPlease provide the name of the student's Faculty Advisor. Note the input is CASE SENSITIVE: ")
        for fac in faculty_list:
            if faculty == fac:
                faculty_rep = False
                return faculty

        if faculty_rep == True:
            print("That is not a valid Faculty Advisor. Please provide names from the list only.")

# Add/Check Phone Number Function
def add_phone():
    number_rep = True
    while number_rep:
        ready = True
        number = input("Please provide the student's mobile phone number, including area code (ex: XXX-XXX-XXXX): ")

        if len(number) == 12:
            count = 0
            for num in number:
                count += 1
                # print(num)

                if (count == 4 or count == 8) and num == "-":
                    ready = True

                elif (count != 4 or count != 8) and num.isdigit():
                    ready = True

                else:
                    ready = False
                    break
        else:
            print("Please follow the format XXX-XXX-XXXX.")
            ready = False

        if ready is False:
            print("The phone number is invalid. Please only use integers or dashes in a XXX-XXX-XXXX format when inputting the phone number.")

        if ready is True:
            number_rep = False
            return number

# Add/Check City to see if it is the right data type
def add_city():
    # Checking City
    city_rep = True
    while city_rep:
        ready = True
        city = input("Please provide the student's city of residence: ")
        for chars in city:
            # print(chars)
            if chars.isdigit() is True or chars in string.punctuation:
                ready = False

        if ready is False:
            print("The City Name provided is invalid. Please try again.")
        if ready is True:
            city_rep = False
            return city

# Add/Check State based on array of States in US
def add_state():
    # State List: https://usastatescode.com/state-array-json
    state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
                  'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                  'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                  'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                  'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
                  'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                  'West Virginia', 'Wisconsin', 'Wyoming']

    state_rep = True
    while state_rep:
        state = input("Please provide the full state name of the student's state of residence. Note the input is CASE SENSITIVE, so use proper capitalization please: ")
        if state in state_list:
            state_rep = False
            return state
        else:
            print("That is an invalid state name. Please try again!")
            state_rep = True


# Update Student Details
def update_student():
    print("\n-----UPDATE STUDENT DETAILS-----")

    mycursor.execute("SELECT StudentId FROM Students") # https://stackoverflow.com/questions/51112900/how-do-i-get-all-values-of-a-column-in-sqlite3
    id_list = [id[0] for id in mycursor.fetchall()]

    while True:
        key = input("Please provide the ID Number of the student you would like to update: ")
        name = mycursor.execute('SELECT FirstName, LastName FROM Students WHERE StudentId is ?',(key,))

        # Check if the ID matches with an existing ID
        if int(key) in id_list:
            print("\nYou have selected ", name.fetchall())
            break
        else:
            print("There is no student with this ID Number. Please try again.")

    while True:
        print("\nWhich attribute would you like to update?\n   1. Major\n   2. Faculty Advisor\n   3. Number")
        choice = input("\nPlease type one of the corresponding numbers to select your option.")
        choice_false = True

        if choice == "1":
            print("\nYou've selected Major.")
            choice_false = False
            major = add_major()

            while True:
                ready = input("\n-----Please type Y or N to confirm or decline these changes.-----")
                if ready.upper() != "Y" and ready.upper() != "N":
                    print("Please answer with Y or N only.")
                if ready.upper() == "Y":
                    break
                if ready.upper() == "N":
                    break

            if ready.upper() == "Y":
                mycursor.execute(
                    'UPDATE Students SET Major = ? WHERE StudentId = ?',
                    (major, key))
                conn.commit()
                print("Updated!")
                break

            elif ready.upper() == "N":
                print("Okay, nothing has happened. Let's try again.")
                continue

        if choice == "2":
            print("\nYou've selected Faculty Advisor")
            choice_false = False
            advisor = add_faculty()

            while True:
                ready = input("\n-----Please type Y or N to confirm or decline these changes.-----")
                if ready.upper() != "Y" and ready.upper() != "N":
                    print("Please answer with Y or N only.")
                if ready.upper() == "Y":
                    break
                if ready.upper() == "N":
                    break

            if ready.upper() == "Y":
                mycursor.execute(
                    'UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?',
                    (advisor, key))
                conn.commit()
                print("Updated!")
                break

            elif ready.upper() == "N":
                print("Okay, nothing has happened. Let's try again.")
                continue

        if choice == "3":
            print("\nYou've selected Phone Number")
            choice_false = False
            phone = add_phone()

            while True:
                ready = input("\n-----Please type Y or N to confirm or decline these changes.-----")
                if ready.upper() != "Y" and ready.upper() != "N":
                    print("Please answer with Y or N only.")
                if ready.upper() == "Y":
                    break
                if ready.upper() == "N":
                    break

            if ready.upper() == "Y":
                mycursor.execute(
                    'UPDATE Students SET MobilePhoneNumber = ? WHERE StudentId = ?',
                    (phone, key))
                conn.commit()
                print("Updated!")
                break

            elif ready.upper() == "N":
                print("Okay, nothing has happened. Let's try again.")
                continue

        if choice_false:
            print("That is not an option. Please try again!")

        if choice_false is False:
            break


# Delete a Student
def delete_student():
    print("\n-----DELETE STUDENT-----")
    mycursor.execute(
        "SELECT StudentId FROM Students")
    id_list = [id[0] for id in mycursor.fetchall()]

    while True:
        key = input("Please provide the ID Number of the student you would like to delete: ")
        if int(key) in id_list:
            name = mycursor.execute('SELECT FirstName, LastName FROM Students WHERE StudentId == ?', (key,))

        else:
            print("That is not a valid ID number. Please try again.")
            continue

        while True:
            print("\nYou've selected ",mycursor.fetchall())

            ready = input("\n-----Please type Y or N to confirm or decline these changes.-----")

            if ready.upper() != "Y" and ready.upper() != "N":
                print("Please answer with Y or N only.")

            if ready.upper() == "Y":
                mycursor.execute('UPDATE Students SET isDeleted = 1 WHERE StudentId = ?', (key,))
                conn.commit()
                print("Updated!")
                return

            if ready.upper() == "N":
                print("Okay, nothing has happened. Let's try again.")
                break

# Search up a Student
def search_student():
    # Add a menu of options to select what you want to search

    while True:
        print("\n-----SEARCH STUDENT BY ATTRIBUTE-----")
        print("\nFrom the following list:\n   1. Major\n   2. GPA\n   3. City\n   4. State\n   5. Advisor")
        select = input("\nPlease provide the corresponding number to select which attribute you would like to search by.")

        # Search by Major
        if select == "1":
            print("\n-----Search by Major-----")
            major = add_major()
            mycursor.execute('SELECT * FROM Students WHERE Major = ?',(major,))
            conn.commit()

            for maj in mycursor.fetchall():
                print(maj)

            print("\nIf there are no entries, there are no currently students who match that major.")
            return

        # Search by GPA
        if select == "2":
            print("\n-----Search by GPA-----")
            gpa = add_gpa()
            mycursor.execute('SELECT * FROM Students WHERE GPA = ?', (gpa,))
            conn.commit()

            for gpa in mycursor.fetchall():
                print(gpa)

            print("\nIf there are no entries, there are no students who match that GPA.")
            return

        # Search by City
        if select == "3":
            print("\n-----Search by City-----")
            city = add_city()
            mycursor.execute('SELECT * FROM Students WHERE City = ?', (city,))
            conn.commit()

            for city in mycursor.fetchall():
                print(city)

            print("\nIf there are no entries, there are no students who live in that city.")
            return

        # Search by State
        if select == "4":
            print("\n-----Search by State-----")
            state = add_state()
            print(state)
            mycursor.execute('SELECT * FROM Students WHERE State = ?', (state,))
            conn.commit()

            for state in mycursor.fetchall():
                print(state)

            print("\nIf there are no entries, there are no students who live in that state.")
            return

        # Search by Advisor
        if select == "5":
            print("\n-----Search by Advisor-----")
            fac = add_faculty()
            mycursor.execute('SELECT * FROM Students WHERE FacultyAdvisor = ?', (fac,))
            conn.commit()

            for fac in mycursor.fetchall():
                print(fac)

            print("\nIf there are no entries, there are no students who have that Faculty Advisor.")
            return

        else:
            print("Invalid selection. Please try again!")


# Menu & Function Implementation
mycursor.execute("SELECT name from sqlite_master WHERE type = 'table' AND name = 'Students'")
table = mycursor.fetchone()

if table is None:
    mycursor.execute(
        'CREATE TABLE Students(StudentId INTEGER PRIMARY KEY AUTOINCREMENT,FirstName TEXT,LastName TEXT,GPA REAL,Major TEXT,FacultyAdvisor TEXT,Address TEXT,City TEXT,State TEXT,ZipCode TEXT,MobilePhoneNumber TEXT, isDeleted INTEGER)')
    conn.commit()
    import_data()

while True:
    print("\n-----WELCOME TO THE STUDENT DATABASE-----\n\n   1. Display all Students and their Attributes\n   2. Add a New Student\n   3. Update a Student\n   4. Delete a Student by ID\n   5. Search Students by Attribute\n   6. Quit")
    select = input("\nPlease select an option by typing in the corresponding number: ")

    # Menu Option 1: Display the Students
    if select == "1":
        display_students()

    # Menu Option 2: Add a Student
    elif select == "2":
        add_student()

    # Menu Option 3: Update a Student
    elif select == "3":
        update_student()

    # Menu Option 4: Delete a Student
    elif select == "4":
        delete_student()

    # Menu Option 5: Search the Students
    elif select == "5":
        search_student()

    # Menu Option 6: End the Menu
    elif select == "6":
        break

    else:
        print("Invalid selection. Please input an integer of 1-6 based on the action you want to complete.")

# Close Cursor & Connection
mycursor.close()
conn.close()