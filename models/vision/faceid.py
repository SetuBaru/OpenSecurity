from inference import FaceID
import os

# quick_learn function.
# _path stores relative path to samples
# ignored stores list of ignored directories
# specify stores whether the learning will be Focused or Complete
# target stores an optional target value to designate as learning target.

bad_dirs = ['.DS_Store']


def quick_learn(_path='/known_samples', target=None, ignored=None):
    # checks if ignored dir list is not set.
    if ignored is None:
        ignored = ['.DS_Store']

    # Initializing instance of FaceID class.
    face_id = FaceID()

    # initializing environmental variables.
    current = None

    # Checks if the _path provided is a directory.
    if os.path.isdir(_path):
        known_sample_path = _path

    # Attempts to fix Entry errors by formatting the _path relative to CWD
    else:
        print(f"{_path}doesn't look like an Active directory, attempting to deal with discrepancies...\n")
        known_sample_path = os.getcwd() + _path

    print(f'Verifying Selected path {known_sample_path}')

    # If path is not a directory returns Invalid_Path
    if not os.path.isdir(known_sample_path):
        print(f'Invalid path selected. {_path} cannot be used.\n')
        return f'Invalid_Path'

    # If path  is a directory then it accepts submission.
    else:
        print(f'Path {known_sample_path} verified Successfully!!\n')

    # begins traversing known_samples_path
    print(f'Search path set to {known_sample_path}\n')
    for _id_ in os.listdir(known_sample_path):

        # filters only for iterables not in ignored list.
        if _id_ not in ignored:

            # Checks if the user has not set mode to focused, if so it creates path to iterable.
            if target is None:
                print(f"Attempting to Index {_id_}...\n")
                current = known_sample_path + '/' + _id_

            # if focused mode is True and target is Set.
            elif target is not None:
                # checks to see if the current iterable is the same as target, if so then creates a path to it.
                if _id_.lower() == target.lower():
                    print(f'Target {target} Located! Attempting to Index....\n')
                    current = known_sample_path + '/' + _id_
            # Safety Net.
            else:
                print('Conditions Validation Error.....\n')
                return 'InvalidConditions'

        # traverses the current set path if it exists.
        if current is not None:
            for _image in os.listdir(current):

                # makes sure each iterable is not in ignored and is a file.
                if _image not in ignored and os.path.isfile(_image):
                    sample_image = current + '/' + _image
                    print(f'Learning the encodings for {sample_image}\n')

                    # calls the learn() method from the face_id class, achieves iterative learning.
                    # function requires a sample_image and sample_name as input.
                    # sample_image is the relative path to the image sample.
                    # sample_name is the name assigned to the sample image.
                    face_id.learn(sample_image, _id_)

                # Displays a message if target is not a valid file.
                elif not os.path.isfile(_image):
                    print(f'{_image} skipped. NotAFile!...\n')

        # print Message if Current File is not indexed.
        elif current is None:
            print('NoPathSpecified....\n')


# Main Test Function
if __name__ == "__main__":
    quick_learn()
