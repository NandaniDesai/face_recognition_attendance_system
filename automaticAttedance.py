import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
from utils import text_to_speech, getImagesAndLabels

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "./Attendance"

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        text_to_speech("Haar Cascade file missing!")
        return False
    return True

def TrackImages(subject):
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists(f"Attendance/{subject}")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if not exists3:
        text_to_speech("Model not trained! Please train the model first!")
        return
    
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    df = pd.read_csv("StudentDetails/studentdetails.csv")
    col_names = ["Enrollment", "Name"]
    attendance = pd.DataFrame(columns=col_names)
    
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                aa = df.loc[df["Enrollment"] == serial]["Name"].values
                tt = str(serial) + "-" + aa[0]
                attendance.loc[len(attendance)] = [serial, aa[0]]
                cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            
            else:
                cv2.putText(im, "Unknown", (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        
        cv2.imshow("Taking Attendance", im)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
    fileName = f"Attendance/{subject}/{subject}_{date}.csv"
    
    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
    attendance.to_csv(fileName, index=False)
    
    cam.release()
    cv2.destroyAllWindows()
    
    text_to_speech("Attendance Marked Successfully!")

def take_attendance_window():
    window = tk.Tk()
    window.title("Take Attendance")
    window.geometry("1280x720")
    window.configure(background="#1E1E1E")
    
    # Header
    header = tk.Frame(window, bg="#E31937", height=80)
    header.pack(fill="x")
    
    title = tk.Label(
        header,
        text="TAKE ATTENDANCE",
        font=("Arial", 24, "bold"),
        bg="#E31937",
        fg="white"
    )
    title.pack(pady=20)
    
    # Content
    content = tk.Frame(window, bg="#1E1E1E")
    content.pack(fill="both", expand=True, pady=40)
    
    # Subject Entry
    tk.Label(
        content,
        text="Enter Subject",
        width=12,
        height=2,
        bg="#1E1E1E",
        fg="white",
        font=("Arial", 14)
    ).grid(row=0, column=0, padx=10, pady=10)
    
    subject_entry = tk.Entry(
        content,
        width=20,
        bg="white",
        fg="#1E1E1E",
        font=("Arial", 14)
    )
    subject_entry.grid(row=0, column=1, padx=10, pady=10)
    
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
    message.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Start Button
    def start_tracking():
        subject = subject_entry.get()
        if subject == "":
            text_to_speech("Please enter subject name!")
            return
        window.destroy()
        TrackImages(subject)
    
    tk.Button(
        content,
        text="Start Taking Attendance",
        command=start_tracking,
        bg="#E31937",
        fg="white",
        width=20,
        height=2,
        font=("Arial", 12)
    ).grid(row=2, column=0, columnspan=2, pady=20)
    
    window.mainloop()

if __name__ == "__main__":
    take_attendance_window()
