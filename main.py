import cv2
import face_recognition
import numpy as np
import os
import datetime
import json
import requests
# API_ENDPOINT - the end point of the web app that connects to twilio
from constants import API_ENDPOINT

images = []
file_names = []
# images is the directory that contains list of known images
file_names_with_ext = os.listdir("./images")

# reading and storing the known images in a list
for name in file_names_with_ext:
    img = cv2.imread(f"./images/{name}")
    images.append(img)
    file_names.append(name.split(".")[0])

def get_encodings(images):
    '''gets a list of images, encodes them and returns a new list with encoded images'''
    encodings = []
    
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodings.append(encode)
    return encodings

def write_to_csv(name):
    '''gets a name and writes it to a csv file along with the current time'''
    with open("visitors.csv", "r+") as file:
        datas = file.readlines()
        names_already_present = set()

        for line in datas:
            names_already_present.add(line.split(",")[0])
        
        if name not in names_already_present:
            time = datetime.time()
            time_str = time.strftime("%H:%M:%S")
            file.writelines(f'\n{name}, {time_str}')

def send_post(url, data={'Name': 'Unknown'}):
    '''makes a POST request to the given url and data'''
    requests.post(url, data=json.dumps(data))

# stores the encodings of known images in a list
known_faces_encondings = get_encodings(images)
# turns on camera and reads from it
cam = cv2.VideoCapture(0)
# infinite loop to read from camera always
while True:
    is_read, img = cam.read()
    img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # checks and finds faces in the frame
    live_faces_locations = face_recognition.face_locations(img)
    # converts the location of the frames into encodings
    live_faces_encodings = face_recognition.face_encodings(img, live_faces_locations)

    for face_loc, face_encoding in zip(live_faces_locations, live_faces_encodings):
        # compares the frame's encodings with known encodings
        matches = face_recognition.compare_faces(known_faces_encondings, face_encoding)
        # the lower the dist, the higher the chance of match
        dist = face_recognition.face_distance(known_faces_encondings, face_encoding)
        idx = np.argmin(dist) # idx with lowest dist value
        print(dist, matches)

        if matches[idx]:
            print("Match found", idx)
            # calls the function that writes the name of the person 
            # along with the time to a csv file
            #write_to_csv(file_names[idx])
            # calls the function that connects to the web app
            send_post(API_ENDPOINT, {'Name': file_names[idx]})
