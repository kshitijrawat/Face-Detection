import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
def new():
    path = "sample"
    images = []
    classname = []
    mylist = os.listdir(path)
    print(mylist)
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classname.append(os.path.splitext(cl)[0])
    print(classname)

    def findEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist

    def markAttendance(name):
        with open('Attendance.csv', 'r+') as f:
            mydatalist = f.readlines()
            namelist = []
            for line in mydatalist:
                entry = line.split(',')
                namelist.append(entry[0])
            if name not in namelist:
                now = datetime.now()
                tstring = now.strftime('%H:%M:%S')
                dstring= now.strftime('%d/%m/%Y')

                f.writelines(f'\n{name},{tstring},{dstring}')

    encodelistknown = findEncodings(images)
    print("ENCODING COMPLETE")

    # cap=cv2.VideoCapture(0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while (True):

        sucess, img = cap.read()
        cv2.putText(img,'press q to exit',(0,25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgs)
        encodesCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

        for encodeFaces, faceloc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodelistknown, encodeFaces)
            facedis = face_recognition.face_distance(encodelistknown, encodeFaces)
            matchIndex = np.argmin(facedis)

            if (matches[matchIndex]):
                name = classname[matchIndex].upper()
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2),(0 , 255, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                markAttendance(name)

        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return 0