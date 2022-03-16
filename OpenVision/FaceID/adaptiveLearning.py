import os
import json
from util import dataman

dm = dataman.Manager()


# Importing the FaceID object
class Memory:
    # Constructor for the Memory Object.
    def __init__(self):
        self.path = "../data/_cache_"
        self.biometric_path = f"{self.path}/BiometricRecord.json"
        self.biometric_object = {0: []}
        self.user_data = {}
        self.userpath = dm.user_path
        # Checks if data path exits, else terminated initialization function.
        print(f"Checking if {self.biometric_path} Path Exists...")
        if os.path.isfile(self.biometric_path):
            print("Path Already Exists....")
        else:
            print(f"{self.biometric_path} not found... Attempting to create the BiometricRecord...")
            # Create the record_ and open it for Writing.
            with open(self.biometric_path, "w") as d:
                # Create InternalStateMachine
                print('Creating Biometric Record...')
                json.dump(self.biometric_object, d)
                # Alert user and close the record_
                print('Biometric Record created Successfully!')
                d.close()
        print(f"Checking if {self.userpath} Path Exists...")
        if os.path.isfile(self.userpath):
            print("Path Already Exists....")
        else:
            print(f"{self.userpath} not found...")
            with open(self.userpath, "w") as d:
                # Create InternalStateMachine
                print('Creating User File...')
                user0 = {  # Data to be written
                    0:
                        {
                            "Full Name": "Abubakr Osama",
                            "Contact_No": "+249905460054",
                            "Email": "mrabubakrosama@gmail.com",
                            "Current Address": "Khartoum, Sudan."
                        }
                }
                json.dump(user0, d)
                # Alert user and close the record_
                print('User File created Successfully!')
                d.close()

    # Function to load the BiometricRecord and the user_file into memory.
    def Load(self):
        with open(self.biometric_path, "r+") as d:
            # Loading Biometric Object
            print('Updating Internal Biometric-data')
            data = json.load(d)
            # Alert user and close the record_
            self.biometric_object.update(data)
            print('Internal Biometric-data Updated Successfully!')
            d.close()
        with open(self.userpath, "r+") as d:
            # Loading User Object
            print('Updating Internal User-Data')
            data = json.load(d)
            # Alert user and close the record_
            self.user_data.update(data)
            print('Internal User-Data Updated Successfully!')
            d.close()
        print('UPDATES COMPLETED SUCCESSFULLY!')

    # Function to Save Current State.
    def Save(self):
        if self.biometric_object is not None:
            with open(self.biometric_path, "r+") as _data:
                # Create InternalStateMachine
                json_select = json.load(_data)
                for key, value in self.biometric_object.items():
                    json_select.setdefault(key, []).append(value)
                print('Updating Biometric Record...')
                json.dump(json_select, _data)
                # Alert user and close the record_
                print('Biometric Record Updated Successfully!')
                _data.close()
        elif self.user_data is not None:
            with open(self.userpath, "r+") as _data:
                # Create InternalStateMachine
                json_select = json.load(_data)
                json_select.append(self.user_data)
                json_select.seek(0)
                print('Updating User File...')
                json.dump(json_select, _data)
                # Alert user and close the record_
                print('User File Updated Successfully!')
                _data.close()
        else:
            print('Nothing to Save...')
        print("Records Updated Successfully!...")
