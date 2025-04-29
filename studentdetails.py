import cv2
import os
import csv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from utils import text_to_speech, is_number, getImagesAndLabels

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if l1 == "" or l2 == "":
        err_screen()
        return
    try:
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcasecade_path)
        Enrollment = l1
        Name = l2
        sampleNum = 0
        directory = trainimage_path + "/" + Enrollment
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum = sampleNum + 1
                cv2.imwrite(
                    f"{directory}/Image{sampleNum}.jpg",
                    gray[y : y + h, x : x + w],
                )
                cv2.imshow("Frame", img)
            
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif sampleNum > 50:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        
        row = [Enrollment, Name]
        with open("StudentDetails/studentdetails.csv", "a+") as csvFile:
            writer = csv.writer(csvFile, lineterminator="\n")
            writer.writerow(row)
        csvFile.close()
        message.configure(text="Images Saved for ER No:" + Enrollment)
        text_to_speech("Images Saved for Enrollment Number " + Enrollment)
    except Exception as e:
        print(e)

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLabels(trainimage_path)
    try:
        recognizer.train(faces, np.array(Id))
    except Exception as e:
        message.configure(text="Please Register someone first!!!")
        text_to_speech("Please Register someone first")
        return
    
    recognizer.save(trainimagelabel_path)
    message.configure(text="Model Trained Successfully!")
    text_to_speech("Model Trained Successfully!")

def register_window():
    window = tk.Tk()
    window.title("Register New Student")
    window.geometry("1280x720")
    window.configure(background="#1E1E1E")

    # Header
    header = tk.Frame(window, bg="#E31937", height=80)
    header.pack(fill="x")
    
    title = tk.Label(
        header,
        text="STUDENT REGISTRATION",
        font=("Arial", 24, "bold"),
        bg="#E31937",
        fg="white"
    )
    title.pack(pady=20)

    # Content
    content = tk.Frame(window, bg="#1E1E1E")
    content.pack(fill="both", expand=True, pady=40)

    # Enrollment
    tk.Label(
        content,
        text="Enrollment No",
        width=12,
        height=2,
        bg="#1E1E1E",
        fg="white",
        font=("Arial", 14)
    ).grid(row=0, column=0, padx=10, pady=10)

    txt1 = tk.Entry(
        content,
        width=20,
        bg="white",
        fg="#1E1E1E",
        font=("Arial", 14)
    )
    txt1.grid(row=0, column=1, padx=10, pady=10)

    # Name
    tk.Label(
        content,
        text="Name",
        width=12,
        height=2,
        bg="#1E1E1E",
        fg="white",
        font=("Arial", 14)
    ).grid(row=1, column=0, padx=10, pady=10)

    txt2 = tk.Entry(
        content,
        width=20,
        bg="white",
        fg="#1E1E1E",
        font=("Arial", 14)
    )
    txt2.grid(row=1, column=1, padx=10, pady=10)

    # Message
    message = tk.Label(
        content,
        text="",
        bg="#1E1E1E",
        fg="white",
        width=32,
        height=2,
        font=("Arial", 14)
    )
    message.grid(row=3, column=0, columnspan=2, pady=10)

    # Buttons
    def take_image():
        TakeImage(
            txt1.get(),
            txt2.get(),
            "haarcascade_frontalface_default.xml",
            "TrainingImage",
            message,
            lambda: None,
            text_to_speech
        )

    def train_image():
        TrainImage(
            "haarcascade_frontalface_default.xml",
            "TrainingImage",
            "TrainingImageLabel/Trainner.yml",
            message,
            text_to_speech
        )

    tk.Button(
        content,
        text="Take Images",
        command=take_image,
        bg="#E31937",
        fg="white",
        width=20,
        height=2,
        font=("Arial", 12)
    ).grid(row=4, column=0, pady=20)

    tk.Button(
        content,
        text="Train Images",
        command=train_image,
        bg="#E31937",
        fg="white",
        width=20,
        height=2,
        font=("Arial", 12)
    ).grid(row=4, column=1, pady=20)

    window.mainloop()

if __name__ == "__main__":
    register_window() 