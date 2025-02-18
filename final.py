import tensorflow as tf
import cv2
import imutils
import numpy as np
import keras.utils
import pyttsx3
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from tensorflow.keras.models import load_model

# global variables
r = Tk()
bg = None
predicted_word = ""  # To store the accumulated word

# Function to segment the hand from the background
def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts, key=cv2.contourArea)
        return thresholded, segmented

# Function to calculate the running average
def run_avg(image, aWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, bg, aWeight)

# Function to clear a widget
def clear_widget(widget):
    widget.destroy()

# Function to reset the predicted word
def reset_word():
    global predicted_word, word_label
    predicted_word = ""
    word_label.config(text="Current Word: ")

# Function to detect hand using the camera
def dtect_hand():
    try:
        aWeight = 0.5
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        top, right, bottom, left = 10, 350, 225, 590
        num_frames = 0

        while True:
            grabbed, frame = camera.read()
            frame = imutils.resize(frame, width=700)
            frame = cv2.flip(frame, 1)
            clone = frame.copy()
            roi = frame[top:bottom, right:left]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            if num_frames < 30:
                run_avg(gray, aWeight)
            else:
                hand = segment(gray)
                if hand is not None:
                    thresholded, segmented = hand
                    cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                    cv2.imshow("Thresholded", thresholded)

            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)
            num_frames += 1
            cv2.imshow("Video Feed", clone)

            keypress = cv2.waitKey(1) & 0xFF
            if keypress % 256 == 32:
                img_name = "Clicked_image.png"
                cv2.imwrite(img_name, thresholded)
                print(f"{img_name} written!")
                predict_image('./Clicked_image.png')
                camera.release()
                cv2.destroyAllWindows()
                break
            if keypress == ord("q"):
                camera.release()
                cv2.destroyAllWindows()
                break
    except:
        messagebox.showwarning("WARNING", "PLEASE SHOW YOUR HAND INSIDE THE BOUNDING BOX!")
        camera.release()
        cv2.destroyAllWindows()

# Function to predict the character and update the word
def predict_image(image_path):
    try:
        global predicted_word, word_label
        model = load_model('modelslr.h5')
        test_image = keras.utils.load_img(image_path, target_size=(64, 64))  # Resize image
        test_image = keras.utils.img_to_array(test_image)  # Convert to array
        test_image = np.expand_dims(test_image / 255.0, axis=0)  # Normalize and expand dimensions
        pred = model.predict(test_image)
        y = np.argmax(pred)

        d1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
              'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
              'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
        y1 = list(filter(lambda x: d1[x] == y, d1))[0]

        predicted_word += y1
        word_label.config(text=f"Current Word: {predicted_word}")

        engine = pyttsx3.init()
        engine.say(f"The current character is: {y1}")
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to predict image. Error: {str(e)}")

# Function to add a photo and predict its value
def add_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        predict_image(file_path)

# GUI components
l1 = Label(r, text="SIGN LANGUAGE RECOGNITION SYSTEM", font=('Helvetica', 24, 'bold'))
l1.pack()

bs = Button(r, text='OPEN CAMERA', width=27, bg='yellow', command=dtect_hand, font=('Helvetica', 10, 'bold'))
bs.pack(side=TOP)

bs1 = Button(r, text='INPUT PHOTO', width=27, bg='yellow', command=add_photo, font=('Helvetica', 10, 'bold'))
bs1.pack(side=TOP)

bs2 = Button(r, text='CLEAR PREDICTION', width=27, bg='yellow', command=reset_word, font=('Helvetica', 10, 'bold'))
bs2.pack(side=TOP)

bs3 = Button(r, text='CLOSE', width=27, bg='yellow', command=r.destroy, font=('Helvetica', 10, 'bold'))
bs3.pack(side=TOP)

word_label = Label(r, text="Current Word: ", font=('Helvetica', 16, 'bold'))
word_label.pack(side=TOP)

frame = Frame(r, width=300, height=400)
frame.pack()
frame.place()

img = ImageTk.PhotoImage(Image.open(r"C:\Users\abhis\OneDrive\Desktop\Sign language dip pro\download.jpeg"), master=r)
label = Label(frame, image=img)
label.pack()

r.mainloop()
