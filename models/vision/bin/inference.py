import user_management as manage
import face_recognition
import cv2
import numpy as np
import os

# Load sample pictures and learn how to recognize them.
manage = manage.ManagementConsole()


class FaceId:
    def __init__(self):
        print('FaceID Object Initialization successful!....')
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
        # checks if target is None
        if target is None:
            target = self.sample_path
        else:
            pass

        # Checks if the _path provided is a directory.
        if os.path.isdir(target):
            known_sample_path = target
        # Attempts to fix Entry errors by formatting _path relative to current working dir.
        else:
            print(f"{target}doesn't look like an Active directory, attempting to deal with discrepancies...")
            known_sample_path = os.getcwd() + target

        # If path is not a directory returns Invalid_Path
        if not os.path.isdir(known_sample_path):
            print(f'Invalid path selected. {target} cannot be used.')
            return f'Invalid_Path'
        # else if path is a directory then it accepts submission.
        else:
            print(f'Path {known_sample_path} verified Successfully!!')

        # begins traversing known_samples_path
        print(f'Search path set to {known_sample_path}')

        # checks if ignored dir list is not set.
        if ignored is None:
            ignored = ['.DS_Store']

        # initializing environmental variables.
        current = None

        # iterates through directories within the target path
        for _id_ in os.listdir(known_sample_path):
            # filters only for iterables not in ignored list.
            if _id_ not in ignored:

                # Checks if the user has not set mode to focused, if so it creates path to iterable.
                if focus is None:
                    print(f"Attempting to Index {_id_}...")
                    current = known_sample_path + '/' + _id_

                # if focused mode is True and target is Set.
                elif focus is not None:
                    # checks to see if the current iterable is the same as target, if so then creates a path to it.
                    if _id_.lower() == focus.lower():
                        print(f'Target {focus} Located! Attempting to Index....')
                        current = known_sample_path + '/' + _id_
                # Safety Net.
                else:
                    print('Conditions Validation Error.....')
                    return 'InvalidConditions'

            # traverses the current set path if it exists.
            if current is not None:
                for _image in os.listdir(current):

                    # makes sure each iterable is not in ignored and is a file.
                    if _image not in ignored and os.path.isfile(_image):
                        sample_image = current + '/' + _image
                        print(f'Learning the encodings for {sample_image}')

                        # calls the learn function to learn iteratively.
                        try:
                            print(f'Attempting to Learn Encodings for {sample_image}...\n')
                            self.learn(sample_image, _id_)
                            print(f'{sample_image} encoded successfully!...')
                        except Exception as LearningError:
                            print(f'Unable to learn encodings for {sample_image}!!')
                            return f'ModuleInitializationError {LearningError}'

                    # Displays a message if target is not a valid file.
                    elif not os.path.isfile(_image):
                        print(f'{_image} skipped. NotAFile!...')

            # print Message if Current File is not indexed.
            elif current is None:
                print('NoPathSpecified....')

    # Function to Learn Features.
    # sample_image indicated relative path to sample image.
    # sample_name indicates label or name assigned to that sample.
    def learn(self, sample_image, sample_name):

        # Load a sample picture and learn how to recognize it.
        _image = face_recognition.load_image_file(sample_image)
        _encoding = face_recognition.face_encodings(_image)[0]

        # Create array of known face encodings and IDs
        self.known_face_encodings.append(_encoding)
        self.known_face_ids.append(sample_name)

    # Function to detect and Identify Faces by Cross-Referencing against local Database.
    def detect(self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        print('Assigning Video Capture Object....\n')
        self.vid_capture = cv2.VideoCapture(0)
        print('Video Capture Object Successfully set to 0.')
        while True:
            # Grab a single frame of video
            ret, frame = self.vid_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the _image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:

                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_ids, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_ids[best_match_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting _image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('Stopping Playback for CV2 Video Object...')
                break
        # Release handle to the webcam
        self.vid_capture.release()
        cv2.destroyAllWindows()
        print('Operation Terminated.')
