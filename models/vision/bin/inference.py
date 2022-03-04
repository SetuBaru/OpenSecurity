import user_management as manage
import face_recognition
import cv2
import numpy as np
import os

# Load sample pictures and learn how to recognize them.
manage = manage.ManagementConsole()


class FaceId:
    def __init__(self):
        print('FaceID object Initialization successful!....')
        # setting defaults.
        self.known_face_encodings = []
        self.known_face_ids = []
        self.vid_capture = None
        self.sample_path = '/known_samples'

    # batched_learning function.
    # target stores relative path to samples
    # focus stores an optional target that can be focused on, for targeted learning, else learning will be full.
    # ignored list contains directories or files to be ignored during indexing.
    def batched_learning(self, target=None, focus=None, ignored=None):

        # checks if the target path to traverse in is set to None
        if target is None:
            target = self.sample_path
        else:
            pass

        # Checks if the target provided is a directory.
        if os.path.isdir(target):
            known_sample_path = target

        # Attempts to fix path errors by re-formatting the target specified relative to current working directory.
        else:
            print(f"{target} is not an Active directory, dealing with discrepancies...")
            known_sample_path = os.getcwd() + target

        # Checks if the target specified is not a directory, if so returns Invalid_Path
        if not os.path.isdir(known_sample_path):
            print(f'Invalid path selected. {target} cannot be used.')
            return f'Invalid_Path'

        # else checks if the target specified is a directory, if so accepts it.
        else:
            print(f'{known_sample_path} successfully verified!!')

        # Begins traversing known_samples_path
        print(f'Search path set to {known_sample_path}')

        # Checks if an ignored list is specified, if not it generates ones.
        if ignored is None:
            ignored = ['.DS_Store']

        # Initializing a variable to store the current path.
        current = None

        # Iterates through directories within a target path.
        for _id_ in os.listdir(known_sample_path):

            # Checks if current Iterable is in the ignored list.
            if _id_ not in ignored:

                # Checks if the user has set a focus, if not then creates a path to iterable.
                if focus is None:
                    print(f"Indexing {_id_}...")
                    current = known_sample_path + '/' + _id_

                # verifies if focus is set.
                elif focus is not None:

                    # Checks to see if the current iterable is the same as focus, if so then creates a relative path.
                    if _id_.lower() == focus.lower():
                        print(f'Target {focus} Located! Attempting to Index....')
                        current = known_sample_path + '/' + _id_

                # Safety Net.
                else:
                    print('Conditions Validation Error.....')
                    return 'InvalidConditions'

            # Traverses the current set path if it exists.
            if current is not None:
                for _image in os.listdir(current):

                    # Creates a path to the iterable.
                    sample_image = current + '/' + _image

                    # Makes sure each iterable is not in ignored and is a file.
                    if _image not in ignored and os.path.isfile(sample_image):
                        # Calls the learn function to learn iteratively.
                        try:
                            print(f'Attempting to Encode {_image}...')
                            self.learn(sample_image, _id_)
                            print(f'{_image} encoded successfully!...')
                        except Exception as LearningError:
                            print(f'Unable to learn encodings for {_image}!!')
                            return f'ModuleInitializationError {LearningError}'

                    # Displays a message if target is not a valid file.
                    elif _image in ignored or not os.path.isfile(sample_image):
                        print(f'{_image} is NotAFile! skipping...')
        print("........Learning Complete!...")

    # Function to Learn Features.
    # sample_image indicated relative path to sample image.
    # sample_name indicates label or name assigned to that sample.
    def learn(self, sample_image, sample_name):

        # Load a sample picture and learn how to recognize it.
        _image = face_recognition.load_image_file(sample_image)
        _encoding = face_recognition.face_encodings(_image)[0]

        # Create array of known face encodings and IDs.
        self.known_face_encodings.append(_encoding)
        self.known_face_ids.append(sample_name)

    # Defines a function to detect and identify Faces. Cross-References real-time data against a predefined Dataset.
    def detect(self):

        # Initialize required variables.
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        print('Assigning Video Capture Object....\n')
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
                    face_distances = face_recognition.face_distance(self.known_face_ids, face_encoding)
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
