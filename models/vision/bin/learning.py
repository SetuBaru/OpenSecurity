from inference import FaceId as Fd
import os
import json


# Importing the FaceID object
class Learning:
    # Function initialized on Learning Object Initialization.
    def __init__(self):
        # Checks if data path exits, else terminated initialization function.
        try:
            print('Checking if Directory Path Exists...')
            os.chdir(os.getcwd()[::-3] + '/' + 'data')
        except Exception as DataPathNotFound:
            print(f'DataPathError!... {DataPathNotFound}')
            exit()
        # specifies StateLog file.
        self.state_path = os.path.dirname('MachineState.json')
        # creates variables to store state encodings
        self.last = None
        self.current = {}
        self.next = None
        self.build = 0
        # checks if the state_path exists in cwd.
        if os.path.exists(self.state_path):
            # opens the state path file
            d = open(self.state_path, )
            # return JSON object as  dictionary
            data = json.load(d)
            # sets counter and state list.
            counter = 0
            positions = [self.last, self.current, self.next, self.build]
            # Traverses through the InternalStateMachine of the StateMachine.json and updates current state w/it.
            for state in data['InternalStateMachine']:
                # checks that counter is equal to or less than 2.
                while counter >= 3:
                    # alters the state list iteratively.
                    positions[counter] = state
                    # increments counter by a value of 1.
                    counter = counter + 1
                # closes the json file and alerts user.
                print('States transferred and counter Updated.')
                d.close()
                # terminates traversal.
                break
        # if the state_path does not exist in cwd.
        else:
            # Create the state_path and open it for Writing.
            with open(self.state_path, "w") as d:
                # Create InternalStateMachine
                print('Creating InternalStateMachine')
                json.dump({"InternalStateMachine": [self.last, self.current, self.next]}, d)
                # Alert user and close the state_path
                print('InternalStateMachineInitialized Successfully!')
                d.close()

    # Function to Learn and record Current State
    def learn(self):
        recognitions = {}
        fd = Fd()
        fd.batched_encode(sample_path='known')
        _last = [self.last, self.current, self.next]
        for _id in fd.known_face_ids:
            recognitions[_id] = fd.known_face_encodings
        _next = [self.last, recognitions[fd.known_face_ids], ]
        _current = [self.current, (self.current + self.next), ]
        # Create the state_path and open it for Writing.
        with open(self.state_path, "w") as d:
            # Create InternalStateMachine
            print('Creating InternalStateMachine')
            json.dump({"InternalStateMachine": [self.last, self.current, self.next]}, d)
            # Alert user and close the state_path
            print('InternalStateMachineInitialized Successfully!')
            d.close()
        self.build += 1

    # Function to Save Current State.
    def save(self):
        pass

    def update(self):
        pass
