from inference import FaceId as Fd
import os
import json


# Importing the FaceID object
class Learning:
    def __init__(self):

        try:
            print('Checking State...')
            os.chdir(os.getcwd()[::-2] + '/' + 'data')
        except Exception as DataPathNotFound:
            print(f'DataPathError:\t{DataPathNotFound}')
            return DataPathNotFound

        data_dir = os.path.dirname('DataPath.json')

        if os.path.exists(data_dir):
            self.state
            # Opening JSON file
            d = open(data_dir)
            # returns JSON object as dictionary
            data = json.load(d)
            # Iterating through  json list
            for i in data['01']:
                print(i)

    def fast(self):
        fd = Fd()
        fd.batched_learning(target='known')
