import shutil
import face_recognition
import cv2
import numpy as np
import os
import random


class DataTool:

    def __init__(self):
        self.current_path = os.getcwd()
        self.log_path = 'data/LOG.txt'
        self.user_database = 'vision/data/usertable.json'
        self.data_path = 'data/Data'
        self.embedding_path = {}  # Create a log to store paths
        self.generated_encodings = []
        self.known_identities = []

    def build_path(self, target_path=None, folder_ref=None):
        if target_path is None:
            target_path = self.data_path
        elif folder_ref is None:
            folder_ref = random.randint(99999, 999999999)
            if folder_ref in os.listdir():
                folder_ref = random.randint(99999, 999999999)
            else:
                pass
        try:
            embedding_path = os.path.join(target_path, folder_ref)
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

    def RelocateFiles(self, source_path=None, target_path=None):
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
