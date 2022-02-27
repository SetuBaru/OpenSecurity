import json
import os
import random


class ManagementConsole:

    def __init__(self):
        self.current_path = os.getcwd()
        self.log_path = 'data/LOG.txt'
        self.user_database = 'vision/data/user-table.json'
        self.data_path = 'data/Data'

    def Add_user(self, student_name=None, student_id=None, email=None, pass1=None, pass2=None):
        if student_name is None:
            student_name = input('Enter the Student Name used for loging in: ')
        elif student_id is None:
            student_id = input('Enter ID NO. of prospective student: ')
        elif email is None:
            student_id = input("Enter email to use in registration: ")
        elif pass1 is None or pass2 is None:
            pass1 = input('Enter new password: ')
            pass2 = input('ReEnter selected password: ')
        elif pass1 != pass2:
            print('Passwords do not match! Please try again....')
            self.Add_user()
        else:
            pass
        dictionary = {  # Data to be written
            f"student name": {student_name},
            "student id": {student_id},
            "email": {email},
            "password": {pass1},
            "unique file": {random.Random()}
        }
        try:
            userdata_path = self.user_database
            json_object = json.dumps(dictionary, indent=4)  # Serializing json
            with open(userdata_path, "w") as userprofile:  # Writing to user-table.json
                userprofile.write(json_object)
            print(f'{student_name} registered successfully!')
        except Exception as ErrorMsg:
            print(f'Failed to register {student_name}....')
            print(f'[jsonHandlingError]\n{ErrorMsg}')
            return ErrorMsg

    def Access_User(self, email, student_id, password, mode='Availability Scan'):
        f = open(self.user_database, "r")  # JSON file
        data = json.load(f)  # returns JSON object as a dictionary
        for i in data['user_details']:  # Iterating through the json as a list
            if mode.lower() == 'availability scan':
                if student_id in data:
                    print(f"{student_id} already registered to an account...\n ")
                    print(f"Please make sure you entered your ID correctly or contact support staff if problem "
                          f"persists\n")
                elif email in data:
                    print(f"{email} already registered to an account...\n")
                    print(
                        "Please make sure you've entered the right email address or try again using a different one\n")
                elif email not in data:
                    print(f'{email} is available')
                elif student_id not in data:
                    print(f'{student_id} is available')
            elif mode.lower() == "login":
                if email in data & student_id in data & password in data:
                    print('Authentication Successful....\n')
                    print(f'Logged in as {student_id}')
                    # FIX
                elif email not in data or student_id not in data:
                    print(f'data {student_id} does not exist....\n')
                    print('Please try again later....\n')
                else:
                    print('Authentication Failed....\n')
                    print('Please try again Later....\n')
        f.close()  # Closing file
