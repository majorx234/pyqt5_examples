#! /usr/bin/python
import sys
import cv2
import numpy as np
from pathlib import Path

def read_csv(filename):
    import csv
    import numpy as np

    images = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            assert len(row) == 2
            images.append(cv2.imread(row[0], 0))
            labels.append(int(row[1]))

    images = np.asarray(images)
    labels = np.asarray(labels)
    return images, labels

def create_and_train_model(images, labels):
    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8,
        threshold=60.00)
    model.train(images, labels)
    return model

def detect_faces(image, cascade_file):
    face_cascade = cv2.CascadeClassifier(cascade_file)
    return face_cascade.detectMultiScale(image)

def mark_faces(image, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

def get_user(prediction):
    users = {0: 'person_0', 1: 'person_1', 2: 'person_2', 3: 'wer anners', 4: 'constantine' }
    return users[prediction]

def main(video_file, csv_file = 'faces.csv'):
    cascade_file = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'

    images, labels = read_csv(csv_file)
    print("csv_loaded")

    model = create_and_train_model(images, labels)
    print("model trained")
    cap = cv2.VideoCapture(video_file)
    while True:
        ret = 0
        img = np.zeros((480,640,3), np.uint8)
        not_ok = True
        while(not_ok):
            ret, img = cap.read()
            if img is None:
                not_ok = True
            else:
                not_ok = False
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        assert ret 
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(grey, cascade_file )
        mark_faces(img, faces)

        user = ''
        
        for (x, y, w, h) in faces:
            face_img = grey[y:y + h, x:x + w]
            img_h, img_w = images[0].shape[:2]
            face_res = cv2.resize(face_img, (img_w, img_h))

            pred, conf = model.predict(face_res)
            if pred == -1:
                continue

            user = get_user(pred)
            print(user, conf)
            cv2.putText(img, '%s' % user, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0))

        cv2.imshow('img', img)
        if (cv2.waitKey(30) & 0xff) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: train_model <videofile> <csv file with images;ids>")
        sys.exit(1)

    video_file=sys.argv[1]
    csv_file=sys.argv[2]
    print("start main")
    main(video_file, csv_file)
