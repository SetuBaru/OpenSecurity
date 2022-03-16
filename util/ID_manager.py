import json
import os
import random


class ManagementConsole:

    def __init__(self):
        self.current_path = os.getcwd()
        self.data_path = '../data/_cache_'
        self.log_path = f'{self.data_path}/_log_.txt'
        self.user_path = f'{self.data_path}/user_file.json'
        print(f'Set data_path = {self.data_path}, log_path= {self.log_path}, user_path= {self.user_path}.')

    def Add_member(self, target_name=None, number=None, email=None, address=None):
        if target_name is None:
            target_name = input("Enter the target's Full Name: ")
        elif number is None:
            number = input("Enter the target's Contact_No: ")
        elif email is None:
            email = input("Enter the target's Email: ")
        elif address is None:
            address = input("Enter the target's Current Address: ")
        else:
            pass
        target_name, number, email, address = str(target_name), str(number), str(email), str(address)
        try:
            print('Generating User ID...')
            new_id = random.randint(0, 9999999999999999999999999)
            id_gen_count = 0
            print('Checking Availability...')
            if self.lookup() != {}:
                print(f"{self.user_path} is empty!....")
                while self.lookup(id_no=new_id) is not False:
                    new_id = random.randint(0, 9999999999999999999999999)
                    if id_gen_count >= 10:
                        print(f"Exceeded max ID generation Limit... Please try again later!")
                        return False
                    else:
                        id_gen_count = id_gen_count + 1
            else:
                pass
            id_no = new_id
        except Exception as ReadError:
            print(f"'READERROR' encountered! {ReadError}")
            return False

        user_info = {  # Data to be written
            id_no:
                {
                    "Full Name": target_name,
                    "Contact_No": number,
                    "Email": email,
                    "Current Address": address
                }
        }
        try:
            user_path = self.user_path
            json_object = json.dumps(user_info, indent=4)  # Serializing json
            with open(user_path, "w") as userprofile:  # Writing to user_file.json
                userprofile.write(json_object)
            print(f"{target_name}'s Data has been registered successfully!")
        except Exception as ErrorMsg:
            print(f'Failed to register {target_name}....')
            print(f'jsonHandlingError:\t{ErrorMsg}')
            return False
        print(f"{user_info} has been added to {self.user_path} Successfully!")
        return True

    def lookup(self, id_no=None, _name=None, _number=None, _email=None):
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
                if _name is not None and _name in data[aa]["Full Name"]:
                    if _number is not None and _number in data[aa]["Contact_No"]:
                        if _email is not None and _email in data[aa]["Email"]:
                            print(f"'{_email}' Located at {data[aa]}")
                            f.close()
                            return data[aa]
                        print(f"'{_number}' Located at {data[aa]}")
                        f.close()
                        return data[aa]
                    print(f"'{_name}' Located at {data[aa]}")
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
