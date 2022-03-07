import user_management as manage
import face_recognition
import cv2
import numpy as np
import os

# Load sample pictures and learn how to recognize them.
manage = manage.ManagementConsole()


class FaceId:
    def __init__(self):
        print('FaceID object Initialized.')
        # setting defaults.
        self.known_face_encodings = []
        self.known_face_ids = []
        self.biometrics = {}
        self.vid_capture = None
        self.sample_path = '/Users/mohammedabbarroh/PycharmProjects/OpenVision/models/vision/known_samples'
        self.counter1 = 0

    # batched_learning function.
    # target_path stores relative path to samples
    # focus stores an optional target that can be focused on, for targeted learning, else learning will be full.
    # ignored list contains directories or files to be ignored during indexing.
    def batched_encode(self, sample_path=None, target=None, ignored=None):
        # checks if the target path to traverse in is set to None
        if sample_path is None:
            sample_path = self.sample_path
        else:
            pass
        # Checks if the target provided is a directory.
        if os.path.isdir(sample_path):
            known_sample_path = sample_path
        # Attempts to fix path errors by re-formatting the target specified relative to current working directory.
        else:
            print(f"{sample_path} is not an Active directory, dealing with discrepancies...")
            known_sample_path = os.getcwd() + sample_path
        # Checks if the target specified is not a directory, if so returns Invalid_Path
        if not os.path.isdir(known_sample_path):
            print(f'Invalid path selected. {sample_path} cannot be used.')
            return f'Invalid_Path'
        # else checks if the target specified is a directory, if so accepts it.
        else:
            print(f'{known_sample_path} verified successfully.')
        # Begins traversing known_samples_path
        print(f'Search path set to {known_sample_path}')
        # Checks if an ignored list is specified, if not it generates ones.
        if ignored is None:
            ignored = ['.DS_Store']
        else:
            pass
        # Initializing a variable to store the current path.
        current = None
        # Iterates through directories within a target path.
        for _id_ in os.listdir(known_sample_path):
            # Checks if current Iterable is in the ignored list.
            if _id_ not in ignored:
                # Checks if the user has set a target, if not then creates a path to iterable.
                if target is None:
                    print(f"Indexing {_id_}...")
                    current = known_sample_path + '/' + _id_
                # verifies if target is set.
                elif target is not None:
                    # Checks to see if the current iterable is the same as target, if so then creates an object path.
                    if _id_.lower() == target.lower():
                        print(f'Located sample file for :{target}:! Indexing....')
                        current = known_sample_path + '/' + _id_
                    # else destroys current path.
                    else:
                        current = None
            # Traverses the current set path if it exists.
            if current is not None:
                for _image in os.listdir(current):
                    # Creates a path to the iterable.
                    sample_image = current + '/' + _image
                    # Makes sure each iterable is not in ignored and is a file.
                    if _image not in ignored and os.path.isfile(sample_image):
                        # Calls the learn function to learn iteratively.
                        try:
                            self.encode(sample_image, _id_)
                        except Exception as LearningError:
                            print(f'Unable to learn encodings for {_image}!!\n')
                            return f'ModuleInitializationError {LearningError}'
                    # Displays a message if target is not a valid file.
                    elif _image in ignored or not os.path.isfile(sample_image):
                        print(f'{_image} skipped...')
        print("Learning process completed successfully!!...")

    # Function to Learn Features.
    # sample_image indicated relative path to sample image.
    # sample_name indicates label or name assigned to that sample.
    def encode(self, sample_image, sample_name, prompt_on_id=False, attentive_learning=False):
        # Load a sample picture and learn how to recognize it.
        _image = face_recognition.load_image_file(sample_image)
        _encoding = face_recognition.face_encodings(_image)[0]

        # Checks if sample is part of the known_face_ids.
        if sample_name not in self.known_face_ids or self.known_face_ids == 0:
            # prompts user to make entry to known_face_ids and biometrics record.
            if prompt_on_id is True:
                _r = input('New Sample Detected.\nConfirm Entry(Y/N):\t')
                if _r.upper() == 'Y':
                    self.known_face_ids.append(sample_name)
                    self.biometrics.setdefault(sample_name, []).append(_encoding)
                    print(f'{sample_name} Biometric Data registered!')
                # allows the user to make another entry
                else:
                    _n = input('Please Re-enter sample name: ')
                    self.encode(sample_image, _n, True)
                    exit()
            # Adds the sample_name to the biometric record
            else:
                self.known_face_ids.append(sample_name)
                self.biometrics.setdefault(sample_name, []).append(_encoding)
                print(f'{sample_name} and Biometric Data registered!')
        else:
            pass

        # If the _encoding is not part of the known_face_encodings
        if len(self.known_face_encodings) == 0 or _encoding not in np.array(self.known_face_encodings):
            # appends it to known_face_encodings and adds it to the biometric record.
            self.counter1 = self.counter1 + 1
            print(f'Indexing: ({self.counter1})')
            self.known_face_encodings.append(_encoding)
            self.biometrics.setdefault(sample_name, []).append(_encoding)
        # Else if it is part of the known_face_encodings gives the user the option to locate it.
        else:
            print('Biometric Data already exists...\n')
            if attentive_learning is True:
                _r = input('Locate Associated ID?\n[Y/N]: ')
                if _r.upper() == 'Y':
                    # Lists the Biometrics key associated with a given _encoding
                    match_result = list(self.biometrics.keys())[list(self.biometrics.values()).index(_encoding)]
                    print('Source Located >> ' + match_result)
                else:
                    print('Action Aborted..')
            else:
                pass

    # Defines a function to detect and identify Faces. Cross-References real-time data against a predefined Dataset.
    def detect(self):
        print('Detection Function Initialized....')
        # Initialize required variables.
        face_locations = []
        # face_encodings = []
        face_names = []
        process_this_frame = True
        print('Assigning Video Capture Object....')
        self.vid_capture = cv2.VideoCapture(0)
        print('Video Capture Object Successfully set to 0.')

        # Initiates an open loop to control the videoCapture.
        while True:

            # Grab a single frame of video.
            ret, frame = self.vid_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing.
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the _image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses).
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time.
            if process_this_frame:

                # Finds all the faces and face encodings in the current frame of video.
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:

                    # See if the face is a match for the known face(s).
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face.
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_ids[best_match_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame

            # Display the results.
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size.
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face.
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face.
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting frames as cv2 Video preview.
            cv2.imshow('Video', frame)

            # Detects for the 'q' on keyboard to terminate VideoCapture!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('Stopping Playback for CV2 Video Object...')
                break

        # Release the VideoCapture Object and the cv2 windows.
        self.vid_capture.release()
        cv2.destroyAllWindows()
        print('Operation Terminated.')


if __name__ == "__main__":
    def test():
        os.chdir('../known_samples')
        print("current path: " + os.getcwd())
        _target = "Abubakr Osama"
        _f = FaceId()
        for _sample in os.listdir(_target):
            if _sample.upper() == '.DS_STORE':
                pass
            else:
                _f.encode(_target + '/' + _sample, _target)
        print(f"known Face ID's:\t{_f.known_face_ids}\n")
        print(f"Stored Embeddings:\n{_f.known_face_encodings}\n")
        print(f"Biometric Record:\n {_f.biometrics}")


    f_ = FaceId()
    f_.batched_encode(None, 'Emma Watsona')
