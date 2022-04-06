import shutil
import os
import random
from Handler import Handler

handler = Handler()


# Data Control Object to simplify data processing operations.
class DataControl:

    # Initialization Function to prepare the Data Control venv
    def __init__(self, _state=None):
        # Default Mode for initialization
        if _state is None:
            print('DataControl Object Initialized Successfully!')
            print('Looking for Previous States....')
            # Checks for an old state's saved data.
            if self.load_state():
                print('Load State Found. Load Presets?')
                self.last_state = self.load_state()
                # gives user an option to load the previous state
                x = input("Type 'l' to Load previous state or 'n' to create a new state: ")
                # if user decided to load state then init will be called again with the load_state() function as _state.
                if x.lower() == 'l':
                    self.__init__(_state=self.load_state())
                elif x.lower() == 'n':
                    print('You have chosen not to load the previous state and instead create a new state!..'
                          'Proceed with Default Settings or choose a custom setup?')
                    # allows the user to choose between a default mode or a custom data environment setup.
                    _x = input("Type 'd' for 'Default' and 'c' for 'Custom' setup: ")
                    if _x.lower() == 'd':
                        self.__init__(_state='default')
                    elif _x.lower() == 'c':
                        self.__init__(_state='custom')
                    # Goes back to default condition with _state still at None
                    else:
                        print(f'{_x} is an invalid response... please try again...')
                        self.__init__()
                else:
                    print(f"Invalid response'{x}'! please make a valid entry and retry!")
                    self.__init__()
            # If no state is found, prompts user to create a state that's either custom or default.
            else:
                print('No Load State found...')
                print('Proceed with Default Settings or choose a custom setup?')
                x = input("Type 'd' for 'Default' and 'c' for 'Custom' setup: ")
                # Mechanism to allow flexibility for multi- use cases.
                if x.lower() == 'd':
                    self.__init__(_state='default')
                elif x.lower() == 'c':
                    self.__init__(_state='custom')
                else:
                    print(f'{x} is an invalid response... please try again...')
                    self.__init__()
            # Exits the function
            exit()

        # checks if the current _state is set to custom
        elif _state == 'custom':
            # receives user input
            t_p = input("Enter a target path to use: ")
            _dirs = input("Enter the directories you'll be working with Separated by Commas(eg: work, data, docs): ")
            print(f'Confirm choices? \ntarget path = {t_p}\t dirs = {_dirs}')
            # feeds the user input into the set_path method to prepare the Data VenV
            self.set_path(target_path=t_p, _dirs=_dirs)
            print('Custom State has been created Successfully!')
            # Attempts to save the current State using the save_state function.
            test = Handler.handle(_object='self.save_state()', log_result=True)
            if test is True:
                self.save_state()
            else:
                print('Failed to Save Custom State....')
                self.__init__(_state='custom')
            # Exits the function
            exit()

        # Checks if the current _State is set to default
        elif _state == 'default':
            # Sets pre-defined path defaults
            self.work_path = os.getcwd()
            self.data_path = f'{self.work_path}/data'
            self.cache_path = f'{self.data_path}/_cache_'
            self.log_path = f'{self.cache_path}/LOG.txt'
            self.biometricDB = f'{self.data_path}/BioMetric.json'
            self.sample_path = f'{self.data_path}/samples'
            self.labelled_image_path = f'{self.data_path}'
            print("Data Paths set successfully!")
            # Sets Up data Objects
            self.embedding_path = {}  # Create a log to store paths
            self.generated_encodings = []
            self.known_identities = []
            print(' Data Objects Created successfully!')
            # Attempts to save the current state. (Attempts because handler.handle sandboxes the func catch errors!)
            test = Handler.handle(_object='self.save_state()', log_result=True)
            if test is True:
                self.save_state()
            else:
                print('Failed to Save State. Try Again...')
                self.__init__(_state='default')
            # Exits the function
            exit()

    # Function to set the path methods.
    def set_path(self, target_path=None, _dirs=None):
        if target_path.lower() == 'default':
            target_path = os.getcwd()
        elif target_path is None:
            target_path = self.work_path
        else:
            self.work_path = target_path
        if not _dirs.__contains__(','):
            print(f'{str(_dirs)} is that the dir you wish to setup?')
            x = input('(y/n)')
            if x.lower() == 'y':
                _dirs = str(_dirs)
            else:
                _dirs = input('Enter Dir to setup: ')
                self.set_path(target_path, _dirs)
                exit()
        else:
            _dir2 = _dirs.split(',')
            _dirs_ = []
            for _dir in _dir2:
                _dirs_.append(_dir.lstrip())
        if _dirs is None:
            self.data_path = f'{target_path}/data'
            self.cache_path = f'{self.data_path}/_cache_'
            self.log_path = f'{self.cache_path}/LOG.txt'
            self.biometricDB = f'{self.data_path}/BioMetric.json'

    def build_path(self, target_path=None, folder_ref=None):
        if target_path is None:
            target_path = self.data_path
        elif folder_ref is None:
            folder_ref = random.randint(9999, 999999999)
            while folder_ref in os.listdir():
                folder_ref = random.randint(99999, 999999999)
        else:
            pass
        try:
            embedding_path = os.path.join(target_path, str(folder_ref))
            os.makedirs(embedding_path)
            print(f' {embedding_path} Created Successfully.....\n')
            self.embedding_path[f'{folder_ref}'] = embedding_path
        except FileExistsError as msg:
            print('Whoops! Looks like file already exits.... \n')
            print(f'[FileExistsError]\n{msg}')
        except FileNotFoundError as msg:
            print('Unable to Locate path....\n')
            print(f'[FileNotFoundError]:\n{msg}')
        except Exception as msg:
            print(f'[EncounteredAnUnknownError]:\n{msg}')
        return True

    def relocate_files(self, source_path=None, target_path=None):
        if source_path is None:
            print('Please Specify a path to move data from...\n')
            source_path = input('Source Path: ')
        elif target_path is None:
            target_path = self.data_path
        for file in os.listdir(source_path):
            current_file = os.path.join(source_path, file)
            if os.path.isfile(current_file):
                source = current_file
                destination = target_path
                shutil.copy(source, destination)
                print(f'{file} moved successfully')

    def load_state(self):
        self.work_path = os.getcwd()
        self.data_path = f'{self.work_path}/data'
        self.cache_path = f'{self.data_path}/_cache_'
        self.log_path = f'{self.cache_path}/LOG.txt'
        self.biometricDB = f'{self.data_path}/BioMetric.json'
        self.sample_path = f'{self.data_path}/samples'
        self.labelled_image_path = f'{self.data_path}'

        # Setting Up data Objects
        self.embedding_path = {}  # Create a log to store paths
        self.generated_encodings = []
        self.known_identities = []
        return True

    def save_state(self):
        self.build_path()
