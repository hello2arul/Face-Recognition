import cv2
import face_recognition
import numpy as np
import os
import datetime

images = []
file_names = []
file_names_with_ext = os.listdir("./images")

for name in file_names_with_ext:
    img = cv2.imread(f"./images/{name}")
    images.append(img)
    file_names.append(name.split(".")[0])

print(file_names)
cam = cv2.VideoCapture(0)

def get_encodings(images):
    encodings = []
    
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encodings.append(encode)
    return encodings

def write_to_csv(name):
    with open("visitors.csv", "r+") as file:
        datas = file.readlines()
        names_already_present = set()

        for line in datas:
            names_already_present.add(line.split(",")[0])
        
        if name not in names_already_present:
            time = datetime.time()
            time_str = time.strftime("%H:%M:%S")
            file.writelines(f'\n{name}, {time_str}')

known_faces_encondings = get_encodings(images)

cam = cv2.VideoCapture(0)

while True:
    is_read, img = cam.read()
    img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    live_faces_locations = face_recognition.face_locations(img)
    live_faces_encodings = face_recognition.face_encodings(img, live_faces_locations)

    for face_loc, face_encoding in zip(live_faces_locations, live_faces_encodings):
        matches = face_recognition.compare_faces(known_faces_encondings, face_encoding)
        # the lower the dist, the higher the chance
        dist = face_recognition.face_distance(known_faces_encondings, face_encoding)
        idx = np.argmin(dist) # idx with lowest dist value
        print(dist, matches)

        if matches[idx]:
            print("Match found", idx)
            write_to_csv(file_names[idx])
    




