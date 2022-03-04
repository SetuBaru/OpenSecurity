from inference import FaceID
import os

# Initializing instance of FaceID class
FaceID = FaceID()

# Prepare sample path and sample name
sample_path = 'known_samples//Abubakr'
person = 'Abubakr'
# Traverse sample directory to learn face_encodings
for sample in os.listdir(sample_path):
    input_img = sample_path + '//' + sample
    # function Learn() takes 2 inputs: sample_image and sample_name
    FaceID.learn(input_img, person)
