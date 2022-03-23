import json
import os
import random


class dB:
    # db Object Initialization Function.
    # sets important work paths.
    def __init__(self):
        self.current_path = os.getcwd()
        self.data_path = '../data/_cache_'
        self.log_path = f'{self.data_path}/LOG.txt'
        self.user_path = f'{self.data_path}/user_file.json'
        print(f'Set data_path = {self.data_path}, log_path= {self.log_path}, user_path= {self.user_path}.')

    # Function to add data to the user_file
    def append(self, _target=None, _number=None, _email=None, _address=None):
        # Get all relevant information.
        if _target is None:
            _target = input("Enter the target's Full Name: ")
        elif _number is None:
            _number = input("Enter the target's Contact_No: ")
        elif _email is None:
            _email = input("Enter the target's Email: ")
        elif _address is None:
            _address = input("Enter the target's Current Address: ")
        else:
            pass
        _target, _number, _email, _address = str(_target), str(_number), str(_email), str(_address)
        # Try to
        # Generate an ID randomly new entries.
        try:
            print('Generating User ID...')
            new_id = random.randint(0, 9999999999999999999999999)
            id_gen_count = 0
            print('Checking Availability...')
            # Conduct a search to determine if the ID is in the user_file
            if self.query() != {}:
                print(f"{self.user_path} is empty!....")
                while self.query(id_no=new_id) is not False:
                    new_id = random.randint(0, 9999999999999999999999999)
                    if id_gen_count >= 10:
                        print(f"Exceeded max ID generation Limit... Please try again later!")
                        return False
                    else:
                        id_gen_count = id_gen_count + 1
            # The ID is assigned to a variable.
            id_no = new_id
            # Error Handling.
        except Exception as ReadError:
            print(f"'READERROR' encountered! {ReadError}")
            return False
        # Draft up the entry utilising dictionary properties.
        user_info = {  # Data to be written
            id_no:
                {
                    "Full Name": _target,
                    "Contact_No": _number,
                    "Email": _email,
                    "Current Address": _address
                }
        }

        # Trying to write the user_info dictionaries to a text file and handling
        # resultant errors.
        try:
            user_path = self.user_path
            json_object = json.dumps(user_info, indent=4)  # Serializing json
            with open(user_path, "w") as userprofile:  # Writing to user_file.json
                userprofile.write(json_object)
            print(f"{_target}'s Data has been registered successfully!")
        except Exception as ErrorMsg:
            print(f'Failed to register {_target}....')
            print(f'jsonHandlingError:\t{ErrorMsg}')
            return False
        print(f"{user_info} has been added to {self.user_path} Successfully!")
        return True

    def query(self, id_no=None, _target=None, _number=None, _email=None):
        f = open(self.user_path, "r")  # JSON file
        data = json.load(f)  # returns JSON object as a dictionary
        if data is {}:
            print(f'{self.user_path} is Empty!')
            return None
        elif id_no is not None:
            if id_no in data:
                print(f"'{id_no}' Located at {data[id_no]}")
                f.close()
                return data[id_no]
            else:
                print(f"{id_no} not found!")
                f.close()
                return False
        else:
            for aa, bb in data:
                if _target is not None and _target in data[aa]["Full Name"]:
                    if _number is not None and _number in data[aa]["Contact_No"]:
                        if _email is not None and _email in data[aa]["Email"]:
                            print(f"'{_email}' Located at {data[aa]}")
                            f.close()
                            return data[aa]
                        print(f"'{_number}' Located at {data[aa]}")
                        f.close()
                        return data[aa]
                    print(f"'{_target}' Located at {data[aa]}")
                    f.close()
                    return data[aa]

                elif _number is not None and _number in data[aa]["Contact_No"]:
                    if _email is not None and _email in data[aa]["Email"]:
                        print(f"'{_email}' Located at {data[aa]}")
                        f.close()
                        return data[aa]
                    print(f"'{_number}' Located at {data[aa]}")
                    f.close()
                    return data[aa]

                elif _email is not None and _email in data[aa]['Email']:
                    print(f"'{_number}' Located at {data[aa]}")
                    f.close()
                    return data[aa]
                else:
                    print(f"No Results Found!")
                    f.close()
                    return False

    def remove(self, id_no):
        try:
            user_path = self.user_path
            f = open(user_path, "r")  # JSON file
            data = json.load(f)  # returns JSON object as a dictionary
            if data == {}:
                print(f"{user_path} is already empty! Unable to Remove User.")
                return False
        except Exception as ErrorMsg:
            print(f"'UserRemovalError'{ErrorMsg}....")
            return False
        print(f"{id_no} has been removed from {user_path} Successfully!")
        return True
