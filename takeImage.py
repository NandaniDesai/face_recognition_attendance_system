import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import Image, ImageTk
from utils import text_to_speech

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_haarcascadefile(haarcasecade_path):
    if not os.path.exists(haarcasecade_path):
        mess.showerror("Error", "Haar Cascade file missing!")
        return False
    return True

def train_images(message, text_to_speech):
    try:
        # Initialize recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Get the training images path
        training_path = "TrainingImage"
        
        if not os.path.exists(training_path):
            text_to_speech("Training folder is missing! Please take images first.")
            return False
            
        # Get all items in training directory
        items = os.listdir(training_path)
        
        if not items:
            text_to_speech("No training data found! Please register students first.")
            return False
            
        faces = []
        ids = []
        
        # Load face detector
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        # Process each enrollment directory
        for enrollment_dir in items:
            if not os.path.isdir(os.path.join(training_path, enrollment_dir)):
                continue
                
            try:
                # Verify enrollment number is valid
                enrollment = int(enrollment_dir)
                dir_path = os.path.join(training_path, enrollment_dir)
                
                # Process each image in the directory
                for image_name in os.listdir(dir_path):
                    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        continue
                        
                    image_path = os.path.join(dir_path, image_name)
                    print(f"Processing: {image_path}")
                    
                    try:
                        # Read and convert image
                        pil_image = Image.open(image_path).convert('L')
                        image_np = np.array(pil_image, 'uint8')
                        
                        # Detect face in image
                        faces_detected = detector.detectMultiScale(image_np)
                        
                        if len(faces_detected) > 0:
                            for (x, y, w, h) in faces_detected:
                                faces.append(image_np[y:y+h, x:x+w])
                                ids.append(enrollment)
                                print(f"Face detected in {image_name}")
                                
                    except Exception as e:
                        print(f"Error processing image {image_name}: {str(e)}")
                        continue
                        
            except ValueError as e:
                print(f"Invalid enrollment directory name: {enrollment_dir}")
                continue
            except Exception as e:
                print(f"Error processing directory {enrollment_dir}: {str(e)}")
                continue
        
        if not faces:
            msg = "No valid faces found in training images!"
            message.configure(text=msg)
            text_to_speech(msg)
            return False
        
        print(f"Training model with {len(faces)} faces...")
        
        # Create model directory
        os.makedirs("TrainingImageLabel", exist_ok=True)
        
        # Train and save the model
        recognizer.train(faces, np.array(ids))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        
        msg = f"Model trained successfully with {len(faces)} images!"
        message.configure(text=msg)
        text_to_speech(msg)
        return True
        
    except Exception as e:
        error_msg = f"Error during training: {str(e)}"
        message.configure(text=error_msg)
        text_to_speech(error_msg)
        print(f"Training error: {str(e)}")
        return False

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            
            # Create main training directory if it doesn't exist
            if not os.path.exists(trainimage_path):
                os.makedirs(trainimage_path)
            
            # Create student directory using enrollment number
            directory = str(Enrollment)  # Convert to string to be safe
            path = os.path.join(trainimage_path, directory)
            os.makedirs(path, exist_ok=True)
            
            while True:
                ret, img = cam.read()
                if not ret:
                    continue
                    
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    
                    # Save image with enrollment number in filename
                    img_filename = f"User.{Enrollment}.{sampleNum}.jpg"
                    img_path = os.path.join(path, img_filename)
                    cv2.imwrite(img_path, gray[y:y+h, x:x+w])
                    
                    cv2.imshow("Frame", img)
                
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            
            # Create StudentDetails directory if it doesn't exist
            os.makedirs("StudentDetails", exist_ok=True)
            
            # Save student details to CSV
            csv_path = "StudentDetails/studentdetails.csv"
            csv_exists = os.path.exists(csv_path)
            
            with open(csv_path, "a+", newline='') as csvFile:
                writer = csv.writer(csvFile)
                # Write header if file is new
                if not csv_exists:
                    writer.writerow(["Enrollment", "Name"])
                writer.writerow([Enrollment, Name])
            
            res = f"Images Saved for ER No:{Enrollment} Name:{Name}\nPlease click Train Images to complete registration."
            message.configure(text=res)
            text_to_speech(res)
            
        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            message.configure(text=error_message)
            text_to_speech(error_message)
            print(error_message)

def main():
    root = tk.Tk()
    root.title("Register New Student")
    root.geometry("1280x720")
    root.resizable(True, True)
    root.configure(background='white')

    # Create header
    header = tk.Frame(root, bg="#E31937")
    header.pack(fill=tk.X)
    
    title = tk.Label(
        header,
        text="KARNAVATI UNIVERSITY",
        bg="#E31937",
        fg="white",
        font=("Arial", 30, "bold"),
        pady=10
    )
    title.pack()
    
    subtitle = tk.Label(
        header,
        text="Student Registration",
        bg="#E31937",
        fg="white",
        font=("Arial", 20),
        pady=5
    )
    subtitle.pack()

    # Create main content frame
    content = tk.Frame(root, bg='white')
    content.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

    # Left side - Entry fields
    left_frame = tk.Frame(content, bg='white')
    left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20)

    # Enrollment Number
    tk.Label(
        left_frame,
        text="Enter Enrollment Number",
        bg='white',
        fg='#000000',  # Dark black text
        font=("Arial", 16, "bold")  # Increased size and made bold
    ).pack(pady=10)

    txt = tk.Entry(
        left_frame,
        width=20,
        font=("Arial", 15),
        fg='#000000',  # Dark black text
        bg='white',
        relief="groove",
        border=2
    )
    txt.pack(pady=5)

    # Student Name
    tk.Label(
        left_frame,
        text="Enter Student Name",
        bg='white',
        fg='#000000',  # Dark black text
        font=("Arial", 16, "bold")  # Increased size and made bold
    ).pack(pady=10)

    txt2 = tk.Entry(
        left_frame,
        width=20,
        font=("Arial", 15),
        fg='#000000',  # Dark black text
        bg='white',
        relief="groove",
        border=2
    )
    txt2.pack(pady=5)

    # Message display
    message = tk.Label(
        left_frame,
        text="",
        bg='white',
        font=("Arial", 12),
        wraplength=400
    )
    message.pack(pady=20)

    # Error screen (if needed)
    err_screen = tk.Label(
        left_frame,
        text="",
        bg='white',
        font=("Arial", 12),
        fg='red',
        wraplength=400
    )
    err_screen.pack(pady=10)

    # Right side - Buttons
    right_frame = tk.Frame(content, bg='white')
    right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20)

    # Take Images button
    takeImg = tk.Button(
        right_frame,
        text="1. Take Images",
        command=lambda: TakeImage(
            txt.get(),
            txt2.get(),
            "haarcascade_frontalface_default.xml",
            "TrainingImage",
            message,
            err_screen,
            text_to_speech
        ),
        fg="#000000",  # Dark black text
        bg="white",
        width=20,
        height=2,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        font=('Arial', 15, ' bold '),
        relief="groove",
        border=2
    )
    takeImg.pack(pady=20)

    # Train Images button
    trainImg = tk.Button(
        right_frame,
        text="2. Train Images",
        command=lambda: train_images(message, text_to_speech),
        fg="#000000",  # Dark black text
        bg="white",
        width=20,
        height=2,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        font=('Arial', 15, ' bold '),
        relief="groove",
        border=2
    )
    trainImg.pack(pady=20)

    # Clear button
    def clear():
        txt.delete(0, 'end')
        txt2.delete(0, 'end')
        message.configure(text="")
        err_screen.configure(text="")

    clearButton = tk.Button(
        right_frame,
        text="Clear",
        command=clear,
        fg="#000000",  # Dark black text
        bg="white",
        width=20,
        height=2,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        font=('Arial', 15, ' bold '),
        relief="groove",
        border=2
    )
    clearButton.pack(pady=20)

    # Quit button
    quitWindow = tk.Button(
        right_frame,
        text="Quit",
        command=root.destroy,
        fg="#000000",  # Dark black text
        bg="white",
        width=20,
        height=2,
        activebackground="#f0f0f0",
        activeforeground="#000000",  # Keep text dark when button is pressed
        font=('Arial', 15, ' bold '),
        relief="groove",
        border=2
    )
    quitWindow.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
