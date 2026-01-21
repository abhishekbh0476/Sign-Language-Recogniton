Sign Language Recognition System

This project implements a Sign Language Recognition System using Deep Learning, OpenCV, and a GUI-based application.
It recognizes hand gestures (A–Z) and converts them into readable characters with voice output.

📌 Features

1.Real-time hand gesture recognition using webcam

2.Image-based sign recognition (upload photo)

3.CNN-based trained model (.h5)

4.Graphical User Interface (Tkinter)

5.Text-to-Speech output

6.ASL alphabet reference image

7.Supports English alphabets (A–Z)

🛠️ Technologies Used

Python

TensorFlow / Keras

OpenCV

NumPy

Tkinter

Pillow

pyttsx3


▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/abhishekbh0476/Sign-Language-Recogniton.git
cd Sign-Language-Recogniton

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python final.py

🎥 How It Works

The user opens the camera or uploads an image.

The hand region is extracted using OpenCV.

The image is preprocessed and passed to the trained CNN model.

The predicted alphabet is displayed in the GUI.

The predicted character is spoken using Text-to-Speech.

📊 Dataset Information

The dataset used for training is included as DATASET.rar (32 MB).

It contains labeled hand gesture images for alphabets A–Z.

The dataset is used only for training purposes.

📌 Notes

Ensure good lighting conditions for better prediction accuracy.

Show only one hand inside the camera bounding box.

Press SPACE to capture the gesture during live detection.

👨‍💻 Author

Abhishek BH
Computer Science Engineering (CSE)
Sign Language Recognition Project

📜 License

This project is created for academic and learning purposes.
