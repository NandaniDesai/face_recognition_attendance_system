import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image
from utils import text_to_speech, getImagesAndLabels


# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        # Create directory for trained model if it doesn't exist
        model_dir = os.path.dirname(trainimagelabel_path)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        # Initialize face recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Get faces and IDs
        faces, Ids = [], []
        
        # Check if directory exists
        if not os.path.exists(trainimage_path):
            res = "Training folder not found. Please take images first."
            message.configure(text=res)
            text_to_speech(res)
            return
            
        # Process each student folder
        for student_folder in os.listdir(trainimage_path):
            student_path = os.path.join(trainimage_path, student_folder)
            if os.path.isdir(student_path):
                try:
                    # Get enrollment number from folder name
                    enrollment = int(student_folder)
                    
                    # Process each image in student folder
                    for img_file in os.listdir(student_path):
                        if img_file.endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(student_path, img_file)
                            try:
                                # Convert image to grayscale
                                pilImage = Image.open(img_path).convert('L')
                                imageNp = np.array(pilImage, 'uint8')
                                
                                faces.append(imageNp)
                                Ids.append(enrollment)
                                print(f"Processing image: {img_path}")
                            except Exception as e:
                                print(f"Error processing image {img_path}: {str(e)}")
                                continue
                except ValueError:
                    print(f"Skipping invalid folder: {student_folder}")
                    continue
        
        if len(faces) == 0:
            res = "No valid images found for training. Please take images first."
            message.configure(text=res)
            text_to_speech(res)
            return
            
        print(f"Training model with {len(faces)} images...")
        # Train the model
        recognizer.train(faces, np.array(Ids))
        
        # Save the model
        print(f"Saving model to: {trainimagelabel_path}")
        recognizer.write(trainimagelabel_path)
        
        res = f"Model trained successfully with {len(faces)} images!"
        message.configure(text=res)
        text_to_speech(res)
        print(res)
        
    except Exception as e:
        res = f"Error during training: {str(e)}"
        message.configure(text=res)
        text_to_speech(res)
        print(res)

def check_haarcascadefile(haarcasecade_path):
    if not os.path.exists(haarcasecade_path):
        text_to_speech("Haar Cascade file missing!")
        return False
    return True

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def train_model():
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
            text_to_speech("No valid faces found in training images!")
            return False
        
        print(f"Training model with {len(faces)} faces...")
        
        # Create model directory
        os.makedirs("TrainingImageLabel", exist_ok=True)
        
        # Train and save the model
        recognizer.train(faces, np.array(ids))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        
        text_to_speech(f"Model trained successfully with {len(faces)} images!")
        return True
        
    except Exception as e:
        text_to_speech(f"Error during training: {str(e)}")
        print(f"Training error: {str(e)}")
        return False

if __name__ == "__main__":
    train_model()
