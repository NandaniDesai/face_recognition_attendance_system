import os
import cv2
import numpy as np
from PIL import Image
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def getImagesAndLabels(path):
    faces = []
    Ids = []
    
    # Handle both flat directory and nested directory structures
    if not os.path.exists(path):
        return faces, Ids
        
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Direct image file
            try:
                pilImage = Image.open(item_path).convert("L")
                imageNp = np.array(pilImage, "uint8")
                Id = int(os.path.splitext(item)[0].split("_")[1])
                faces.append(imageNp)
                Ids.append(Id)
            except Exception as e:
                print(f"Error processing image {item}: {str(e)}")
                continue
        elif os.path.isdir(item_path):
            # Nested directory
            for image_file in os.listdir(item_path):
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        image_path = os.path.join(item_path, image_file)
                        pilImage = Image.open(image_path).convert("L")
                        imageNp = np.array(pilImage, "uint8")
                        Id = int(os.path.splitext(image_file)[0].split("_")[1])
                        faces.append(imageNp)
                        Ids.append(Id)
                    except Exception as e:
                        print(f"Error processing image {image_file}: {str(e)}")
                        continue
    
    return faces, Ids

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False 