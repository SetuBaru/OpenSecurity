import shutil
import os
import random
import Handler

handler = Handler()


# Data Control Object to simplify data processing operations.
class DataControl:

    # Initialization Function to prepare the Data Control venv
    def __init__(self, _state=None):
        if _state is None:
            print('DataControl Object Initialized Successfully!')
            print('Looking for Previous States....')
            # Checks for an old state save.
            if self.load_state():
                print('Load State Found. Load Presets?')
                self.last_state = self.load_state()
                # Option to Load
                x = input("Type 'l' to Load previous state or 'n' to create a new state: ")
                if x.lower() == 'l':
                    # Loading last state
                    self.__init__(_state=self.last_state)
                elif x.lower() == 'n':
                    print('Proceed with Default Settings or choose a custom setup?')
                    _x = input("Type 'd' for 'Default' and 'c' for 'Custom' setup: ")
                    # Mechanism to allow flexibility for multi- use cases.
                    if _x.lower() == 'd':
                        self.__init__(_state='default')
                    elif _x.lower() == 'c':
                        self.__init__(_state='custom')
                    else:
                        print(f'{_x} is an invalid response... please try again...')
                        self.__init__()
                else:
                    print(f"Invalid response'{x}'! please make a valid entry and retry!")
                    self.__init__()
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
            exit()

        elif _state == 'custom':
            t_p = input("Enter a target path to use. To use current path you can also type 'default': ")
            _dirs = input("Enter the directories you'll be working with Separated by Commas(eg: work, data, docs): ")
            print(f'Confirm choices? \ntarget path = {t_p}\t dirs = {_dirs}')
            self.set_path(target_path=t_p, _dirs=_dirs)
            print('Custom State has been created Successfully!')
            test = Handler.handle(Object=self.save_state(), LogResults=True)
            if test is True:
                self.save_State()
            else:
                print(f"'_StateSaveError' Occurred!\t{test}")
                self.__init__(_state='custom')
            exit()

        elif _state == 'default':
            self.work_path = os.getcwd()
            self.data_path = f'{self.work_path}/data'
            self.cache_path = f'{self.data_path}/_cache_'
            self.log_path = f'{self.cache_path}/LOG.txt'
            self.biometricDB = f'{self.data_path}/BioMetric.json'
            self.sample_path = f'{self.data_path}/samples'
            self.labelled_image_path = f'{self.data_path}'
            print("Data Paths set successfully!")
            # Setting Up data Objects
            self.embedding_path = {}  # Create a log to store paths
            self.generated_encodings = []
            self.known_identities = []
            print(' Data Objects Created successfully!')
            test = Handler.handle(Object=self.save_state(), LogResults=True)
            if test is True:
                self.save_State()
            else:
                print(f"'_StateSaveError' Occurred!\t{test}")
                self.__init__(_state='default')
            exit()

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
        pass
