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

    def LearnEmbedding(self, sample_path, sample_name):
        # Load a sample picture and learn how to recognize it.
        image_sample = face_recognition.load_image_file(sample_path)
        generated_embedding = face_recognition.face_encodings(image_sample)[0]
        # Create array of known face encodings and IDs
        face_embeddings = [generated_embedding]
        face_ids = [sample_name]
        #   Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        video_capture = cv2.VideoCapture(0)
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(face_embeddings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]
                    face_ids = self.known_identities = np.unique(self.known_identities + face_ids)
                    face_embeddings = self.generated_encodings = np.unique(self.generated_encodings + face_embeddings)
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(face_ids, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = face_ids[best_match_index]
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

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
