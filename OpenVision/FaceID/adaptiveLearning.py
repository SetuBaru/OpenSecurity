from faceId import FaceID as Fd
import os
import json


# Importing the FaceID object
class Memory:
    # Constructor for the Memory Object.
    def __init__(self):
        # Checks if data path exits, else terminated initialization function.
        try:
            print('Checking if Directory Path Exists...')
            os.chdir(os.getcwd()[::-3] + '/' + 'data')
        except Exception as DataPathNotFound:
            print(f'DataPathError!... {DataPathNotFound}')
            exit()
        # specifies BiometricRecord file.
        self.record_ = os.path.dirname('BiometricRecord.json')
        # Defining object attributes and Initial state vars.
        self.temp_ = [None, None, None]
        # checks if the record_ exists in cwd.
        if os.path.exists(self.record_):
            print(f'{self.record_} located. Loading data!')
        else:
            # Create the record_ and open it for Writing.
            with open(self.record_, "w") as d:
                # Create InternalStateMachine
                print('Creating InternalStateMachine')
                json.dump({"Biometric Record": self.temp_}, d)
                # Alert user and close the record_
                print('Biometric Record created Successfully!')
                d.close()

    # Function to move the biometric_record into a target variable
    def pull(self, record_=None, target_var=None):
        if record_ is None:
            record_ = self.record_
        if target_var is None:
            target_var = self.temp
        # Create the record_ and open it for Writing.
        with open(self.record_, "r") as d:
            # Create InternalStateMachine
            print('Creating InternalStateMachine')
            json.load({"Biometric Record": self.temp_}, d)
            # Alert user and close the record_
            print('Biometric Record created Successfully!')
            d.close()

    # Function to Save Current State.
    def push(self, source_var, biometric_record):
        pass
